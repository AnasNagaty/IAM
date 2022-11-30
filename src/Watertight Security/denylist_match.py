import json
import boto3
import hashlib

def match_hashlist(filehash):  
    s3_client = boto3.client('s3')
    s3_clientobj = s3_client.get_object(Bucket='denylist-hashfile-upload-275f5670', Key='hashlist.txt')
    hashlist = s3_clientobj['Body'].read().decode('utf-8')
    hashlist = hashlist.strip()
    if filehash in hashlist.split('\n'):
        return True
def parse_sqs(event):
    buc = ''
    key = ''
    print("Print events",event)
    for each in event['Records']:
        data = json.loads(each['body'])
        print("Print data",data)
        buc = data['Records'][0]['s3']['bucket']['name']
        key = data['Records'][0]['s3']['object']['key']
    return buc, key
def lambda_handler(event, context):
    print(event)
    print(type(event))
    bucket, key = parse_sqs(event)
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    body = obj.get()['Body'].read()
    hashvalue = hashlib.sha256(body).hexdigest()
    if match_hashlist(hashvalue) is True:
        print("matched for existing hash", hashvalue)
    else:
        print("no matching hash ")
