import json
import os
import urllib.request

import boto3

s3 = boto3.resource('s3')
bucket_name = os.getenv('S3_BUCKET_NAME')


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    urllib.request.urlretrieve('https://www.memecreator.org/static/images/memes/4185030.jpg',
                               '/tmp/meme-of-the-week.jpg')

    s3.meta.client.upload_file('/tmp/meme-of-the-week.jpg', bucket_name, 'meme-of-the-week.jpg')

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit '
    }
