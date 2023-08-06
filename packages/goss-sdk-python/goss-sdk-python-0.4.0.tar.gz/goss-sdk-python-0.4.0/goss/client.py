# -*- coding=utf-8

import os

import boto3 as amazon_s3
import qcloud_cos as tencent_cos
import oss2 as aliyun_oss
import obs as huaweicloud_obs

from .exception import GossException
from .comm import *

from .cloud import *

class GossClient(object):

    CLIENT_SUPPORTED_MAP = {
        GOSS_AMAZON_S3: GossAmazonS3Client,
        GOSS_TENCENT_COS: GossTencentCOSClient,
        GOSS_ALIYUN_OSS: GossAliyunOSSClient,
        GOSS_HUAWEICLOUD_OBS: GossHuaweicloudOBSClient,
    }
    
    def __init__(self, ctype, secret_id, secret_key, region, bucket):
        """
        Initialize client
        """
        if ctype not in self.CLIENT_SUPPORTED_MAP:
            raise GossException("OOS type about '{type}' does not supported".format(type=ctype))
        self._client = self.CLIENT_SUPPORTED_MAP[ctype](secret_id, secret_key, region, bucket)

    def upload_file(self, local_path, cloud_path):
        """
        Upload file to cloude
        """
        return self._client.upload_file(local_path, cloud_path)