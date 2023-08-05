# nextcode Python SDK

Nextcode-sdk is a python package for interfacing with Wuxi Nextcode services.

### Installation
```bash
$ pip install nextcode-sdk -U
```

```bash
$ pip install nextcode-sdk[jupyter] -U
```

### Getting started

```python
import nextcode
client = nextcode.Client(api_key="xxx")
qry = client.service("query")
qry.status()
qry.get_queries()
qry.get_query(query_id)
qry.list_templates()

```

### Jupyter notebooks

To start using the python sdk in Jupyter Notebooks you will first need to install it using the `jupyter` extras and then load the gor `%` magic extension.

```bash
$ pip install nextcode-sdk[jupyter] -U
%load_ext nextcode.gor
```

Now you can run gor with the following syntax:
```bash
# simple one-liner
%gor gor #dbsnp# | top 100

# one-liner which outputs to local variable as a pandas dataframe
results = %gor gor #dbsnp# | top 100

# multi-line statement
%%gor 
gor #dbsnp# 
  | top 100

# multi-line statement which writes results into project folder
%%gor user_data/results.gorz <<
gor #dbsnp# 
  | top 100

# output results to local variable as a pandas dataframe
%%gor myvar <<
gor #dbsnp# 
  | top 100

# read from a pandas dataframe in a local variable
%%gor
gor [var:myvar] 
  | top 100

# reference a local variable
num = 10
%%gor
gor [var:myvar] 
  | top $num

```