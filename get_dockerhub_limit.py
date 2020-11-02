#!/usr/bin/env python

# NOTE: Each run of this script decreases the remaining limit by 1 
#
# From https://docs.docker.com/docker-hub/download-rate-limit/#how-can-i-check-my-current-rate
#
# > Remember that these headers are best-effort and there will be small variations.

# pip3 install -r requirements.txt
import sys
import os
import traceback
import requests
from signal import signal, alarm, SIGALRM
from argparse import ArgumentParser

VERSION = '0.0.1'

class DockerHubError(Exception):
	pass

def _alarm_handler(signum, frame):
	raise DockerHubError('Timeout exceeded.')

class DockerHub(object):
    def __init__(self, verbose, username, password):
        self.repository = 'ratelimitpreview/test'
        self.token_url = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:' + self.repository + ':pull'
        self.registry_url = 'https://registry-1.docker.io/v2/' + self.repository + '/manifests/latest'
        self.username = ''
        self.password = ''

        self.verbose = verbose

    def limit_extractor(self, str_raw):
        if self.verbose:
            print("Extracting limit from string: " + str_raw)
        if ";" in str_raw:
            split_arr = str_raw.split(';') # TODO: return other values too?
            if len(split_arr) > 0:
                return split_arr[0]
        else:
            return str_raw

    def get_token(self):
        # User has passed in own credentials, or we need anonymous access.
        if self.username and self.password:
            r_token = requests.get(self.token_url, auth=(self.username, self.password))
        else:
            r_token = requests.get(self.token_url)

        # error handling
        r_token.raise_for_status()

        resp_token = r_token.json()

        if self.verbose:
            print(resp_token)

        token = resp_token.get('token')

        if not token:
            raise Exception('Cannot obtain token from Docker Hub. Please try again!')

        return token

    ## Test against registry
    def get_registry_limits(self):
        headers_registry = { 'Authorization': 'Bearer ' + self.get_token() }

        r_registry = requests.get(self.registry_url, headers=headers_registry)

        # error handling
        r_registry.raise_for_status()

        # We need to check the response headers!
        resp_headers = r_registry.headers

        if self.verbose:
            print(resp_headers)

        if "RateLimit-Limit" in resp_headers and "RateLimit-Remaining" in resp_headers:
            limit = self.limit_extractor(resp_headers["RateLimit-Limit"])
            remaining = self.limit_extractor(resp_headers["RateLimit-Remaining"])

            print("Docker Hub registry limit " + limit + " with remaining pulls " + remaining)
            return (limit, remaining)

        else:
            #raise Exception('Cannot fetch Docker Hub registry limits')
            print("Seems no limit apply. Using a registry proxy already?")
            return (0, 0)

def main():
    parser = ArgumentParser(description="get_dockerhub_limits (Version: %s)" % (VERSION))

    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument("-t", "--timeout", help="Timeout in seconds (default 10s)", type=int, default=10)
    args = parser.parse_args(sys.argv[1:])

    verbose = args.verbose

    signal(SIGALRM, _alarm_handler)
    alarm(args.timeout)

    # TODO: Test and document
    username = os.environ.get('DOCKER_USERNAME')
    password = os.environ.get('DOCKER_PASSWORD')

    dh = DockerHub(verbose, username, password)

    dh.get_registry_limits()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print("UNKNOWN - Error: %s" % (e))
        sys.exit(3)
