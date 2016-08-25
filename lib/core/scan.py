import sys
import urllib2
from urlparse import urlparse
import socket
import httplib
import ssl

chttps = 0
chttp = 0
cerror = 0

class Scan:

    def __init__(self, settings):
        global chttps, chttp, cerror
        self.settings = settings

    def config_request(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def connection(self, url, scheme='https://'):
        ctx = self.config_request()

        url = scheme + site
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.settings['http']['user_agent'])
        req.add_header('Origin', self.settings['http']['origin'])
        try:
            response = urllib2.urlopen(req, timeout=3, context=ctx)
        except socket.error as error:
            return str(error), -1, ''
        except urllib2.URLError as error:
            return str(error.reason), -2, ''
        except httplib.HTTPException as error:
            return str(error), -3, ''
        else:
            return response.geturl(), response.getcode(), response.info().items()

    def get_data(self, site):
        global chttps, chttp, cerror
        newurl, code, headers = connectionN(site)
        if code < 0:
            newurl, code, headers = connectionN(site, 'http://')
        scheme_token = newurl.count('https://')
        if code == 200 and scheme_token == 1:
            chttps += 1
        elif code == 200 and scheme_token == 0:
            chttp += 1
        else:
            cerror += 1
        return newurl, code, headers

    def get_summary(self):
        print('')
        print('Connections summary')
        print('https: {}').format(chttps)
        print('http: {}').format(chttp)
        print('error: {}').format(cerror)
