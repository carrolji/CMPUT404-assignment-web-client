#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = data[0].split(" ")[1]
        return int(code)

    def get_headers(self,data):
        return None

    def get_body(self, data):
        #last item in data list
        return data[-1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        u = urlparse(url)
        HOST = u.hostname
        PORT = u.port
        path = u.path

        if path == "":
            path = '/'

        if PORT == None:
            PORT = 80
       
        # HTTP GET HEADER
        payload = "GET {} HTTP/1.1\r\nHost: {}:{}\r\nConnection: close\r\n\r\n".format(path,HOST,PORT)
        
        self.connect(HOST, PORT)
        self.sendall(payload)
        
        data = self.recvall(self.socket).split('\r\n')
        code = self.get_code(data)
        body = self.get_body(data)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        p_url = urlparse(url)
        HOST = p_url.hostname
        PORT = p_url.port
        path = p_url.path

        if path == "":
            path = '/'
        
        if PORT == None:
            PORT = 80

        a_len = 0
        post_a = ""
        if args:
            post_a = urlencode(args)
            a_len = len(post_a)
        
        # HTTP POST Header
        cont_type = "Content-Type: application/x-www-form-urlencoded"
        cont_len = "Content-Length: {}\r\n\r\n{}".format(a_len,post_a)
        payload = "POST {} HTTP/1.1\r\nHost: {}:{}\r\n{}\r\n{}\r\n\r\n".format(path,HOST,PORT,cont_type,cont_len)

        self.connect(HOST, PORT)
        self.sendall(payload)

        data = self.recvall(self.socket).split('\r\n')
        code = self.get_code(data)
        body = self.get_body(data)
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
