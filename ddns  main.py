import urllib.request
import json
import time

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
temp_ip=urllib.request.urlopen('https://ident.me').read().decode('utf8')

def ip_to_cname(external_ip):
    #you need to change your conversion rules here
    ip_in_ddns="pool-"
    for c in external_ip:
        if c!=".":
            ip_in_ddns=ip_in_ddns+c
        else:
            ip_in_ddns=ip_in_ddns+"-"

    
    ip_in_ddns=ip_in_ddns+".cpe.net.cable.rogers.com"
    print(ip_in_ddns)
    return ip_in_ddns

while(1):
    time.sleep(10)
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print(external_ip)
    if(temp_ip!=external_ip):
        print(temp_ip)
        temp_ip=external_ip
        print("execute ip change")
        ip_in_ddns=ip_to_cname(external_ip)

        #change your key and password here
        client = AcsClient('KEY', 'PSSWD', 'cn-hangzhou')

        record=DescribeSubDomainRecordsRequest()
        
        #change to your subdomain here
        record.set_SubDomain("imaginepilot.xyz")

        rec=client.do_action_with_exception(record);
        rec=rec.decode('utf8').replace("'", '"')
        print(rec)
        rec=json.loads(rec)
        print(rec)
        rec=rec["DomainRecords"]["Record"][0]["RecordId"]
        print(rec)
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_Value(ip_in_ddns)
        request.set_Type("CNAME")
        request.set_RR("@")
        request.set_RecordId(rec)

        response = client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))