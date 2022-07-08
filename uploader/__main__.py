import os
import sys
import requests
import subprocess

from utils import get_logger
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder

DEVICE_TYPE = os.getenv('DEVICE_TYPE', default=None)
RELEASE = os.getenv('RELEASE', default=None)
UPDATE_MODULE = os.getenv('UPDATE_MODULE', default=None)
DEVICE_GROUP = os.getenv('DEVICE_GROUP', default=None)
FILES = os.getenv('FILES', default=None)

MENDER_AUTH_USERNAME = os.getenv('MENDER_AUTH_USERNAME', default=None)
MENDER_AUTH_PASSWORD = os.getenv('MENDER_AUTH_PASSWORD', default=None)
MENDER_SERVER_URL = os.getenv('MENDER_SERVER_URL', default=None)

def get_jwt() -> str:
    auth_response = requests.post(f'{MENDER_SERVER_URL}/api/management/v1/useradm/auth/login', verify=False, auth=HTTPBasicAuth(MENDER_AUTH_USERNAME, MENDER_AUTH_PASSWORD))
    if auth_response.status_code == 200:
        return auth_response.text
    else:
        raise ValueError('error: Mender credentials invalid.')

def generate_mender_artifact() -> None:
    try:
        subprocess.run(f"""
            mender-artifact write module-image \
                -t "{DEVICE_TYPE}" \
                -n "{RELEASE}" \
                -T "{UPDATE_MODULE}" \
                -o "{RELEASE}.mender" \
                -g {DEVICE_GROUP} \
                {" ".join(["-f " + i for i in FILES.split(",")])}
        """, shell=True)

    except Exception as e:
        raise ValueError('error: Failed to create a Mender artifact', e)

def upload_mender_artifact(artifact_name: str, auth_token: str) -> None:
    try:
        artifact = open(f'./{artifact_name}', 'rb')

        mp_encoder = MultipartEncoder(
            fields={
                'artifact': (artifact_name, artifact, 'text/plain'),
            }
        )

        uploader_response = requests.post(
            f'{MENDER_SERVER_URL}/api/management/v1/deployments/artifacts',
            data=mp_encoder,
            headers={
                'Content-Type': mp_encoder.content_type,
                'Authorization': f'Bearer {auth_token}'
            }
        )

        if uploader_response.status_code != 201:
            raise ValueError(uploader_response.content)
    except Exception as e:
        raise ValueError('error: Failed to upload artifact to Mender.', e)

def main() -> None:
    logger = get_logger()

    try:
        for env_var in [FILES, DEVICE_TYPE, RELEASE, UPDATE_MODULE, DEVICE_GROUP, MENDER_AUTH_USERNAME, MENDER_AUTH_PASSWORD, MENDER_SERVER_URL]:
            if env_var is None:
                raise ValueError('error: Required environment variables must be set.')
        
        artifact_name = f"{RELEASE}.mender"

        jwt = get_jwt()
        logger.info('success: Authenticated against Mender management server...')

        generate_mender_artifact()
        logger.info('success: Mender artifact created...')
        
        logger.info('info: Attempting to upload Mender artifact to Mender...')
        upload_mender_artifact(artifact_name, jwt)
        logger.info(f'success: Artifact {artifact_name} has been uploaded to Mender!')
        return 0
    except ValueError as e:
        logger.error(e)
        return 1

if __name__ == '__main__':
    sys.exit(main())