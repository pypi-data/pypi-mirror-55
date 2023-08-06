# Lumber-Cloud

Lumber is a cloud service for logs

## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install lumber-cloud.

```bash
pip install lumber-cloud
```

## Usage

Import the lumber_cloud module and initialize it with your app token.

```python
from lumber_cloud import Lumber

lumber = Lumber('your_app_token')
```

Create some logs with one of six levels.

```python
lumber.info('info')
lumber.debug('debug')
lumber.verbose('verbose')
lumber.warning('warning')
lumber.error('error')
lumber.critical('critical')
```

Optionally send stringified 'code' to any of the lumber methods.

```python
lumber.info('info', json.dumps({ key: 'value' }, null, 2))
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
