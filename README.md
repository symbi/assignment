# homwork
Aukai Amusement Park assignment

## environment
```
$ python3 -V
Python 3.10.2
```
## How to run
```
git clone <repo>
cd assignment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd venv
python solution.py
```
Result is saved in [answer.log](https://github.com/symbi/assignment/blob/main/answer.log)

## The idea:
There are 4 conditions to meet the requirement:
```
condition 1 : {'kids': 3, 'food': 2, 'shop': 1, 'coaster': 2, 'flat': 2}

condition 2 : {'kids': 3, 'food': 2, 'shop': 1, 'coaster': 3, 'flat': 1}

condition 3 : {'kids': 2, 'food': 2, 'shop': 1, 'coaster': 2, 'flat': 3}

condition 4 : {'kids': 2, 'food': 2, 'shop': 1, 'coaster': 3, 'flat': 2}
```
The idea is to calculate each condition maximum attractions within budget and choose the condition with max attractions.

To get each condition maximum attractions:
* sort attraction amount descend by type
* tuning data: 
    * filtering out those less amount with more cost
    * get all combination subset of each type
    * sort by amount descend
* start from the first combination of each type (the one with largest amount), total cost is over budget.
* reduce to budget by each time choosing the one(the type) with max cost/amount rate, till under the budget
* add back to budget by each time swap with the one(the type) with max cost/amount rate if adding it still under budget.
* get the result
* compare the results of 4 conditions, select the one with max attractions amount.

## Clean up
```
deactivate
```
