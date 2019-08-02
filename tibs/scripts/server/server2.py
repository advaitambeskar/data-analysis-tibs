import socket

class Connection():  
    def __init__(self): 
        self.connected = False        

    def start_connention(self):
        host = '192.168.42.1'
        port = 8888

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)         

        #Bind socket to local host and port
        try:
            self.server.bind((host, port))
        except socket.error as msg: # CAN SOMEONE FIX THIS? I AM UNABLE TO BE SURE IF THAT IS CORRECT
            print('Binding failed, '+ msg)
              

        #Start listening on socket
        self.server.listen(10)

        self.connection, addr = self.server.accept()             

        #Disable blocking
        self.connection.settimeout(0.0)        

        self.connected = True                     

    def read(self):
        try:
            data = 'THIS' # KAREEM ADD YOUR VARIABLE HERE AND POSSIBLY COMMENT AN EXAMPLE
        except:
            data = ["N"] #no data
        return data

    def send(self, message):
        self.connection.sendall(message) # KENNY USE THE FUNCTION TO SEND!!

    def close(self):
        print("closing")
        self.connected = False
        self.server.close()