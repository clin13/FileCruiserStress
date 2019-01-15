import json

class ContentSearchClient (object):

    def content_search(self, tenant_id, path = None, query = {}) :
        _url = self.content_search_url
        query['index'] = tenant_id
        if path :
            if path == '.' :
                query['path'] = '/'
            else : 
                query['path'] = path
        _url = self.add_query_string(_url, query)
        return self._do_request(_url, 'GET')

