// SQLite grammar spec at https://www.sqlite.org/lang.html
var sqlParser = require('sqlite-parser');

//var csv = require('csv-parser');
var es = require('event-stream');
var fs = require('fs');

// Sanity check
var query = 'SELECT * FROM test';
var ast = sqlParser(query);
console.log('AST for sanity check query \"' + query + '\":');
console.log(prettify(ast) + '\n');

// TODO: Pass it as arg.
var jsonOutFilename = '../../data/queries_ASTs.json';
var jsonOut = [];

// Extract SQL queries from input txt file, building an AST for each one as we
// go. We also extract named tables as well, so we can infer the number of
// "materialized" views and joins on each script.
fs.createReadStream('../../data/queries.txt')
    .pipe(es.split())  // One query per line (no semi-colon required).
    .on('data',
        function(data) {

          // One query per line.
          var query = data.trim();
          var json = processQuery(query);
          if (json != null) {
            console.log('=> AST:\n' + prettify(json) + '\n');
            jsonOut.push(json);
          }
        })
    .on('end', function() {
      console.log('\n\nWriting queries to ' + jsonOutFilename + '...');
      writeToFile(jsonOutFilename, prettify(jsonOut));
    });

// Catch high level exceptions and ignore so we can continue for the next
// script.
process.on('uncaughtException',
           function(err) { console.log('Error: ' + err); });

// Extracts AST for a single SQL query.  Returns AST, if valid query,
// null otherwise.
function processQuery(query) {
  // Skip it if it's a comment.
  if (query.startsWith('--')) {
    return null;
  }

  var prettyQuery = query.replace(/\s+/g, ' ');

  // Skip empty queries.
  if (!prettyQuery) {
    return null;
  }

  console.log('====> Query: ' + prettyQuery);

  try {
    var ast = sqlParser(query);
    return {'queryText' : query, 'ast' : ast};
  } catch (err) {
    console.log('Could not build AST: ' + err);
    return null;
  }
}

// JSONify.
function prettify(ast) { return JSON.stringify(ast, null, ' '); }

function writeToFile(filename, data) {
  fs.writeFile(filename, data, 'utf8', function(err) {
    if (err) {
      return console.log(err);
    }
  });
}
