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
```
