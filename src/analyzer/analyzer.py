from datasketch import MinHash, MinHashLSHForest

import argparse
import jmespath
import json
import pandas as pd


def getQueryMinHash(queryText):
  tokens = queryText.split(' ')
  m = MinHash(num_perm=128)

  for token in tokens:
    m.update(token.encode('utf8'))

  return m


def printStats(json_filename):
  with open(json_filename) as json_data:
    d = json.load(json_data)

    # Query simple index: queryNum -> queryText
    queryIndex = {}

    # Index of queries as a LSH forest for top-k similar queries.
    queriesLSHIndex = MinHashLSHForest(num_perm=128)

    # You can grok the CSV from stdout by using cut, e.g.,
    #
    # $ python analyzer.py -i ../../data/queries_ASTs.json | grep "csv:" | cut -d':' -f2 > /tmp/out.csv
    print 'csv:"queryNum","numExplicitJoins","referencedTables","groupByColumns","numGroupByClauses"'

    for queryNum, entry in enumerate(d):
      print '\n=> Stats for query number \"%s:\"' % queryNum

      # Group by clauses.
      groupByColumns = jmespath.search(
          'ast.statement[*].group.expression[*].name[]', entry)
      print 'groupBy columns: %s' % groupByColumns

      # Base tables when the query has no joins.
      baseTables = jmespath.search(
          'ast.statement[?from.variant == \'table\'].from.name[]', entry)
      print 'baseTables: %s' % baseTables

      # Base tables when the query has joins.
      baseTables += jmespath.search(
          'ast.statement[?from.variant == \'join\'].from.source.name[]', entry)
      print 'baseTables (with joins): %s' % baseTables

      # Join tables.
      joinTables = jmespath.search(
          'ast.statement[?from.variant == \'join\'].from.map[*].source.name[]', entry)
      print 'joinTables: %s' % joinTables

      # All tables mentioned in the query
      referencedTables = baseTables + joinTables

      # Joins.
      joinPathPrefix = 'ast.statement[*].from.map[*].constraint.on'
      joinsLeft = jmespath.search(joinPathPrefix + '.left.name', entry)
      joinsRight = jmespath.search(joinPathPrefix + '.right.name', entry)
      print 'explicit joins (left-hand side): %s' % joinsLeft
      print 'explicit joins (right-hand side): %s' % joinsRight

      # Text
      queryText = jmespath.search('queryText', entry)

      # Index it into an LSH forest for top-k textually similar queries.
      queryLSH = getQueryMinHash(queryText)
      queryIndex[queryNum] = {
          'queryText': queryText,
          'queryLSH': queryLSH
      }
      queriesLSHIndex.add(queryNum, queryLSH)

      # Sort for a prettier CSV dump.
      referencedTables.sort()
      groupByColumns.sort()
      # CSV header:
      # queryNum,numExplicitJoins,referencedTables,groupByColumns,numGroupByColumns
      print 'queryNum = %s' % queryNum
      print 'csv:"%s","%s","%s","%s","%s"' % (
          queryNum,
          len(joinsLeft[0]) if len(joinsLeft) > 0 else 0,
          ','.join(referencedTables),
          ','.join(groupByColumns),
          len(groupByColumns))

      # Populate a reverse index from table to script.
      tableToQuery = {}
      for referencedTable in referencedTables:
        if referencedTable not in tableToQuery:
          tableToQuery[referencedTable] = [queryNum]
        else:
          tableToQuery[referencedTable].append(queryNum)

    # Sample search on LSH forest index: top-3 most similar queries.
    queriesLSHIndex.index()
    k = 3
    queryNum = 10
    query = queryIndex[queryNum]
    print '\n\nTop %s queries similar to "%s":' % (k, query['queryText'])
    top_k = queriesLSHIndex.query(query['queryLSH'], k)
    for k in top_k:
      print '\n"%s"' % queryIndex[k]['queryText']


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description='Prints stats on SQL queries.')
  parser.add_argument('-i', '--input_json_filename',
                      help='Relative path of input JSON file containing SQL ASTs.',
                      required=True)
  args = parser.parse_args()

  printStats(args.input_json_filename)
