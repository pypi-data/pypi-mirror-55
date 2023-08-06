# -*- coding=utf-8

import os

class _GossClientBase(object):

    def _join_path(self, a, b):
        if a:
            return a + '/' + b
        return b

    def upload_file(self, local_path, cloud_path):
        """
        Upload file to cloude
        """
        if not os.path.exists(local_path):
            return '', 'File `{file}` does not exist'.format(file=local_path)
        return self._upload_file(local_path, cloud_path)

    def _upload_file(self, local_path, cloud_path):
        raise NotImplementedError()
