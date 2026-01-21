from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from tempfile import SpooledTemporaryFile
import os

class StaticStorage(S3Boto3Storage):
    location = 'static'
    def _save(self, name, content):
        content.seek(0, os.SEEK_SET)
        with SpooledTemporaryFile() as content_autoclose:

            content_autoclose.write(content.read())
            return super(StaticStorage, self)._save(name, content_autoclose)


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    def _save(self, name, content):
        content.seek(0, os.SEEK_SET)
        with SpooledTemporaryFile() as content_autoclose:

            content_autoclose.write(content.read())
            return super(PublicMediaStorage, self)._save(name, content_autoclose)


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    file_overwrite = False
    custom_domain = False
    def _save(self, name, content):
        content.seek(0, os.SEEK_SET)
        with SpooledTemporaryFile() as content_autoclose:

            content_autoclose.write(content.read())
            return super(PrivateMediaStorage, self)._save(name, content_autoclose)