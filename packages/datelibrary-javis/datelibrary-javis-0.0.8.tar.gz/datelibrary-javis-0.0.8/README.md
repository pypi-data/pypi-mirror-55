# Package Info

Date Extraction library built on top of Python native date libraries to support business vocabularies.

# Installation
```
 pip install datelibrary-javis
```

# Usage

```python
 import datelibrary
 from datelibrary.dates import DateData
 text = "my sales from june to aug'
 date_obj = DateData(text)
 print(date_obj.comile_dates())
 >>>['2018-06-01', '2018-08-31'] #list of strings
```

# Scope

>	current date = 5th November 2019

> current day = Tuesday


| Type | Parsed Date |
| ---- | ---- |
| ytd (year to date) | ['2019-01-01', '2019-11-05'] |
| mtd (month to date) | ['2019-11-01', '2019-11-05'] |
| qtd (quarter to date) | ['2019-10-01', '2019-11-05'] |
| l3m (last 3 months) | ['2019-07-01', '2019-10-30'] |
| june to august | ['2019-06-01', '2019-08-31'] |
| june 2018 to august 2018 | ['2018-06-01', '2018-08-31'] |
| june 2018 | ['2018-06-01'] |
|  1/6/2019 to 2/6/2019 | ['2019-06-01', '2019-06-02'] |
|  last month | ['2019-10-01', '2019-10-31'] |
|  last week | ['2019-10-27', '2019-10-03'] |
|  last year | ['2019-01-01', '2019-01-31'] |

