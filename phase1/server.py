import socket
import sys
import threading
HOST='127.0.0.1'
PORT=8081
class WebServer(threading.Thread):
	directory="data"
	def __init__(self, host, port):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.connections = [] 
		self.running = True  
	def bindsocket(self):
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
        		self.serversocket.bind((self.host, self.port))
			print(" http://127.0.0.1:%d"%self.port)
			print("press CTRL-C to stop the server")
		except:
			self.port += 1
			self.bindsocket()
		self.run()
	def run(self):
	
		self.serversocket.listen(1)
		clientSocket, clientAddress =  self.serversocket.accept()
		Data = clientSocket.recv(1024)
		query = bytes.decode(Data)
		http_Method = query.split(' ')[0]
		second_term = query.split(' ')[1]
		if(http_Method == 'GET'):
			if(second_term == '/'):
				requestedFile = self.directory + '/index.html'
			print(requestedFile)	
			try:
				fp = open(requestedFile, 'rb')
				responseData = fp.read()
				header = self.headers(200)
				fp.close()
			except:
				header = self.headers(400)
				responseData = b"<html><body><p> Error 404 File not found</p></body></html>"	
			finalResponse = header.encode()
			finalResponse += responseData
			clientSocket.send(finalResponse)				  
			clientSocket.close()
		else:
			print("HTTP request methode unknown")			

	
			
	def headers(self, httpCode):
		headr = ''
		if(httpCode == 200):
			headr = 'HTTP/1.1 200 OK'
		elif(httpCode == 404):
			headr = 'HTTP/1.1 404 File Not Found'
		return headr
	

neserver = WebServer(HOST,PORT)
neserver.bindsocket()
