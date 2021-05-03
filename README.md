# Yirgachefe
A library for the convenience of configuring environment variables, configuration files, and logger.

## Prerequisite
- Python 3.7.x

## Quick start
The configuration file format is JSON, and the default location is [CWD]/configure.json.
* CWD: Current working directory (you can get it with 'os.getcwd()')

### Example configure.json
```json
{
  "API_PORT": 8100,
  "STORAGE_ID": "storage_1"
}
```

### Example Code
```python
from yirgachefe import config, logger

logger.debug(config['API_PORT'])
logger.info(config.API_PORT)

config['NEW'] = 'new value'
config.NEW2 = 'new value2'
```

## Custom Usage

### Default configure.json.
* This value is set internally and is used even if the file doesn't exist.
* You can use the changed value by explicitly setting it in the file.
```json
{
  "debug": false,
  "log_level": "WARNING",
  "log_format": "%(asctime)s,%(msecs)03d %(process)d %(thread)d %(levelname)s %(filename)s(%(lineno)d) %(message)s",
  "encoding": "utf-8"
}
```
* debug: Set stream handler to logging with coloredlog.
* log_level: Log level for logging.
* log_format: Log format for logging.
* encoding: The encoding value used when saving the configuration file with Yirgachefe.
