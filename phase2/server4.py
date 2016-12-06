import socket
import sys
import threading
import time
host='127.0.0.1'
port=8080
directory='data3'
def content_types( file_name):
        content_types = {'html': 'text/html',
						'pdf':'application/pdf',
                                                'txt': 'text/txt',
						'gif':'images/gif',
                                                'jpg': 'image/jpeg',
                                                'png': 'image/png',
                                                'ico': 'icon/ico'}
        return content_types[file_name.split('.')[-1]]
def header(http_code, content_type):
	headr = ''
	if(http_code == 200):
		headr = 'HTTP/1.1 200 OK\n'
	elif(http_code == 404):
		headr = 'HTTP/1.1 404 File Not Found\n'
	headr += 'Content-Type:'+ content_type + '\n'
	headr += '\n'
	return headr


def WebServer():
		port=8085
		host='127.0.0.1'
		directorty='data'
		bindsocket(host,port)
def bindsocket(host,port):
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
        		serversocket.bind((host, port))
			print(" http://127.0.0.1:%d"%port)
			print("press CTRL-C to stop the server")
		except:
			port += 1
			bindsocket(host,port)

		run(serversocket)
def run(serversocket):
		while(True):
			print("Waiting for connection\n")
			serversocket.listen(1)
			clientsocket, clientaddress = serversocket.accept()
			requested_data = clientsocket.recv(1024)
			print("Received connection from:",clientaddress)
			query = bytes.decode(requested_data)
			http_method = query.split(' ')[0]
			#print("method:",http_method)
			if(http_method == 'GET'):
				print(http_method)
				file_ = query.split(' ')[1]
				if(file_ == '/'):
					file_ = '/index.html'
				file_ = directory + file_
				try:
					fp = open(file_, 'rb')
					response = fp.read()
					fp.close()
					content_type = content_types(file_)
				
					h = header(200, content_type)
				except:
					content_type = content_types(file_)
					h = header(400, 'text/html')
					response = "<html><body><p> Error 404 File not found</p></body></html>".encode()	
				final_response = h.encode()
				final_response += response
				clientsocket.send(final_response)				  
				time.sleep(50)
				clientsocket.close()
			else:
				print(http_method)
				print("HTTP request method unknown")			
			
                       
				
WebServer()


