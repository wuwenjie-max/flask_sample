#!/usr/bin/python
# -*- coding: UTF-8 -*
from minio import Minio

from util.setting import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET_NAME,
)

client = Minio(
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    secure=False,
)


def init_minio(bucket=MINIO_BUCKET_NAME):
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)
        policy = '''
                    {
                        "Version":"%s",
                        "Statement":[
                            {
                                "Effect":"Allow",
                                "Principal":{
                                    "AWS":["*"]
                                },
                                "Action":[
                                    "s3:GetBucketLocation",
                                    "s3:ListBucketMultipartUploads"
                                ],
                                "Resource":[
                                    "arn:aws:s3:::%s"
                                ]
                            },
                            {
                                "Effect":"Allow",
                                "Principal":{
                                    "AWS":["*"]
                                },
                                "Action":[
                                    "s3:AbortMultipartUpload",
                                    "s3:DeleteObject",
                                    "s3:ListMultipartUploadParts",
                                    "s3:PutObject",
                                    "s3:GetObject"
                                ],
                                "Resource":[
                                    "arn:aws:s3:::%s/*"
                                ]
                            }
                        ]
                    }
                    ''' % (
            '2012-10-17',
            bucket,
            bucket,
        )
        client.set_bucket_policy(bucket_name=bucket, policy=policy)


def get_object(object_name, file_path, client=client, bucket=MINIO_BUCKET_NAME):
    return client.fget_object(bucket, object_name, file_path).etag


def put_object(object_name, file_pat, client=client, bucket=MINIO_BUCKET_NAME):
    client.fput_object(bucket, object_name, file_pat)
    public_url = 'http://{}:{}/{}/{}'.format(
        MINIO_ENDPOINT.split(':')[0],
        MINIO_ENDPOINT.split(':')[1],
        bucket,
        object_name,
    )
    return public_url
