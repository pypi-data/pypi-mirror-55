import requests
import base64
import json
import numpy as np
import os
import pandas as pd
import warnings

class simSearch():
    """
    Base class for a simSearch instance.
    
    Parameters
    ----------
    DataUploaded: boolean (default = True). If training data already uploaded to simMachines's software, set to True. If not, set to False and angels can be trained on new data not yet uploaded to the software by passing variables X and y to the classifier. \n
    fileName: string (default = ''). Name of the data file if new data is being used to train classifier. Optional, not needed if DataUploaded = True. \n
    specs: dictionary (default = {}). Data specification types for training data. Dictionary keys represent the header names, and the values represent the data types. Optional, highly recommended if DataUploaded = False. \n
    folderName: string (default = ''), Name of folder containing training data.\n
    specFileName: string (default = ''), Name of spec file to use for training. If empty, the most recent compatible file will be chosen.\n
    verbose: bool (default = True). Enable verbose output\n
    Pivots: int (default = 256), The number of primary search points in the engine. This may improve query speed at the cost of training time. (Range 256 to 1024)\n
    Probability: float (default = .95), Minimum accepted probability that the distance between the result and the query will be within the Accepted Error range.  Any result with lower probability will be discarded.\n
    AcceptedError: float (default = 1.2), Maximum accepted difference in distance between returned objects and the query object (Minimum = 1).\n
    K: int (default = 10), Specify the k number of results for the nearest neighbor search.\n
    Storage: int (default = 1)\n
    Parallelism: int (default = 2)\n
    PivotSampleSize: int (default = 20000)\n
    CacheSize: int (default = 1000000)\n
    IndexCount: int (default = 3)\n
    MaximumBytesPerObject: int (default = 500000)\n
    IndexSampleSize: int (default = 100)        
    """
    def __init__(self,authenticate_creds,*,DataUploaded = True,fileName = '', specs={},
            folderName = '', specFileName = '',verbose=True, Pivots = 256,
            Probability = .95, AcceptedError = 1.2, K = 10,
            Storage = 1, Parallelism = 2, PivotSampleSize = 20000, CacheSize = 1000000, 
            IndexCount = 3, MaximumBytesPerObject = 500000, IndexSampleSize = 100):
        try:
            self.filepassword = authenticate_creds['filepassword']
            self.username = authenticate_creds['username']
            self.https = authenticate_creds['https']
            self.path = authenticate_creds['path']
            self.port = authenticate_creds['port']
        except KeyError:
            raise AttributeError("Credentials not passed from Authenticate.credentials.")

        ## Second verification of username and password
        verify_URL = 'https' + '://' + self.path + ':' + self.port + '/cloud/verifyUser' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud/verifyUser'
        password = base64.b64decode(self.filepassword.split()[1]).decode().split(':')[1]
        self.b64password = base64.b64encode(password.encode())
        resp_verify = requests.get(verify_URL,auth=(self.username, password))
        if resp_verify.status_code != 200:
            raise AttributeError("Username-Password combination not recognized. Please try again.")
            
        self.fileName = fileName
        self.DataUploaded = DataUploaded
        self.specs = specs
        self.folderName = folderName
        self.specFileName = specFileName
        self.verbose = verbose
        self.Pivots = Pivots
        self.Probability = Probability
        self.AcceptedError = AcceptedError
        self.K = K
        self.Storage = Storage
        self.Parallelism = Parallelism
        self.PivotSampleSize = PivotSampleSize
        self.CacheSize = CacheSize
        self.IndexCount = IndexCount
        self.MaximumBytesPerObject = MaximumBytesPerObject
        self.IndexSampleSize = IndexSampleSize

        # Building base URL's
        base_cloud_url = 'https' + '://' + self.path + ':' + self.port + '/cloud' if self.https else 'http' + '://' + self.path + ':' + self.port + '/cloud'
        self.base_cloud_url = base_cloud_url
        base_v2_url = 'https' + '://' + self.path + ':' + self.port + '/V2.0' if self.https else 'http' + '://' + self.path + ':' + self.port + '/V2.0'
        self.base_v2_url = base_v2_url
        
        # Checking if folderName exists
        if not self.DataUploaded:
            listFolders_URL = self.base_cloud_url +'/listFolders'
            resp_folders = requests.get(listFolders_URL,auth=(self.username, password))
            if resp_folders.status_code == 200:
                resp_folders_json = json.loads(resp_folders.content.decode())
                folder_exists = 0
                for item in resp_folders_json['list']:
                    if item['name'] == self.folderName:
                        folder_exists = 1
            else:
                raise AttributeError(resp_folders.content.decode())
                
            self._folder_exists = folder_exists
            if self._folder_exists:
                raise AttributeError("Folder name '" + self.folderName + "' already exists. Must choose a unique folder name if 'DataUploaded' is set to False")   
                
        # Warnings
        if self.fileName and self.DataUploaded:
            warnings.warn("Since 'DataUploaded' = True, 'fileName' will be ignored.")
        if not self.DataUploaded and not self.specs:
            warnings.warn("Data type specifications ('specs') not provided. Automated specification types will be used in model creation. However, it is recommended that spec files are created by the user to improve model performence.")
        # if not self.DataUploaded and self.specFileName:
            # warnings.warn("A spec file name was provided for data not yet uploaded to simMachines's software. 'specFileName' will be ignored.")
        # Exceptions
        if not self.fileName and not self.DataUploaded:
            raise AttributeError('Missing file name (fileName) for data to be uploaded.')
        if not self.folderName:
            raise AttributeError("Must specify name of folder to train Leliel with ('folderName' variable).")            
            
        
    def fit(self, *, X='', instanceName = ''):
        """
        Train a simSearch instance
        
        Parameters
        ----------
        X: array or pandas DataFrame, optional (default = ''), shape = (n_samples, n_features). Training data. If X is an array, the first row must be the headers. If X is a pandas DataFrame, the column names will be used as the headers. Optional, only needed if 'DataUploaded' is set to False.\n 
        instanceName: string (default = ''), Name of instance to be trained.\n
        
        Returns
        ---------
        self: object. Returns self.
        
        """

        password = base64.b64decode(self.b64password).decode()
        
        ## Checking if folder exists
        if instanceName:
            self.instanceName = instanceName
            if self.DataUploaded:
                ## Warnings
                if isinstance(X,pd.DataFrame):
                    warnings.warn("Since 'DataUploaded' = True, 'X' will be ignored.")
                elif isinstance(X,pd.Series):
                    warnings.warn("Since 'DataUploaded' = True, 'X' will be ignored.")
                else: 
                    if type(X) == str and X:
                       warnings.warn("Since 'DataUploaded' = True, 'X' will be ignored.")
                    else:
                        if len(X) > 0:
                            warnings.warn("Since 'DataUploaded' = True, 'X' will be ignored.")           
                
                
                ## getting Specs from folder
                specs_URL = self.base_cloud_url +'/listSpecByFolder?folderName=' + self.folderName
                resp_specs = requests.get(specs_URL,auth=(self.username, password))
                if resp_specs.status_code == 200:
                    specs_json = json.loads(resp_specs.content.decode())
                    valid_specFileName = 0
                    createdDate = 0
                    spec_file_name = ''
                    for spec_file in specs_json['list']:
                        if 'RAMIEL' in spec_file['angelName']:
                            if self.specFileName:
                                if self.specFileName == spec_file['fileName']:
                                    valid_specFileName = 1
                            else:
                                ## If specFileName not given by user, choose most 
                                ## recent compatible file present 
                                createdDate_curr = spec_file['createdDate']
                                if createdDate_curr > createdDate:
                                    createdDate = createdDate_curr
                                    spec_name_curr = spec_file['fileName'].split('.')[0]
                                    valid_specFileName = 1
                    spec_file_name = spec_name_curr
                else:
                    raise AttributeError(resp_specs.content.decode())
                
                ## Error message if specFileName not recognized
                if not valid_specFileName and self.specFileName:
                    raise AttributeError("Spec file name not recognized.")
                elif not valid_specFileName:
                    raise AttributeError("No compatible spec files found for folder " + self.folderName)
                if spec_file_name:
                    self.specFileName = spec_file_name                

            ## New data not uploaded yet is being used to train angel
            else:         
                if isinstance(X,pd.DataFrame):
                    headers = list(X.columns)
                    X = np.asarray(X)
                elif isinstance(X,pd.Series):
                    headers = [X.name]
                    X = np.asarray(X)
                else: 
                    if type(X) == str:
                        raise TypeError('X cannot be a string. Acceptable types: pandas Dataframe or numpy array.')
                    else:
                        if len(X) > 0:
                            headers = list(X[0])
                            X = np.asarray(X)
                        else:
                            raise AttributeError("X must be provided if 'DataUploaded' is set to False")
                        
                # Creating new folder
                if not self._folder_exists:
                    createFolder_URL = self.base_cloud_url +'/createFolder'
                    folder_data = {"folderName" : self.folderName}
                    resp_CreateFolder = requests.post(createFolder_URL,data = folder_data,auth=(self.username, password))
                    if not resp_CreateFolder.status_code == 200:
                        raise AttributeError(resp_CreateFolder.content.decode())
                else:
                    raise AttributeError('Folder with name %s already exists.' % self.folderName)
                    
                ## Upload data to "folderName"
                uploadFile_URL = self.base_cloud_url + '/uploadFile'
                
                ## Validating shape of input data
                if X.shape[1] != len(headers):
                    raise ValueError('X.shape[1] must equal the length of headers')

                    
                with open(self.fileName,'wb') as r:
                    ## Header
                    header_string = '\t'.join(headers) + '\n'
                    r.write(header_string.encode('utf8'))
                    for i,row in enumerate(X):
                        row_str = '\t'.join([str(val) for val in row.tolist()])
                        if i == (len(X)-1):
                            pass
                        else:
                            row_str += '\n'
                        r.write(row_str.encode('utf8'))
                    r.flush()
                r.close()
                
                filesize = os.path.getsize(self.fileName)
                
                with open(self.fileName,'rb') as f:
                    file_stream = {'fileData' : f}
                    file_data = {'fileName' : self.fileName
                              ,'fileSize' : filesize
                              ,'folderName' : self.folderName
                              ,'authorization' : self.filepassword
                              }
                    resp_upload = requests.post(uploadFile_URL
                                         ,files = file_stream
                                              ,data = file_data
                                              ,auth = (self.username,password))
                f.close()
                os.remove(self.fileName)
                
                if not resp_upload.status_code == 200:
                    raise AttributeError(resp_upload.content.decode())
                
                ## Create spec file
                create_specs_url = self.base_cloud_url + '/createSpecsForFolder'
                if not self.specs:
                    # Use recommended specs from /getSpecsOfFolder
                    getSpecs_URL = self.base_cloud_url + '/getSpecsOfFolder?folderName=' + self.folderName
                    resp_specs = requests.get(getSpecs_URL,auth=(self.username,password))
                    if resp_specs.status_code == 200:
                        resp_specs_json = json.loads(resp_specs.content.decode())
                        column_dict = {}
                        for item in resp_specs_json['columns']:
                            col_name = item['columnName']
                            spec_type = item['typeOfColumn']
                            column_dict[col_name] = spec_type
                        print(column_dict)
                        id_col = input("Enter the column to be used as the 'ID' field: ")
                        if id_col not in column_dict.keys():
                            raise AttributeError("Column " + id_col + " not found in data set.")
                        column_dict[id_col] = 'ID'
                        column_dict_json = json.dumps(column_dict)
                        self.specFileName =  input("Enter spec file name: ")
                        specs_data = {"specsTypes" : column_dict_json
                                          ,"folderName" : self.folderName
                                          ,"specsFileName" : self.specFileName
                                          ,"modelType" : "simSearch"
                                    }
                        resp_create_specs = requests.post(create_specs_url
                                  , data = specs_data
                                  , auth = (self.username,password))
                        if not resp_create_specs.status_code == 200:
                            raise AttributeError(resp_create_specs.content.decode())
                    else:
                        raise AttributeError(resp_specs_json.content.decode())
                else:
                    column_dict_json = json.dumps(self.specs)
                    if not self.specFileName:
                        self.specFileName =  input("Enter spec file name: ")
                    specs_data = {"specsTypes" : column_dict_json
                                      ,"folderName" : self.folderName
                                      ,"specsFileName" : self.specFileName
                                      ,"modelType" : "simSearch"
                                }
                    resp_create_specs = requests.post(create_specs_url
                                          , data = specs_data
                                          , auth = (self.username,password))
                    if not resp_create_specs.status_code == 200:
                        raise AttributeError(resp_create_specs.content.decode())
                
            params_str = 'K=' + str(self.K) + '_@_@_PIVOTS=' + str(self.Pivots) + '_@_@_PROBABILITY=' + str(self.Probability) + \
                        '_@_@_ACCEPTED_ERROR=' + str(self.AcceptedError) + '_@_@_EXECUTE_FOLD=false' + '_@_@_PIVOT_SAMPLE_SIZE=' + \
                        str(self.PivotSampleSize) + '_@_@_CACHE_SIZE=' + str(self.CacheSize) + '_@_@_INDEX_COUNT=' + str(self.IndexCount) + '_@_@_MAXIMUM_BYTES_PER_OBJECT=' + \
                        str(self.MaximumBytesPerObject) + '_@_@_INDEX_SAMPLE_SIZE=' + str(self.IndexSampleSize)
            ## Building API call
            instance_data = {"instanceName" : self.instanceName,
                             "folderName" : self.folderName,
                             "modelType": 'simSearch',
                             "params": params_str,
                             "storage" : self.Storage,
                             "parallelism" : self.Parallelism,
                             "authorization" : self.filepassword,
                             "specsFileName" : self.specFileName
                    }
            ## POST request to create instance
            createInstance_url = self.base_cloud_url + '/createInstance'
            resp = requests.post(createInstance_url,data = instance_data, auth = (self.username, password))
            
            if resp.status_code == 200:
                listInstances_url = self.base_cloud_url + '/listInstances'
                status = 'Unknown'
                while status not in ('RUNNNING', 'BUILD_ERROR'):
                    resp_status = requests.get(listInstances_url, auth=(self.username, password))
                    if resp_status.status_code == 200:
                        resp_JSON = json.loads(resp_status.content.decode())
                        
                        ## looping through instances
                        for l in resp_JSON['list']:
                            if l['label'] == self.instanceName:
                                status_curr = l['status']
                                if status != status_curr:
                                    status = status_curr
                                    if self.verbose:
                                        print('Status: ' + status)
                    else:
                        raise AttributeError(resp_status.content.decode())
                    if status == 'RUNNING':
                        print("Instance '" + self.instanceName + "' is ready for querying.")
                        break
                    elif status == 'BUILD_ERROR':
                        print("Instance '" + self.instanceName + "' returned a status of '" + status + "'.")
                        break
            else:
                ## If instance not created, set instance name to '' 
                self.instanceName = ''
                raise AttributeError(resp.content.decode())
        else:
            raise AttributeError("Must enter instance name as 'instanceName' variable")
        
        return self
    
        
    def get_neighbors(self, X, *, version = ''):
        """
        Retrive nearest neighbors using trained simSearch instance.
        
        Parameters
        ----------
        X: {array-like}. Samples to retrieve neighbors for. shape = (n_samples, n_features). 
        First line must be headers. 
        
        Returns
        ----------
        neighbors_final: list, shape = (n_samples,(K,2))
        ID, distance pairs of nearest neighbors
        """
        password = base64.b64decode(self.b64password).decode()    
    
        if self.instanceName:
            if isinstance(X,pd.DataFrame):
                headers = list(X.columns)
                X = np.asarray(X)
            elif isinstance(X,pd.Series):
                headers = [X.name]
                X = np.asarray(X)
            else: 
                if type(X) == str:
                    raise TypeError('X cannot be a string. Acceptable types: pandas Dataframe, Series or numpy array.')
                else:
                    if len(X) > 0:
                        headers = list(X[0])
                        X = np.asarray(X[1:])
                    else:
                        raise AttributeError("X must be provided if 'DataUploaded' is set to False")
            headers_str = '\t'.join(headers)
            samples = X
            neighbors_final=[]
            if samples.shape[0]> 0:
                failed_queries = 0
                for samp in samples:
                    neighbors=[]
                    sample_str = '\t'.join([str(s) for s in samp])
                    queryObject_url = self.base_cloud_url + '/queryObject'
                    if version:
                        query_data = {"instanceName" : self.instanceName,
                                      "version" : version,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }
                    else:
                        query_data = {"instanceName" : self.instanceName,
                                      "query" : headers_str + '\n' + sample_str,
                                      "authorization" : self.filepassword
                                }              
                    resp_query = requests.post(queryObject_url
                                               ,data = query_data
                                               ,auth = (self.username, password))
                        
                    if resp_query.status_code == 200:
                        ## Converting response to JSON object
                        resp_query_json = json.loads(resp_query.content.decode())
                        for item in resp_query_json['results']:
                            neighbors.append((item['id'],float(item['distance'])))
                        neighbors_final.append(neighbors)
                    else:
                        failed_queries += 1
                        error_message = resp_query.content.decode()
                
                if not failed_queries:
                    return neighbors_final
                else:
                    raise AttributeError("One or more queries producing errors. API error message: " + error_message + ".")        
            else:
                raise AttributeError("Must contain both headers and query objects for prediction.")           
        else:
            raise AttributeError("Must create instance by using fit() before predicting.")