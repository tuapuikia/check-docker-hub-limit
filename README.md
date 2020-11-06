# Check Docker Hub Limit

This script allows to check the [Docker Hub Limit](https://docs.docker.com/docker-hub/download-rate-limit/#how-can-i-check-my-current-rate).
It does so by querying the registry and parsing the response header.

> **Note**
>
> Every script execution decreases the remaining pull count!

## Requirements

* Python 3 with the requests library

## Installation

```
apt install python3 python3-pip

pip3 install -r requirements.txt
```

## Usage

```
usage: check_docker_hub_limit.py [-h] [-w WARNING] [-c CRITICAL] [-v] [-t TIMEOUT]

Version: 1.0.0

optional arguments:
  -h, --help            show this help message and exit
  -w WARNING, --warning WARNING
                        warning threshold for remaining
  -c CRITICAL, --critical CRITICAL
                        critical threshold for remaining
  -v, --verbose         increase output verbosity
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds (default 10s)
```

### Docker Hub Authentication

In case you want to use your own username and password credentials for hub.docker.com,
you need to export them into the environment.

```
export DOCKERHUB_USERNAME='xxx'
export DOCKERHUB_PASSWORD='xxx'
```

You can verify the credentials in use with passing the `--verbose` parameter and checking
for this message:

```
Notice: Using Docker Hub credentials for 'dnsmichi'
```

On macOS you can use Oh My Zsh and the [dotenv plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/dotenv)
to automatically source `$HOME/.env`.

### Examples

```
$ python3 check_docker_hub_limit.py
OK - Docker Hub: Limit is 5000 remaining 4997|'limit'=5000 'remaining'=4997
```

```
$ python3 check_docker_hub_limit.py -w 10000 -c 3000
WARNING - Docker Hub: Limit is 5000 remaining 4999|'limit'=5000 'remaining'=4999
```

```
$ python3 check_docker_hub_limit.py -w 10000 -c 5000
CRITICAL - Docker Hub: Limit is 5000 remaining 4998|'limit'=5000 'remaining'=4998
```

## Monitoring Integration

You can use this script in your Nagios/Icinga/Naemon/Sensu/etc. monitoring environments.
It implements the [Monitoring Plugins API](https://www.monitoring-plugins.org/doc/guidelines.html)
and returns performance data metrics.


