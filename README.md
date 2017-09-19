# circleci-artifact-getter

# Intro

Utility to download artifacts from CircleCI builds

```
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
```

Note! Script at this moment script only works with text files as artifacts

# Examples

```
source setup.sh
export TOKEN=circleciapitoken
python circleci-getter.py --debug --user transisland --project platform --branch develop --filter '.*/deployments/.*'
```

```
python circleci-getter.py --user transisland --project platform --branch develop --filter '.*/deployments/.*'
Getting latest successful build on develop
Latest successful build on develop is #2411
Look up artifacts url for build number #2411 ...
Got the following URLs: [u'https://2411-76292669-gh.circle-artifacts.com/0/home/ubuntu/platform/deployments/deployment.yml', u'https://2411-76292669-gh.circle-artifacts.com/0/home/ubuntu/platform/deployments/deployment.yml%253D']
Downloading files to out ...
Wrote out/deployment.yml
Wrote out/deployment.yml%253D
```

# Build executable

```
source setup.sh
pyinstaller --onefile circleci-getter.py
dist/circleci-getter -h
```

# Get executable

```
curl -L -O https://github.com/transisland/circleci-artifact-getter/releases/download/0.0.1/circleci-getter-linux
chmod u+x circleci-getter-linux
```
