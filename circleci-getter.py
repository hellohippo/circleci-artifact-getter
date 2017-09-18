#!/usr/bin/env python

"""
CLI tool for retrieving artifacts from CircleCI

Usage:
  circleci-getter [--debug] --user=USER --project=PROJECT [--branch=BRANCH] [--filter=FILTER]
  [--out=OUT] [--token=TOKEN]

Options:
  --debug           Print debug info
  --help            Print this message
  --user=USER       GitHub organisation name or user name
  --project=PROJECT GitHub project name 
  --branch=BRANCH   Branch from where to get artifacts. [default: master]
  --filter=FILTER   Get only files that match provided filter (use Python re format) [default: .*]
  --out=OUT         Directory to put downloaded artifacts to [default: out]
  --token=TOKEN     Env var name to read CircleCI API token from [default: TOKEN]
"""

from docopt import docopt
import requests
import copy
import json
import logging
import os
import re

BASE_URL = 'https://circleci.com/api/v1.1/project/github'

def get_options(args):
    result = {}
    for key, value in args.items():
        result[key.lstrip('--')] = value
    logging.debug('Extracted options: {}'.format(result))
    return result

def get_token(token_name):
    if token_name in os.environ:
        return os.environ[token_name]
    raise EnvironmentError('Can not read env variable {}'.format(args['--token']))

def send_request(url, params):
    headers = {'Accept': 'application/json'}
    result = requests.get(url, params = params, headers = headers)
    if result.status_code == 200:
        return result
    else:
        raise IOError('Received code {}: {}'.format(result.status_code, result.text))   

def get_build_number(base_url, branch, token):
    logging.info('Getting latest successful build on {}'.format(branch))
    params = {'circle-token': token, 'limit': 1, 'filter': 'successful'}
    url = '{}/tree/{}'.format(base_url, branch)
    latest_build = send_request(url, params)
    latest_build_json = json.loads(latest_build.text)
    return latest_build_json[0]['build_num']

def get_artifacts_url_as_list(base_url, build_number, artifact_filter, token):
    logging.info('Look up artifacts url for build number #{} ...'.format(build_number))
    params = {'circle-token': token}
    url = '{}/{}/artifacts'.format(base_url, build_number)
    artifacts = send_request(url, params)
    result = []
    for artifact in json.loads(artifacts.text):
        # If matches then return it
        if re.match(artifact_filter, artifact['path']):
            result.append(artifact['url'])
    return result

def download_files(urls, out, token):
    logging.info('Downloading files to {} ...'.format(out))
    params = {'circle-token': token}
    if not os.path.exists(out):
        try:
            os.makedirs(out)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    for url in urls:
        rsp = send_request(url, params)
        with open(os.path.join(out, os.path.basename(url)), "w") as f:
            f.write(rsp.text)
            logging.info('Wrote {}'.format(f.name))

def main():
    arguments = docopt(__doc__)

    if arguments['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    token = get_token(arguments['--token'])
    options = get_options(arguments)
    url = '{}/{}/{}'.format(BASE_URL, options['user'], options['project'])

    build_number = get_build_number(url, options['branch'], token)

    logging.info('Latest successful build on {} is #{}'.format(options['branch'], build_number))

    artifacts_url_list = get_artifacts_url_as_list(url, build_number, options['filter'], token)

    logging.info('Got the following URLs: {}'.format(artifacts_url_list))

    download_files(artifacts_url_list, options['out'], token)

if __name__ == "__main__":
    main()



"""
base_payload = {'circle-token': '214bed4d74229d31da1b4ab0f8490361b59a19bf'}
headers = {'Accept': 'application/json'}
base_url = 'https://circleci.com/api/v1.1/project/github/transisland/platform'
branch = 'staging'

# Get latest build for the staging branch
print 'Getting latest successful build on {}'.format(branch)
latest_build_payload = copy.copy(base_payload)
latest_build_payload['limit'] = 1
latest_build_payload['filter'] = 'successful'
latest_build_url = '{}/tree/{}'.format(base_url, branch)
print latest_build_payload
print latest_build_url
latest_build = requests.get(latest_build_url,
                            params = latest_build_payload,
                            headers = headers)

latest_build_json = json.loads(latest_build.text)
latest_build_number = latest_build_json[0]['build_num']
print 'Latest successful build on {} is #{}: {}'.format(branch, latest_build_number, latest_build_json[0]['build_url'])
print 'Look up artifacts url...'
build_artifacts_url = '{}/{}/artifacts'.format(base_url, latest_build_number)
build_artifacts = requests.get(build_artifacts_url,
                               params = base_payload,
                               headers = headers)

for artifact in json.loads(build_artifacts.text):
  print artifact['url']
"""
'''

rsp = requests.get('https://circleci.com/api/v1.1/project/github/transisland/platform/latest/artifacts', params=payload)
print 'text ' + rsp.text
print json.loads(rsp.text)
if rsp.status_code == 200:
  logging.info(rsp.json())
else:
  logging.error(rsp.status_code)



'''
