#!python
#! -*- coding:utf-8-*-

"""
Set of tools to work with AWS

We assume that ~/.aws/credentials exists and is formatted like::

  aws_access_key_id = SECRETKEY
  aws_secret_access_key = SECRETKEY

We walk a set of files, and we remove rootpath, because we want the bucket to start / 
at the point of rootpath.

TODO: make more robust, build a verification routine to check once uploaded
TODO: upload based on git rev

"""


import os
import boto3
from botocore.exceptions import ClientError
from mimetypes import MimeTypes



def upload_file(bucket_name,filePath):
    """upload file to bucket, and alter metadata
    stolen from http://www.lambdatwist.com/s3-hosting-guide/
    """
    session = boto3.Session()
    client = session.client('s3')
    s3 = session.resource('s3')
    destname = filePath.replace(rootpath, '')
    try:                 
        data = open(filePath, 'rb')
        ftype, encoding = MimeTypes().guess_type(filePath)
        conType = ftype if ftype is not None else encoding if encoding is not None else 'text/plain'    
        s3.Object(bucket_name, destname).put(Body=data,ContentType=conType,ACL='public-read')
    except ClientError as err:
        print("Failed to upload artefact to S3.\n" + str(err))
        return False
    except IOError as err:
        print("Failed to access artefact in this directory.\n" + str(err))
        return False   
    return True


def walk_files(rootpath, targetbucket):
    """
    """
    print('walking {}'.format(rootpath))
    for dirpath, folders, _files in os.walk(rootpath, followlinks=True):
        files = [os.path.join(dirpath, f) for f in _files]
        for folderpath in folders:
            remote_mkdir(folderpath, targetbucket)
        for filepath in files:
            remote_put_file(filepath, targetbucket)
            
def remote_mkdir(folderpath, targetbucket):
    """
    """
    print('execute boto command to mk {} on {}'.format(folderpath, targetbucket))
    
def remote_put_file(filepath, targetbucket):
    print('boto put {} on {}'.format(filepath, targetbucket))
    upload_file(targetbucket, filepath)
          
def upload_files_to_s3(rootpath, tgtbucket):
    """
    """

    walk_files(rootpath, tgtbucket)

if __name__ == '__main__':
#    rootpath = '/home/pbrian/projects/hackermews/src/'
#    targetbucket = 'hackermews.org'

    
    rootpath = '/var/projects/devmanual/docs/_build/html/'
    targetbucket = 'thesimplecto.com'
    
    upload_files_to_s3(rootpath, targetbucket)
