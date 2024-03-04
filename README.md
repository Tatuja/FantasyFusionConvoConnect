In order to run the script open the console and type:

```shell
$ python3 matcher.py <path to the csv input file> <number of rounds>
```
 
For example, having a csv file `data.csv` with content:

```csv
-,Alice,Bob,Jerry,Olivia
Alice,-,1,3,2
Bob,1,-,2,3
Jerry,3,2,-,1
Olivia,2,1,3,-
```

one can run:
```shell
$ python3 matcher.py data.csv 2
```
to get the output:
```
Round 1
Alice - Jerry, score: 15
Bob - Olivia, score: 7

Round 2
Alice - Olivia, score: 8
Bob - Jerry, score: 8
```
