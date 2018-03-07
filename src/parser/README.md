# SQL to AST parser

This is mostly a wrapper around SQLite's node.js parser. Assumes as input a txt file with one query per line, outputs a JSON file with one object per query AST.

```
$ node sql_to_AST.js [-i <INPUT_QUERIES_TXT_FILE>] [-o <OUTPUT_ASTS_JSON_FILE>]
```

## Default input:

```
../../data/queries.txt
```

## Default output

```
../../data/queries_ASTs.json
```
