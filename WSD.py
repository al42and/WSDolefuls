#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import argparse
import email
import requests
import time
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser(description='Make Canon MG3040 scan')
parser.add_argument('-H', nargs=1, required=True, help='Scanner ip/hostname')
parser.add_argument('-j', nargs='?', required=False, type=int, help='Retrieve specific job instead of making a new one')
parser.add_argument('-o', nargs=1, required=True, help='Output image file')

args = parser.parse_args()
host, jobid, output = args.H[0], args.j, args.o[0]
print (host, jobid, output)

URL='http://{}:80/wsd/scanservice.cgi'.format(host)

def post_req(fname, **kwargs):
    headers = {'content-type': 'application/soap+xml'}
    req = ''.join(open(fname).readlines())
    for k in kwargs:
        req = req.replace('{{'+k+'}}', str(kwargs[k]))
    return requests.post(URL,data=req,headers=headers)

def parse_multipart(resp):
    content_with_header = b'Content-type: ' + resp.headers['Content-Type'].encode('ascii') + resp.content
    m = email.message_from_bytes(content_with_header)
    return list(m.walk())

def submit_job():
    ret = post_req('submit_job.xml', URL=URL).content
    xml = ET.fromstring(ret)
    jobid = xml.find('{http://www.w3.org/2003/05/soap-envelope}Body').\
                find('{http://schemas.microsoft.com/windows/2006/08/wdp/scan}CreateScanJobResponse').\
                find('{http://schemas.microsoft.com/windows/2006/08/wdp/scan}JobId').\
                text
    return jobid

def request_image(jobid):
    ret = post_req('request_image.xml', URL=URL, JOBID=jobid)
    ret_parts = parse_multipart(ret)
    for part in ret_parts:
        if part.get_content_type() == 'image/jpeg':
            return part.get_payload(decode=True)
    raise Exception('Can not parse response')


if jobid is None:
    # Submit new job
    jobid = submit_job()
    print ('Submitted job', jobid, ', waiting for reply...')

image_data = request_image(jobid)
open(output, 'wb').write(image_data)

