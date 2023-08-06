# -*- coding:utf8 -*-
import requests
import json
from printer import print_list
from color_string import UseStyle

LIST_URL = "/tcpth/list"
REG_ADD_URL = "/tcpth/register/add"
REG_DEL_URL = "/tcpth/register/delete"
TRUST_ADD = "/tcpth/auth/addtrustip"
TRUST_DEL = "/tcpth/auth/rmtrustip"
TRUST_GET = "/tcpth/auth/trustip"

# LIST_KEYS = ['name','local','proxy_port', 'out_connection_count','is_remote_manage',   'write_bytes', 'write_speed', 'read_bytes', 'read_speed']
LIST_KEYS = ['name', 'local', 'proxy_port', 'out_connection_count', 'is_remote_manage', 'write_speed', 'read_speed']
LIST_KEYS_SHOW = ['Name', 'Local Service', 'Proxy Port', 'Out Conn Count', 'Remote Managed', 'Write Speed',
                  'Read Speed']


def get_column_max_len(keys, j_list):
    pass


class Executor:
    def __init__(self, port):
        self.port = port
        self.base_url = "http://localhost:" + str(port)

    def list(self):
        try:
            r = requests.get(self.base_url + LIST_URL)
            # c = r.text.encode('utf8')
            l = json.loads(r.text)
            if len(l) > 0:
                print_list(LIST_KEYS_SHOW, LIST_KEYS, l)

            else:
                print 'no res'
        except Exception, e:
            print e.message

    def get(self, name):
        try:
            name = name.strip()
            r = requests.get(self.base_url + LIST_URL)
            # c = r.text.encode('utf8')
            l = json.loads(r.text)
            # if len(l) > 0:
            name_l = []
            for item in l:
                if item['name'] == name:
                    name_l.append(item)
            print_list(LIST_KEYS_SHOW, LIST_KEYS, name_l)

            # print UseStyle('No result for name: ' + name, fore=red)

        except Exception, e:
            print e.message

    def register(self, cmd):
        pass

    def reg_add(self, client_name, local_service, proxy_port):
        spl_service = local_service.split(':')
        if len(spl_service) != 2:
            return False

        payload = json.dumps({
            "name": client_name,
            "proxy_port": proxy_port,
            "local_host": spl_service[0],
            "local_port": spl_service[1]
        })
        r = requests.post(self.base_url + REG_ADD_URL, data=payload, headers={'content-type': 'application/json'})
        if r.text == 'true':
            print UseStyle('Add Registration Successfully.', fore='green')
        else:
            print UseStyle('Add Registration Failed', fore='red')
        return True

    def reg_rm(self, client_name, proxy_port):
        payload = json.dumps({
            "name": client_name,
            "proxy_port": proxy_port
        })
        r = requests.post(self.base_url + REG_DEL_URL, data=payload, headers={'content-type': 'application/json'})
        if r.text == 'true':
            print UseStyle('Delete Registration Successfully.', fore='green')
        else:
            print UseStyle('Delete Registration Failed', fore='red')
        return True

    def trust_ip_rm(self, client_name, ip):
        r = requests.get(self.base_url + self._get_trust_ip_rm(client_name, ip))
        if r.text == 'true':
            print UseStyle('Delete TrustIp Successfully.', fore='green')
        else:
            print UseStyle('Delete TrustIp Failed', fore='red')
        return True

    def trust_ip_add(self, client_name, ip):
        r = requests.get(self.base_url + self._get_trust_ip_add(client_name, ip))
        if r.text == 'true':
            print UseStyle('Add TrustIp Successfully.', fore='green')
        else:
            print UseStyle('Add TrustIpFailed', fore='red')
        return True

    def trust_ip_rm_by_port(self, client_name, proxy_port, ip):
        r = requests.get(self.base_url + self._get_trust_ip_rm_by_port(client_name, proxy_port, ip))
        if r.text == 'true':
            print UseStyle('Delete TrustIp Successfully.', fore='green')
        else:
            print UseStyle('Delete TrustIp Failed', fore='red')
        return True

    def trust_ip_add_by_port(self, client_name, proxy_port, ip):
        r = requests.get(self.base_url + self._get_trust_ip_add_by_port(client_name, proxy_port, ip))
        if r.text == 'true':
            print UseStyle('Add TrustIp Successfully.', fore='green')
        else:
            print UseStyle('Add TrustIpFailed', fore='red')
        return True

    def trust_ip_get(self, client_name):
        r = requests.get(self.base_url + TRUST_GET + '/' + client_name)
        l = json.loads(r.text)
        keys = l.keys()
        for key in keys:
            wait_print = 'Proxy Port ' + key + ' : \n'
            ips = l[key]
            for ip in ips:
                wait_print += '    ' + ip + '\n'
            print wait_print
        # print l

    def trust_ip_get_by_port(self, client_name, proxy_port):
        r = requests.get(self.base_url + TRUST_GET + '/' + client_name + '/' + proxy_port)
        l = json.loads(r.text)
        print '\n'.join(l)

    def _get_trust_ip_rm(self, client_name, ip):
        return TRUST_DEL + '/' + client_name + '/' + ip

    def _get_trust_ip_add(self, client_name, ip):
        return TRUST_ADD + '/' + client_name + '/' + ip

    def _get_trust_ip_rm_by_port(self, client_name, proxy_port, ip):
        return TRUST_DEL + '/' + client_name + '/' + proxy_port + '/' + ip

    def _get_trust_ip_add_by_port(self, client_name, proxy_port, ip):
        return TRUST_ADD + '/' + client_name + '/' + proxy_port + '/' + ip


