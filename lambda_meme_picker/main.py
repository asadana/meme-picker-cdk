import json
import os
import urllib.request

import boto3

from PIL import Image, UnidentifiedImageError

s3 = boto3.resource('s3')
bucket_name = os.getenv('S3_BUCKET_NAME')

FILE_NAME = '/tmp/meme-of-the-week.jpg'


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    path, _ = urllib.request.urlretrieve('https://i.pinimg.com/originals/4a/32/fb/4a32fbcba40cc06ea6ca0edbd4dbae1c.png')

    try:
        with open(path, 'rb') as image_file:
            image = Image.open(image_file)

            # next 3 lines strip exif
            image_data = list(image.getdata())
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(image_data)

            image_without_exif.convert('RGB')
            image_without_exif.save(FILE_NAME)

            s3.meta.client.upload_file(FILE_NAME, bucket_name, 'meme-of-the-week.jpg',
                                       ExtraArgs={
                                           "ACL": "public-read"
                                       })
    except UnidentifiedImageError:
        print("The image download was unsuccessful.")

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit '
    }
