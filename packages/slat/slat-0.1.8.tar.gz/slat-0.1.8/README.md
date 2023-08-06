# SLaT
**S**imple **La**mbda **T**oolkit

Collection of reusable Python tools for lambda development


## Logging
 [Structlog](http://www.structlog.org/en/stable/index.html) is used for structured JSON logging
 
 ### Usage
```python
import logging
from slat.log_util import LogUtil

log = LogUtil.init_logger(default_level='INFO',  correlation_id_key_val={'request_id': '999'})
log.info('is this JSON: {"answer": 42}')
log.error("the log message", some="value", extra_data=[1, 2, 3, "4"])
# only OUR logger will render as JSON
logging.getLogger("test").warning("hello")
```
output:
```
{"event": "is this JSON: {\"answer\": 42}", "level": "info", "logger": "slat.log_util", "request_id": "999", "timestamp": "2019-11-06T21:04:33.517295Z"}
{"event": "the log message", "extra_data": [1, 2, 3, "4"], "level": "error", "logger": "slat.log_util", "request_id": "999", "some": "value", "timestamp": "2019-11-06T21:04:33.517652Z"}
hello
```

## Developing

### create file .pypirc
```
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository: https://upload.pypi.org/legacy/
username:
password:

[pypitest]
repository: https://test.pypi.org/legacy/
username:
password:
```

### build
```
rm -rf dist
# python setup.py bdist_wheel --universal
python setup.py sdist
```

### pypitest
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install slat --index-url https://test.pypi.org/simple/
```

### pypi
```
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
pip install slat
```