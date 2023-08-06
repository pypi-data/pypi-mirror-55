# -*- coding=utf-8

from boto3 import Session

from .base import _GossClientBase

class GossAmazonS3Client(_GossClientBase):

    RESOURCE_URI_FORMAT = 'https://{bucket}.s3-{region}.amazonaws.com/{path}'

    def __init__(self, secret_id, secret_key, region, bucket):
        """
        Initialize client
        """
        self._region = region
        self._bucket = bucket
        self._client = Session(
            aws_access_key_id=secret_id,
            aws_secret_access_key=secret_key,
            region_name=region,
        ).resource('s3').Bucket(bucket)

    def _upload_file(self, local_path, cloud_path):
        """
        Upload file to cloude
        """
        try:
            with open(local_path, 'rb') as fileobj:
                self._client.put_object(Key=cloud_path, Body=fileobj)
        except Exception as err:
            return '', err
        return self.RESOURCE_URI_FORMAT.format(bucket=self._bucket, region=self._region, path=cloud_path), None
