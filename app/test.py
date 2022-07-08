import os
import time

import boto3

linode_obj_config = {
    "aws_access_key_id": os.environ.get("S3_KEY"),
    "aws_secret_access_key": os.environ.get("S3_SECRET_KEY"),
    "endpoint_url": "https://cdn.doublel.studio/",
}

for key in linode_obj_config.keys():
    print(f"{key} : {linode_obj_config[key][:-1]} {linode_obj_config[key][-1]}")

client = boto3.client("s3", **linode_obj_config)

response = client.list_buckets()
for bucket in response["Buckets"]:
    print(bucket["Name"])

time.sleep(10)
