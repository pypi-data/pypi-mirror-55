# envvarconf
Safe app configuration from environment variables without extra dependencies

# Example
Define our settings
```python3
from envvarconf import BaseSettings


class Settings(BaseSettings):
    SENTRY_DSN: str
    LOGGING_LEVEL: str = 'debug'

    HOST: str
    PORT: int


if __name__ == "__main__":
    settings = Settings(envvar_prefix='EVC')
    settings.load()

    print("OK!")
    print(settings)
```

Run application without any environment definition
```python3
$ python3 main.py
There is errors in settings
 * SENTRY_DSN is not defined
 * HOST is not defined
 * PORT is not defined

Application settings:
SENTRY_DSN(EVC_SENTRY_DSN) <class 'str'> = NOT DEFINED!
LOGGING_LEVEL(EVC_LOGGING_LEVEL) <class 'str'> = debug
HOST(EVC_HOST) <class 'str'> = NOT DEFINED!
PORT(EVC_PORT) <class 'int'> = NOT DEFINED!
```

Define EVC_PORT variable:
```
$ EVC_PORT=1 python3 main.py
There is errors in settings
 * SENTRY_DSN is not defined
 * HOST is not defined

Application settings:
SENTRY_DSN(EVC_SENTRY_DSN) <class 'str'> = NOT DEFINED!
LOGGING_LEVEL(EVC_LOGGING_LEVEL) <class 'str'> = debug
HOST(EVC_HOST) <class 'str'> = NOT DEFINED!
PORT(EVC_PORT) <class 'int'> = 1
```

Define all variables
```
$ EVC_SENTRY_DSN=testing EVC_HOST=localhost EVC_PORT=80 python3 main.py
OK!
<Settings SENTRY_DSN=testing, LOGGING_LEVEL=debug, HOST=localhost, PORT=80>
```
# envvarconf
