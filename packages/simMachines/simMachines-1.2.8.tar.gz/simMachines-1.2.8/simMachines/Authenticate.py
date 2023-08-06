import requests
import base64
from getpass import getpass

"""
Updates:
    - All API calls status codes verified before any other action
    - If data not uploaded to GUI, user does not have to input header parameters 
    outside of the data variables. 
    - Input data format supports pandas data frame or series, as well as numpy arrays
"""

class Authenticate():
    def __init__(self,*, username = '', password = '', path = '127.0.0.1',port = '9090',https = False):
        credentials = {}
        self.credentials = credentials 
        self.path = path
        self.port = str(port)
        self.https = https
        self.credentials['path'] = self.path
        self.credentials['port'] = self.port
        self.credentials['https'] = self.https
        if username:
            self.username = username 
        else:
            username = input("Enter username: ")
            self.username = username
        self.credentials['username'] = self.username
        if password:
            self.password = password 
        else:
            password = getpass("Enter password: ")
            self.password = password             

        ## Verifying username and password
        verify_URL = 'https' + '://' + self.path + ':' + self.port + '/cloud/verifyUser' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud/verifyUser'
        resp_verify = requests.get(verify_URL,auth=(self.username, self.password))
        if resp_verify.status_code == 200:
            authform = username + ':' + password
            filepassword = base64.b64encode(authform.encode())
            filepassword = filepassword.decode()
            filepassword = 'Basic ' + filepassword        
            self.filepassword = filepassword
            self.credentials['filepassword'] = self.filepassword
        else:
            raise AttributeError(resp_verify.content.decode())
