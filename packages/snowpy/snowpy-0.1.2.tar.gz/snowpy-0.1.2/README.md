# SnowPy 
## Current release: SnowPy [v0.1.2]

<img src="" height="200">

'SnowPy' is a Python package providing a set of user-friendly functions to help upload and download data from database systems such as Microsoft SQL Server, Snowflake, (more to come). 'SnowPy' intially realsed as data tools for the mltoolkit project (https://mltoolkit.github.io/MLToolKit).

<img src="" height="200">

## Introduction
SnowPy is a Python library to upload and download data from database system

## Installation
```
pip install SnowPy
```
If the installation failed with dependancy issues, execute the above command with --no-dependencies

```
pip install SnowPy --no-dependencies
```

## Functions


## Usage
```python
import snowpy
```

### Warning: Python Variable, Function or Class names 
The Python interpreter has a number of built-in functions. It is possible to overwrite thier definitions when coding without any rasing a warning from the Python interpriter. (https://docs.python.org/3/library/functions.html)
Therfore, AVOID THESE NAMES as your variable, function or class names.
<table border="1">
<tr><td>abs</td><td>all</td><td>any</td><td>ascii</td><td>bin</td><td>bool</td><td>bytearray</td><td>bytes</td></tr>
<tr><td>callable</td><td>chr</td><td>classmethod</td><td>compile</td><td>complex</td><td>delattr</td><td>dict</td><td>dir</td></tr>
<tr><td>divmod</td><td>enumerate</td><td>eval</td><td>exec</td><td>filter</td><td>float</td><td>format</td><td>frozenset</td></tr>
<tr><td>getattr</td><td>globals</td><td>hasattr</td><td>hash</td><td>help</td><td>hex</td><td>id</td><td>input</td></tr>
<tr><td>int</td><td>isinstance</td><td>issubclass</td><td>iter</td><td>len</td><td>list</td><td>locals</td><td>map</td></tr>
<tr><td>max</td><td>memoryview</td><td>min</td><td>next</td><td>object</td><td>oct</td><td>open</td><td>ord</td></tr>
<tr><td>pow</td><td>print</td><td>property</td><td>range</td><td>repr</td><td>reversed</td><td>round</td><td>set</td></tr>
<tr><td>setattr</td><td>slice</td><td>sorted</td><td>staticmethod</td><td>str</td><td>sum</td><td>super</td><td>tuple</td></tr>
<tr><td>type</td><td>vars</td><td>zip</td><td>__import__</td></tr>
</table>

If you accedently overwrite any of the built-in function (e.g. list), execute the following to bring built-in defition.
```python
del(list)
```

## Functions
```
|- MSSQL
| |- execute_mssql_query
| |- read_data_mssql
| |- write_data_mssql
| |- read_data_mssql_bcp
| |- write_data_mssql_bcp
|- MySQL
|  |- To be integrated...
|- Snowflake
|  |- execute_snowflake_sql_query
|  |- read_data_snowflake
|  |- write_data_snowflake
|- CSV
|  |- read_data_csv
|  |- write_data_csv
```

## SnowPy Example
```python
# to be posted
```

### Data Loading 
```python
# to be posted
```

## License
```
Copyright 2019 Sumudu Tennakoon

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Cite as
```
@misc{SnowPy2019,
  author =  "Sumudu Tennakoon",
  title = "SnowPy: A Python library to upload and download data from database systems",
  year = 2019,
  publisher = "GitHub",
  howpublished = {\url{https://mltoolkit.github.io/SnowPy/}},
  version = "0.1.0"
}
```

## SnowPy Project Timeline
2018-07-02 [v0.0.1]: Initialte MLToolKit project.
2019-07-02 [v0.0.1]: Snowpy functions first released as etl tools for MLToolKit project (https://mltoolkit.github.io/MLToolKit/).
2019-07-02 [v0.1.0]: First Release of SnowPy as seperate package.
2019-11-11 [v0.1.1]: Bug Fixes and enhancements
2019-11-16 [v0.1.2]: Bug Fixes, Integrate MSSQL BCP support

## Future Release Plan
TBD [v0.1.5]: Integrate Data Exchage Server.
TBD [v0.1.6]: Integrate MySQL support.
TBD [v0.1.7]: Comprehensive Documentation

## References
- https://pandas.pydata.org/
- https://docs.snowflake.net/manuals/user-guide/python-connector.html
- https://www.numpy.org/
- https://docs.python.org/3.6/library/re.html
- http://json.org/
- https://www.sqlalchemy.org/
- https://docs.microsoft.com/en-us/sql/tools/bcp-utility
- https://github.com/mkleehammer/pyodbc/wiki

