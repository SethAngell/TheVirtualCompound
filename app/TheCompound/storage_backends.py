from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "static"
    AWS_DEFAULT_ACL = "public-read"


class PublicMediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    AWS_DEFAULT_ACL = "public-read"
