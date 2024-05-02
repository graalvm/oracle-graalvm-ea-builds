import json
import os
import urllib.request
from jsonschema import validate as json_validate
from multiprocessing.pool import Pool


GENERIC_EA_SCHEMA = 'generic-ea-schema.json'
LATEST_EA_JSON = 'latest-ea.json'
LATEST_EA_SCHEMA = 'latest-ea-schema.json'
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCHEMAS_DIR = 'schemas'
VERSIONS_DIR = 'versions'


def validate(json_name, schema_name):
    print(f'Validating {json_name}...')
    with open(os.path.join(ROOT_PATH, VERSIONS_DIR, json_name)) as f:
        json_contents = json.load(f)
    with open(os.path.join(ROOT_PATH, SCHEMAS_DIR, schema_name)) as f:
        schema_contents = json.load(f)
    json_validate(json_contents, schema_contents)
    print(f'  ... validates against {schema_name}')
    if schema_name == LATEST_EA_SCHEMA:
        builds = [json_contents]
    else:
        builds = json_contents
        ensure_one_latest_build(json_name, builds)
    validate_builds(builds)
    print(f'  ... passes sanity checks and all its URLs exist')


def ensure_one_latest_build(json_name, builds):
    num_latest = sum([1 if build['latest'] else 0 for build in builds])
    assert num_latest == 1, f'Expected one latest build in {json_name}, got {num_latest}'


def validate_builds(builds):
    for build in builds:
        version = build['version']
        download_base_url = build['download_base_url']
        files = build['files']
        assert version in download_base_url, f'version not found in download_base_url: {json.dumps(build)}'
        assert all(version in file['filename'] for file in files), f'version not found in all filenames: {json.dumps(build)}'
        check_urls_exist(download_base_url, files)


def check_urls_exist(download_base_url, files):
    with Pool() as pool:
        download_urls = [f'{download_base_url}{file["filename"]}{extension}' for extension in ['', '.sha256'] for file in files]
        pool.map(check_url_exists, download_urls)


def check_url_exists(download_url):
    request = urllib.request.Request(download_url, method='HEAD')
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        assert False, f"Failed to retrieve '{download_url}': {e}"
    assert response.status == 200, f"Expected status code of 200, got {response.status} for '{download_url}'"


if __name__ == '__main__':
    for file_name in os.listdir('versions'):
        assert file_name.endswith('.json'), f"Unexpected non-JSON file '{file_name}'"
        schema_name = LATEST_EA_SCHEMA if file_name == LATEST_EA_JSON else GENERIC_EA_SCHEMA
        validate(file_name, schema_name)
    print('JSON validation successful')
