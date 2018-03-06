# Run

```
$ python analyzer.py -i ../../data/queries_ASTs.json
```

For CSV output:
```
$ python analyzer.py -i ../../data/queries_ASTs.json | grep "csv:" | cut -d':' -f2 > /tmp/out.csv

```
