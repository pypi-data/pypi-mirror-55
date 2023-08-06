# -*- coding=utf-8

from obs import ObsClient

from .base import _GossClientBase

class GossHuaweicloudOBSClient(_GossClientBase):

    def __init__(self, secret_id, secret_key, region, bucket):
        """
        Initialize client
        """
        self._region = region
        self._bucket = bucket
        self._client = ObsClient(
            access_key_id=secret_id,
            secret_access_key=secret_key,
            server='https://obs.{region}.myhuaweicloud.com'.format(region=region),
        )

    def _upload_file(self, local_path, cloud_path):
        """
        Upload file to cloude
        """
        try:
            resp = self._client.putFile(bucketName=self._bucket, objectKey=cloud_path, file_path=local_path)
            if resp.status > 300:
                raise ValueError('Upload file error: {err}'.format(err=resp.errorMessage))
        except Exception as err:
            return '', err
        return resp.body['objectUrl'], None
