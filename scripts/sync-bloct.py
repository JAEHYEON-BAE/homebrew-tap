#!/usr/bin/env python3
"""Sync the public Bloct release using this tap's short-lived Actions token."""
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request

SOURCE = 'JAEHYEON-BAE/bloct'


def update(cask, release, data):
    tag = release['tag_name']
    if release.get('draft') or release.get('prerelease') or not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+', tag):
        raise ValueError('Expected a stable vMAJOR.MINOR.PATCH release')
    assets = [a for a in release['assets'] if a['name'] == 'Bloct.zip']
    if len(assets) != 1:
        raise ValueError('Expected exactly one Bloct.zip asset')
    digest = hashlib.sha256(data).hexdigest()
    if assets[0].get('digest') != 'sha256:' + digest:
        raise ValueError('Downloaded ZIP does not match GitHub asset SHA256')
    text = cask.read_text()
    current = re.search(r'^  version "([0-9]+\.[0-9]+\.[0-9]+)"$', text, re.M)
    if not current:
        raise ValueError('Missing current cask version')
    version = tag[1:]
    if tuple(map(int, version.split('.'))) < tuple(map(int, current[1].split('.'))):
        raise ValueError('Refusing to downgrade the cask')
    text, versions = re.subn(r'^  version "[^"]+"$', f'  version "{version}"', text, flags=re.M)
    text, hashes = re.subn(r'^  sha256 "[0-9a-f]+"$', f'  sha256 "{digest}"', text, flags=re.M)
    if versions != 1 or hashes != 1:
        raise ValueError('Expected one version and one sha256 field')
    if text == cask.read_text():
        print(f'Bloct {version}: already current; ZIP checksum verified')
    else:
        cask.write_text(text)
        print(f'Updated Bloct to {version}; ZIP checksum verified')


def main():
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'bloct-tap-sync'}
    token = os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    request = urllib.request.Request(f'https://api.github.com/repos/{SOURCE}/releases/latest', headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        release = json.load(response)
    tag = release['tag_name']
    if not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+', tag):
        raise ValueError('Unexpected release tag')
    # No authorization header is forwarded to the public release asset/CDN.
    with urllib.request.urlopen(f'https://github.com/{SOURCE}/releases/download/{tag}/Bloct.zip', timeout=60) as response:
        data = response.read()
    update(Path('Casks/bloct.rb'), release, data)


if __name__ == '__main__':
    main()
