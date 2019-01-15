from monga_client.common.retry import normal_retry

class SwiftProxy():

    def combine_swift_url(self, acc = None, con = None, obj = None):
        if not acc : raise Exception()
        if type(acc) == unicode and acc != None: 
            acc = acc.encode('utf-8')
        if type(con) == unicode and con != None: 
            con = con.encode('utf-8')
        if type(obj) == unicode and obj != None: 
            obj = obj.encode('utf-8')
        if con and obj :
            return '/'.join([acc, self.quote(con), self.quote(obj)])
        elif con :
            return '/'.join([acc, self.quote(con)])
        else :
            return acc

    @normal_retry()
    def swift_get(self, acc, con = None, obj = None, headers = {}, query = {}):
        _url = self.swift_url + self.combine_swift_url(acc, con, obj)
        _query = {}
        _url = self.add_query_string(_url, query)
        _headers = headers.copy()
        return self._do_request(_url, 'GET', _headers)

    @normal_retry()
    def swift_post(self, acc, con = None, obj = None, body = '', 
                   headers = {}, query = {}):
        _url = self.swift_url + self.combine_swift_url(acc, con, obj)
        _query = {}
        _url = self.add_query_string(_url, query)
        _headers = headers.copy()
        return self._do_request(url = _url, 
                                method = 'POST', 
                                headers = _headers,
                                contents = body)

    @normal_retry()
    def swift_put(self, acc, con = None, obj = None, body = '', 
                  headers = {}, query = {}):
        _url = self.swift_url + self.combine_swift_url(acc, con, obj)
        _query = {}
        _url = self.add_query_string(_url, query)
        _headers = headers.copy()
        return self._do_request(url = _url, 
                                method = 'PUT', 
                                headers = _headers,
                                contents = body)

    @normal_retry()
    def swift_delete(self, acc, con = None, obj = None, headers = {}, 
                     query = {}):
        _url = self.swift_url + self.combine_swift_url(acc, con, obj)
        _query = {}
        _url = self.add_query_string(_url, query)
        _headers = headers.copy()
        return self._do_request(_url, 'DELETE', _headers)

    @normal_retry()
    def swift_head(self, acc,  con = None, obj = None, 
                   headers = {}, query = {}):
        _url = self.swift_url + self.combine_swift_url(acc, con, obj)
        _query = {}
        _url = self.add_query_string(_url, query)
        _headers = headers.copy()
        return self._do_request(_url, 'HEAD', _headers)
