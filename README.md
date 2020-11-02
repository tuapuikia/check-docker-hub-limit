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
python3 check_docker_hub_limit.py --help
usage: check_docker_hub_limit.py [-h] [-v] [-t TIMEOUT]

get_dockerhub_limits (Version: 0.0.1)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds (default 10s)
```


## Monitoring Integration

You can use this script in your Nagios/Icinga/Naemon/Sensu/etc. monitoring environments.
It implements the Monitoring Plugins API and returns performance data metrics.


