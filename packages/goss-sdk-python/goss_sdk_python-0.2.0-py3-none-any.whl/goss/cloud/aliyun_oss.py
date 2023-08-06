# -*- coding=utf-8

from oss2 import Auth, Bucket
from oss2.compat import urlunquote

from .base import _GossClientBase

class GossAliyunOSSClient(_GossClientBase):

    def __init__(self, secret_id, secret_key, region, bucket):
        """
        Initialize client
        """
        self._region = region
        self._bucket = bucket
        self._client = Bucket(
            auth=Auth(secret_id, secret_key),
            endpoint='http://{region}.aliyuncs.com'.format(region=region),
            bucket_name=bucket,
        )

    def _upload_file(self, local_path, cloud_path):
        """
        Upload file to cloude
        """
        try:
            with open(local_path, 'rb') as fileobj:
                self._client.put_object(key=cloud_path, data=fileobj)
        except Exception as err:
            return '', err
        return urlunquote(self._client._make_url(self._bucket, cloud_path)), None
