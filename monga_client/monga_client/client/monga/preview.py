class PreviewAPI (object):

    def preview_file(self, file_path, headers = {}, params = None) :
        _url = self.frog_url + '/' + self.quote(file_path)
        if params:
        	_url = '?'.join([_url, params])
        _headers = headers.copy()
        _headers['X-Auth-Token'] = self.token
        return self._do_request(_url, 'GET', _headers)
