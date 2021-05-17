import json
import os
import random
import urllib.request

import boto3

from PIL import Image, UnidentifiedImageError
from google_images_download import google_images_download

s3 = boto3.resource('s3')
bucket_name = os.getenv('S3_BUCKET_NAME')

FILE_NAME = '/tmp/meme-of-the-week.jpg'

SEARCH_PARAMS = {
    "keywords": "\"timecard\" meme",
    "limit": 50,
    "format": "jpg",
    "language": "English",
    "safe_search": True,
    "no_download": True,
    "silent_mode": True
}


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    if event and 'meme' in event.keys():
        image_url = event['meme']
    else:
        image_url = _pick_image()
    print(f"Picking image: {image_url}")

    path, _ = urllib.request.urlretrieve(image_url)

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


def _pick_image() -> str:
    google_images_instance = google_images_download.googleimagesdownload()
    paths = google_images_instance.download(SEARCH_PARAMS)

    print(f"Output of the _pick_image: {paths}")

    path_list = list(paths[0].values())[0]

    # pick a random number to pick an image
    index = random.randint(0, len(path_list))

    return path_list[index]
