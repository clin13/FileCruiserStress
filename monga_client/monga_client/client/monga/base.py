import http.client
from monga_client.common.utils import *
from urllib.parse import urljoin, parse_qs, urlsplit, urlunsplit, urlparse

def _do_request(url, method = 'GET', headers = {}, contents = None, 
                chunk_size = 65536, _size = None, read = True,
                timeout = 60):
    _u = urlparse(url)
    if _u.scheme == 'http' :
        conn = http.client.HTTPConnection(_u.hostname, _u.port, timeout = timeout)
    elif _u.scheme == 'https' :
        conn = http.client.HTTPConnection(_u.hostname, _u.port, timeout = timeout)
    #Make size header
    if not contents :
        _size = 0
    elif not _size and contents:
        _size = len(contents)
    headers['Content-Length'] = _size
    _url = _u.path + '?' + _u.query

    if contents :
        if hasattr(contents, 'read'):
            conn.putrequest(method, _url)
            for header, value in headers.iteritems():
                conn.putheader(str(header), str(value))
            conn.endheaders()
            chunk = contents.read(65536)
            while chunk:
                conn.send(chunk)
                chunk = contents.read(65536)
        else:
            conn.request(method, _url, contents, headers)
    else :
        conn.request(method, _url, contents, headers)

    resp = conn.getresponse()
    _headers = {}
    for header, value in resp.getheaders():
        _headers[header] = value
    _resp = {'status' : resp.status, 'headers' : _headers}
    if read :
        return AttributeDict(_resp), resp.read()
    else :
        return AttributeDict(_resp), resp
