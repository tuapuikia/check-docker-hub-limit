# Check Docker Hub Limit

This script allows to check the [Docker Hub Limit](https://docs.docker.com/docker-hub/download-rate-limit/#how-can-i-check-my-current-rate).
It does so by first obtaining an auth token and then querying the Docker Hub registry with a HEAD request to parse `RateLimit-Limit`, `RateLimit-Remaining` and `RateLimit-Reset`.

You can use your [Docker Hub credentials](#docker-hub-authentication) to authenticate, otherwise an anonymous token is used. 

This script implements the [Monitoring Plugins API specification](https://www.monitoring-plugins.org/doc/guidelines.html) and provides state output, performance data metrics and exit states for integration into existing monitoring environments. 

## Requirements

* Python 3 with the requests library 

## Installation

### Debian/Ubuntu

```shell
apt-get update

apt -y install python3 python3-pip

pip3 install -r requirements.txt
```

### RHEL/CentOS/Fedora

```shell
yum makecache

yum -y install python3 python3-pip

pip3 install -r requirements.txt
```

### SLES/OpenSUSE

```shell
zypper ref

zypper in -y python3 python3-pip

pip3 install -r requirements.txt
```

### ArchLinux

```shell
pacman -Sy --noconfirm python python-pip

pip install -r requirements.txt
```

### macOS

```shell
brew install python3 

pip3 install -r requirements.txt
```

## Usage

```
usage: check_docker_hub_limit.py [-h] [-w WARNING] [-c CRITICAL] [-v] [-t TIMEOUT]

Version: 2.0.0

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

Run the script to fetch the current remaining count. The plugin script exit code returns `0` being OK.

```
$ python3 check_docker_hub_limit.py
OK - Docker Hub: Limit is 5000 remaining 4997|'limit'=5000 'remaining'=4997

$ echo $?
0
```

Specify the warning threshold with `10000` pulls, and the critical threshold with `3000`.
The example shows how the state changes to `WARNING` with a current count of `4999` remaining
pull requests. The plugin script exit code changes to `1`.

```
$ python3 check_docker_hub_limit.py -w 10000 -c 3000
WARNING - Docker Hub: Limit is 5000 remaining 4999|'limit'=5000 'remaining'=4999

$ echo $?
1
```

Specify a higher critical threshold with `5000`. When the remaining count goes below this value,
the plugin script returns `CRITICAL` and changes the exit state into `2`.

```
$ python3 check_docker_hub_limit.py -w 10000 -c 5000
CRITICAL - Docker Hub: Limit is 5000 remaining 4998|'limit'=5000 'remaining'=4998

$ echo $?
2
```

When a timeout is reached, or another error is thrown, the exit state switches to `3` and the output state becomes `UNKNOWN`.

## Monitoring Integration

You can use this script in your Nagios/Icinga/Naemon/Sensu/etc. monitoring environments.
It implements the [Monitoring Plugins API](https://www.monitoring-plugins.org/doc/guidelines.html)
and returns performance data metrics. 

## Development

Mount the source into the Docker environment. 

```
docker run -ti -v `pwd`:/mnt centos bash
```

```
docker run -ti -v `pwd`:/mnt opensuse/leap bash
```

```
docker run -ti -v `pwd`:/mnt archlinux bash
```

