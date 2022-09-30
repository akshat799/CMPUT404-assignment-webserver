#  coding: utf-8 
from genericpath import exists
import socketserver,os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))
        
        method = self.data.decode('utf-8').split()[0]
        pathRequest = self.data.decode('utf-8').split()[1]

        

        if method != 'GET':
            header = "HTTP/1.1 405 Method Not Allowed\r\n"
            contentType = "Content-Type: text/html\r\n"
            self.request.sendall(bytearray(header + contentType,'utf-8'))

        else:

            if pathRequest[-1] == "/":
                currentPath = os.getcwd() + "/www" + pathRequest + "index.html"
                contentType = "Content-Type: text/html\r\n"
                header = "HTTP/1.1 200 OK\r\n" 
                
            elif pathRequest[-4:] == ".css":
                currentPath = os.getcwd() + "/www" + pathRequest
                contentType = "Content-Type: text/css\r\n"
                header = "HTTP/1.1 200 OK\r\n" 

            elif pathRequest[-5:] == ".html":
                currentPath = os.getcwd() + "/www" + pathRequest
                contentType = "Content-Type: text/html\r\n"
                header = "HTTP/1.1 200 OK\r\n"                 

            else:
                currentPath = os.getcwd() + "/www" + pathRequest
                

            if "/.." in pathRequest or "../" in pathRequest:
                currentPath = os.getcwd() + "/www" + pathRequest
                contentType = "Content-Type: text/html\r\n"
                header = "HTTP/1.1 404 Page Not Found\r\n" 
                self.request.sendall(bytearray(header + contentType,'utf-8'))

            elif os.path.exists(currentPath) == True:
                try:
                    file = os.path.abspath(currentPath)
                    f = open(file,"r")
                    content = f.read()
                    f.close()
                    contentLength = f'Content-Length: {len(content)}\r\n\r\n'    
                    self.request.sendall(bytearray(header + contentType + contentLength + content, 'utf-8'))
                except:
                    contentType = "Content-Type: text/html\r\n"
                    header = f'HTTP/1.1 301 Moved Permanently\r\n'
                    location = f'Location: {pathRequest}/\r\n' 
                    self.request.sendall(bytearray(header + contentType + location,'utf-8'))

            else:
                header = 'HTTP/1.1 404 Page Not Found\r\n'
                contentType = "Content-Type: text/html\r\n"
                self.request.sendall(bytearray(header + contentType,'utf-8'))

            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
