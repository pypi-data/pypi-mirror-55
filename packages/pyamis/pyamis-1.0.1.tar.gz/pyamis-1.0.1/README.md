# PyAmis

## 1. Installation

Install with pip

- ```pip install pyamis```

## 2. Examples

```python
from __future__ import print_function
from pyamis import mod

table = mod.Table(
    title='AmisTable'
)
table.set_title('A Amis Table Example')
table.add_column('text', 'measurement', '${mea}')                      
table.add_column('text', 'avg value', '${avg_value}')                  
table.add_column('text', '90% value', '${percent_90}')                 
table.add_column('text', '99% value', '${percent_99}')                 
table.add_column('text', '99.9% value', '${percent_999}')              
rows_dict = {
    'mea': 'mb/s',
    'avg_value': 11, 
    'percent_90': 11.5,
    'percent_99': 11.54, 
    'percent_999': 11.55, 
}
table.set_rows([rows_dict])

# call xx.render() will get the json data that amis needs
# print(table.render())
```
