import httplib
import base64

class YDaw(object):
    headers = {}
    all_headers = {'Accept': '*/*',
        'Authorization': '',
        'Expect': '100-continue',
        'Content-Type': 'application/binary',
        'Depth': 1,
        'Content-Length': 0}
    
    header_types = {'folder_status': ('Accept',
                                      'Authorization',
                                      'Depth'),
                    'create_folder': ('Accept',
                                      'Authorization'),
                    'sync_data': ('Accept',
                                  'Authorization',
                                  'Expect',
                                  'Content-Type',
                                  'Content-Length')}

    def __init__(self, token=None, user=None, pwd=None):
        if token:
            self.auth = 'OAuth %s' % token
        elif user and pwd:
            b_auth = b'%s:%s' % (user, pwd)
            self.auth = 'Basic %s' % base64.b64encode(b_auth)
        else:
            raise Exception()
        self.all_headers['Authorization'] = self.auth

    def _set_headers(self, header_type, content_len=None):
        self.headers = {}
        for key, val in self.all_headers.items():
            if key in self.header_types[header_type]:
                self.headers[key] = val
        if content_len:
            self.headers['Content-Length'] = content_len

    def get_folder_status(self, folder):
        self._set_headers('folder_status')
        return self.request('PROPFIND', '/%s' % folder)

    def create_folder(self, folder):
        self._set_headers('create_folder')
        return self.request('MKCOL', '/%s' % folder)

    def sync_file(self, folder, file_name, file_data):
        self._set_headers('sync_data', len(file_data))
        return self.request('PUT', '/%s/%s' % (folder,
                file_name), file_data)

    def request(self, method, path, data=None):
        conn = httplib.HTTPSConnection("webdav.yandex.ru")
        conn.putrequest(method, path)
        for key, value in self.headers.items():
            conn.putheader(key, value)
        conn.endheaders()
        if data:
            conn.send(data)
        response = conn.getresponse()
        conn.close()
        print response.getheaders()
        print response.status
        data = response.read()
        print data
        return response.status