if __name__ == '__main__':
    e = Executor(8080)
    # e.trust_ip_add("wls", "1.1.1.1")
    # e.trust_ip_get_by_port("wls", "2223")
    e.trust_ip_get("wls")
    # e.trust_ip_get_by_port("wls",'2223')
    #
    # import requests
    #
    # url = "http://localhost:8080/tcpth/register/delete"
    #
    # payload = "{\n\t\"name\":\"wls\",\n\t\"proxy_port\":\"3333\"\n}"
    # headers = {'content-type': 'application/json'}
    #
    # response = requests.request("POST", url, data=payload, headers=headers)
    #
    # print(response.text)

    # import re
    #
    # line = "wls 3333";
    # #
    # searchObj = re.search(r'(\S*)\s*(\S*)\s*(\S*)\s*(\S*)', line, re.M | re.I)
    # # # searchObj = re.search(r'(.*) are (.*?) .*', line, re.M | re.I)
    # print searchObj.group(3) + 'xx'
    # if searchObj.group(3) == '':
    #     print 'xxx'
    # if searchObj:
    #     print "searchObj.group() : ", searchObj.group(0)
    #     print "searchObj.group(1) : ", searchObj.group(1)
    #     print "searchObj.group(2) : ", searchObj.group(2)
    #     print "searchObj.group(3) : ", searchObj.group(3)
    #     print "searchObj.group(4) : ", searchObj.group(4)
    #     print searchObj.lastindex
    # else:
    #     print "Nothing found!!"

    # import json
    #
    # str1 = '[{"proxy_port":"2223","is_remote_manage":"false","read_speed":"0KB/s","write_bytes":"0KB","name":"wls","out_connection_count":"0","read_bytes":"0KB","local":"localhost:22","write_speed":"0KB/s"}]'
    #
    # j = json.loads(str1)
    #
    # print(j)
    # print(type(j))


    # from urllib import urlencode
    # import urllib2
    # def http_post(url, data):
    #     post = urlencode(data)
    #     req = urllib2.Request(url, post,headers={"Content-Type": "application/json; charset=UTF-8"})
    #     response = urllib2.urlopen(req)
    #     return response.read()
    #
    #
    # data = {
    #     "name": "wls",
    #     "proxy_port": 3333
    # }
    # http_post('http://localhost:8080/tcpth/register/delete', data)
