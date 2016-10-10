import json
from requests import session
from requests.exceptions import ConnectionError
from ConfigParser import RawConfigParser, NoSectionError


def parse_config():
    config = RawConfigParser()
    config.read('owtf.config')
    port = config.get('owtf', 'port').strip('\'')
    host = config.get('owtf', 'host').strip('\'')
    return host or '127.0.0.1', port or 8009


def addtarget(portmap):
    '''Accepts a dict of format { hostname :[<list of ports>] }'''
    COUNT = 0
    urldata = dict()
    API_HOST, API_PORT = parse_config()
    API_URL = "http://%s:%s/api/targets" % (API_HOST, API_PORT)
    for host, ports in portmap.items():
        for port, service in ports:
            if service == 'https' or port==443:
                URL = "https://%s:%s" % (host, port)
            elif service == 'http':
                URL = "http://%s:%s" % (host, port)

            urldata['target_url'] = URL
            with session() as c:
                try:
                    response = c.post(API_URL, data=urldata)
                    print response.text
                except ConnectionError:
                    print "[!] ERROR : Please check values in owtf.config (or, is OWTF running?)"
                    exit(1)
