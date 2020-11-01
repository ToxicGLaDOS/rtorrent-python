#
# Copyright (c) 2013 Dean Gardiner, <gardiner91@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from base64 import b64encode
import string
try:
    import xmlrpc.client as xmlrpclib
except:
    import xmlrpclib


class BasicAuthTransport(xmlrpclib.Transport):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        auth_headers = self.get_auth_headers()
        xmlrpclib.Transport.__init__(self, headers=[auth_headers])



    def get_auth_headers(self):
        if self.username is not None and self.password is not None:
            b64 = str(b64encode(f"{self.username}:{self.password}".encode("utf-8")), "utf-8")
            auth_value = f"Basic {b64}"
            return ('AUTHORIZATION', auth_value)

    def single_request(self, host, handler, request_body, verbose=0):
        # issue XML-RPC request

        try:
            connection = self.send_request(host, handler, request_body, False)
            response = connection.getresponse()
            if response.status == 200:
                self.verbose = verbose
                return self.parse_response(response)
        except xmlrpclib.Fault:
            raise
        except Exception:
            self.close()
            raise

        #discard any response data and raise exception
        if response.getheader("content-length", 0):
            response.read()
        raise xmlrpclib.ProtocolError(
            host + handler,
            response.status, response.reason,
            response.msg,
        )
