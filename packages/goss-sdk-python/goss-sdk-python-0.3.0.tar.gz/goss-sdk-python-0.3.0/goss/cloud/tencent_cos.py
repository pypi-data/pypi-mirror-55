# -*- coding=utf-8

from qcloud_cos import CosS3Client, CosConfig

from .base import _GossClientBase

class GossTencentCOSClient(_GossClientBase):

    def __init__(self, secret_id, secret_key, region, bucket):
        """
        Initialize client
        """
        self._region = region
        self._bucket = bucket
        self._conf = CosConfig(
            Secret_id=secret_id,
            Secret_key=secret_key,
            Region=region,
        )
        self._client = CosS3Client(
            conf=self._conf,
            retry=3,
        )

    def _upload_file(self, local_path, cloud_path):
        """
        Upload file to cloude
        """
        try:
            self._client.upload_file(Bucket=self._bucket, Key=cloud_path, LocalFilePath=local_path)
        except Exception as err:
            return '', err
        return self._conf.uri(bucket=self._bucket, path=cloud_path), None
