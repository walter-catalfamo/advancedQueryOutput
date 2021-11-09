# QueryByOutput

This project is able to build an SQL query when given an input table and an example of a result of a query on it. The algorithm is based on the paper _Query by Output (Tran et al.)_. Specifically case C1 is implemented.

## Execution

Here follows the result of the execution of:
```
python /home/adminuser/Desktop/progetto/QueryByOutput/query_by_output.py
```

Four cases are presented. The first one is the example from the paper, while the others show how the algorithm behaves in various cases

##### Output

----------Loading: db.csv,example.csv tables: ['master', 'batting']----------\
------DB-------\
['pID', 'name', 'country', 'weight', 'bats', 'throws', 'year', 'team', 'stint', 'HR']\
[[1, 1, 1, 85, 1, 0, 2001, 1, 2, 40], [1, 1, 1, 85, 1, 0, 2003, 2, 2, 50], [2, 2, 1, 72, 0, 0, 2001, 1, 1, 73], [2, 2, 1, 72, 0, 0, 2002, 1, 1, 40], [3, 3, 1, 80, 0, 1, 2004, 3, 2, 35], [4, 4, 2, 72, 1, 0, 2001, 1, 3, 60], [5, 5, 3, 72, 0, 0, 2004, 3, 3, 30]]\
------EXAMPLE------\
[[2], [5]]\
['name']\
------PROJECTED TABLE & TARGET CLASSES-------\
[[1], [1], [2], [2], [3], [4], [5]]\
[-1, -1, 0, 0, -1, -1, 1]\
------DECORATED TABLE------\
[[-1, 1, 1, 1, 85, 1, 0, 2001, 1, 2, 40], [-1, 1, 1, 1, 85, 1, 0, 2003, 2, 2, 50], [0, 2, 2, 1, 72, 0, 0, 2001, 1, 1, 73], [0, 2, 2, 1, 72, 0, 0, 2002, 1, 1, 40], [-1, 3, 3, 1, 80, 0, 1, 2004, 3, 2, 35], [-1, 4, 4, 2, 72, 1, 0, 2001, 1, 3, 60], [1, 5, 5, 3, 72, 0, 0, 2004, 3, 3, 30]]\
-------TREE-------\
attribute: 9 threshold 1.5::\
	&emsp;&emsp;1\
	&emsp;&emsp;attribute: 1 threshold 4.5\
	&emsp;&emsp;	&emsp;&emsp;-1\
	&emsp;&emsp;	&emsp;&emsp;1\
**SELECT name FROM master JOIN batting WHERE ((stint <= 1.5) OR (stint > 1.5 AND ((pID > 4.5))))**\
*Example 1 is the example of the paper, as you can see the output is very similar, although not equal, as we consider pID to be numerical by giving it an identifier and thus making it usable*

----------Loading: db2.csv,example2.csv tables: ['people']----------\
------DB-------\
['birthYear', 'height', 'weight']\
[[0, 200, 80], [0, 200, 70], [200, 100, 80], [200, 100, 70]]\
------EXAMPLE------\
[[0, 200, 80], [200, 100, 70]]\
['birthYear', 'height', 'weight']\
------PROJECTED TABLE & TARGET CLASSES-------\
[[0, 200, 80], [0, 200, 70], [200, 100, 80], [200, 100, 70]]\
[1, -1, -1, 1]\
------DECORATED TABLE------\
[[1, 0, 200, 80], [-1, 0, 200, 70], [-1, 200, 100, 80], [1, 200, 100, 70]]\
-------TREE-------\
attribute: 1 threshold 100.0\
	&emsp;&emsp;attribute: 3 threshold 75.0\
	&emsp;&emsp;	&emsp;&emsp;-1\
	&emsp;&emsp;	&emsp;&emsp;1\
	&emsp;&emsp;attribute: 3 threshold 75.0\
	&emsp;&emsp;	&emsp;&emsp;1\
	&emsp;&emsp;	&emsp;&emsp;-1\
**SELECT birthYear, height, weight FROM people WHERE ((birthYear <= 100.0 AND ((weight > 75.0))) OR (birthYear > 100.0 AND ((weight <= 75.0))))**\
*Example 2 shows that the algorithm is able to find opposite conditions depending on the specific subtree. See where weight is first selected >75 and then <=75 in the right subtree*

----------Loading: db3.csv,example3.csv tables: ['people']----------\
------DB-------\
['birthYear', 'height', 'weight']\
[[0, 200, 80], [0, 200, 70], [200, 100, 80], [200, 100, 70]]\
------EXAMPLE------\
[[0, 200, 80], [200, 100, 80]]\
['birthYear', 'height', 'weight']\
------PROJECTED TABLE & TARGET CLASSES-------\
[[0, 200, 80], [0, 200, 70], [200, 100, 80], [200, 100, 70]]\
[1, -1, 1, -1]\
------DECORATED TABLE------\
[[1, 0, 200, 80], [-1, 0, 200, 70], [1, 200, 100, 80], [-1, 200, 100, 70]]\
-------TREE-------\
attribute: 3 threshold 75.0\
	&emsp;&emsp;-1\
	&emsp;&emsp;1\
**SELECT birthYear, height, weight FROM people WHERE ((weight > 75.0))**\
*Example 3 shows that the algorithm is able to find the best attribute that can select the desired queries, reducing considerably the query size*

----------Loading: db4.csv,example4.csv tables: ['people']----------\
------DB-------\
['birthYear', 'height', 'weight']\
[[0, 200, 80], [0, 200, 70], [200, 100, 80], [200, 100, 70]]\
------EXAMPLE------\
[[0, 300, 80], [200, 300, 80]]\
['birthYear', 'height', 'weight']\
------PROJECTED TABLE & TARGET CLASSES-------\
[[0, 200, 80], [0, 200, 70], [200, 100, 80], [200, 100, 70]]\
**No query can be found to match a row in the example:**\
[0, 300, 80]\
*Example 4 shows that if a query doesn't exist (impossible rows), it is not possible to find a query*

Process finished with exit code 0


