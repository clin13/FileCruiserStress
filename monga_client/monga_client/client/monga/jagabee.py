class JagabeeAPI (object):

    def register_post(self, email = None, password = None, data = None, 
                       headers = {}):
        _headers = headers.copy()
        _url = "http://localhost:7000/register"
        if data :
            _req = data
        else :
            _req = {
                "email" : email,
                "password" : password
            }
            _req = json.dumps(_req)
        return self._do_request(_url, 'POST', _headers, _req)

    def register_put(self, email = None, password = None, enable = None,  
                     data = None, headers = {}) :
        _headers = headers.copy()
        _url = "http://localhost:7000/register"
        if data :
            _req = data
        else :
            _req = {
                "email" : email
            }
            if password != None :
                _req['password'] = password
            if enable != None :
                _req['enable'] = enable
            _req = json.dumps(_req)
        return self._do_request(_url, 'PUT', _headers, _req)

    def register_delete(self, email = None, data = None, headers = {}) :
        _headers = headers.copy()
        _url = "http://localhost:7000/register"
        if data :
            _req = data
        else :
            _req = {
                "email" : email
            }
            _req = json.dumps(_req)
        return self._do_request(_url, 'DELETE', _headers, _req)
