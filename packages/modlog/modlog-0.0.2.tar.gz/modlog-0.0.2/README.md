# Modlog



Get module logger with environment variables

[![Build Status](https://travis-ci.org/atomse/modlog.svg?branch=master)](https://travis-ci.org/atomse/modlog)

## Environment variables

modlog using environment variables

If module name: a.b.c, the environment variable is:

* `{A}_LOG_LEVEL`

values are compatible with logging module,
following values are supported:

* notset
* debug
* info
* warning
* error
* critical

```json
{
        50: 'CRITICAL', 
        40: 'ERROR', 
        30: 'WARNING', 
        20: 'INFO', 
        10: 'DEBUG', 
        0: 'NOTSET'
}
```


## Example


```python

import modlog

logger = modlog.getLogger(__name__) # This will read environment variables and set logger level

logger.info("a")

```


