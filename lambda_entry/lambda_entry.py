import boto3

from util import b64string_to_image_bytes

s3 = boto3.resource("s3")


def lambda_handler(event, context):
    for key in ['file_name', 'file', 'file_type']:
        if key not in event:
            print("bad key:", key)
            raise ValueError(f"not a valid request.")
    bucket = s3.Bucket("test0-ranxiao")
    o = bucket.put_object(Key=event['file_name'], Body=b64string_to_image_bytes(event['file']))
    return {
        'statusCode': 200,
        'body': {"message": str(o)}
    }