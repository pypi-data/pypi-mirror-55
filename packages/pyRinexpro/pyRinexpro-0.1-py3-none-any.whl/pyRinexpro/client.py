# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:00:44 2019

@author: andres_c
"""

import requests
import json
import logging
from time import sleep
from .session import ASession, Session, SessionList, SessionStatus
from .process import Process, ProcessStatus, ProcessList, ParamsVrs

HOST="https://api.rinexpro.com:5003"

class ErrorAPI(Exception):
    """The execption used when api return an error"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Client:
    """A client to the rinexpro api, it contain the api key and can make request to the api
    
    Args:
        secret_key (str): The api key
    """
    def __init__(self, secret_key):
        self.secret_key = secret_key
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def api_request(self, uri, params={}, method='get', files={}, parse_resp=True):
        """Make an HTTP request to the api
        
        Args:
            uri (str): The url without host name
            params (dict(str,object)): The url parameters (default is {})
            method (str): The HTTP method, not case sensitive (default is 'get')
            files (dict(str,file)): Files to upload only with POST method (default is {})
            parse_resp (bool): Parse the response as a json file (default is True)

        Returns:
            object or list(byte): The parsed json as a Python object or the HTTP content
        """
        uri = HOST + uri + "?key=" + self.secret_key
        for k,v in params.items():
            uri += "&{}={}".format(k,v)
        if method.upper() == "POST":
            response = requests.post(uri, files=files)
        elif method.upper() == "PUT":
            response = requests.put(uri)
        elif method.upper() == "DELETE":
            response = requests.delete(uri)
        elif method.upper() == "GET":
            response = requests.get(uri)
        else:
            raise ValueError('method should be "get", "post", "put" or "delete"')
        if response.status_code != 200 and response.status_code != 201:
            if response.headers.get('Content-Type') == 'application/json':
                json_obj = json.loads(response.text)
                if 'error' in json_obj:
                    raise ErrorAPI(json_obj['error'])
            raise ErrorAPI(response.content)
        if parse_resp == False:
            return response.content
        json_obj = json.loads(response.text)
        if 'error' in json_obj:
            raise ErrorAPI(json_obj['error'])
        return json_obj
            
    def getSessions(self, status=None, before=None, after=None):
        """Get all sessions as a list
        
        Example:
            
        .. code-block:: python
            
            >>> sesssions = client.getSessions(after='20190521')
        
        Args:
            status(int or SessionStatus): Filter sessions by status (default is None)
            before(str or datetime): Filter sessions by last_epoch (default is None)
            after(str or datetime): Filter sessions by last_epoch (default is None)
        
        Returns:
            SessionList: All sessions found
        """
        params = {}
        if status is not None:
            if isinstance(status, int):
                params['status'] = status
            else:
                params['status'] = status.value
        if before is not None:
            if isinstance(before, str):
                params['before'] = before
            else:
                params['before'] = before.strftime("%Y%m%d")
        if after is not None:
            if isinstance(after, str):
                params['after'] = after
            else:
                params['after'] = after.strftime("%Y%m%d")
        json_obj = self.api_request("/session", params)
        return SessionList(json_obj, self)

    
    def getSession(self, id):
        """Get a session by id
        
        Example:
            
        .. code-block:: python
            
            >>> sesssion = client.getSession(12)
        
        
        Args:
            id (int): The id of the session
        
        Returns:
            Session: The session associated to the id
        """
        json_obj = self.api_request("/session/%d" % (id))
        return Session(json_obj, self)
    
    def getProcesses(self, algo=None, status=None, before=None, after=None):
        """Get all processes as a list
        
        Example:
            
        .. code-block:: python
            
            >>> processes = client.getProcesses(algo='diff', status=PROC_SUCCESS)
        
        
        Args:
            algo (str): Filter processes by algo (default is None) 
            status(int or SessionStatus): Filter processes by status (default is None)
            before(str or datetime): Filter processes by last_epoch (default is None)
            after(str or datetime): Filter processes by last_epoch (default is None)
            
        Returns:
            ProcessList: All processes found
        """
        params = {}
        if status is not None:
            if isinstance(status, int):
                params['status'] = status
            else:
                params['status'] = status.value
        if before is not None:
            if isinstance(before, str):
                params['before'] = before
            else:
                params['before'] = before.strftime("%Y%m%d")
        if after is not None:
            if isinstance(after, str):
                params['after'] = after
            else:
                params['after'] = after.strftime("%Y%m%d")
        if algo is not None:
            params['algo'] = algo
        json_obj = self.api_request("/process", params)
        return ProcessList(json_obj, self)
    
    def getProcess(self, id):
        """Get a process by id
        
        Example:
            
        .. code-block:: python
            
            >>> process = client.getProcess(24)
        
        Args:
            id (int): The id of the process
        
        Returns:
            Process: The process associated to the id
        """
        json_obj = self.api_request("/process/%d" % (id))
        return Process(json_obj, self)
    
    def uploadSession(self, sess_file=None, link=None, antenna_height=None, format=None, wait=False, refresh_rate=10, wait_retry='ask'):
        """Create a session by uploading a file
        
        Example:
            
        .. code-block:: python
            
            >>> sesssion = client.uploadSession(link="https://my-sessions-files/session-3")
        
        
        Args:
            sess_file (str or file): The file location or file-like object (default is None)
            link (str): The file url (default is None)
            antenna_height (float): The antenna height (default is None)
            format (str): The file format (default is None)
            wait (bool): Wait for the process to finish (default is None)
            refresh_rate (int): The time in second between each update, used when wait is True (default is 10)
            wait_retry (str): Should it wait for the preprocessing to retry (default is ask)

        Returns:
            Session: The created session
        """
        params = {}
        if antenna_height is not None:
            params['antenna_height'] = antenna_height
        if format is not None:
            params['format'] = format
        if link is not None:
            params['link'] = link
            json_obj = self.api_request("/session/upload", params=params, method='post')
        elif isinstance(sess_file, str):
            f = open(sess_file, 'rb')
            json_obj = self.api_request("/session/upload", params=params, method='post', files={'file':f})
            f.close()
        else:
            json_obj = self.api_request("/session/upload", params=params, method='post', files={'file':sess_file})
        sess = Session(json_obj, self)
        if wait:
            self.logger.info("Session uploaded id:%d", sess._id)
            sess.wait(refresh_rate, wait_retry)
        return sess
    
    def virtualSession(self, *args, wait=False, refresh_rate=10, **kwargs):
        """Create a virtual session
        
        Example:
            
        .. code-block:: python
            
            >>> sesssion = client.virtualSession('MYVRS', 64.03, 12.91, "2019-01-21 12:33:05",
                                                 "2019-01-21 15:15:35", 30)
        
        Args:
            *args: ParamsVrs or same parameters as ParamsVrs.__init__()
            wait (bool): wait for the process to finish (default is None)
            refresh_rate (int): The time in second between each update, used when wait is True (default is 10)
            **kargs: Same parameters as ParamsVrs.__init__()

        Returns:
            Session: The created session
        """
        if len(args) == 1 and isinstance(args[0], ParamsVrs):
                params = args[0].to_dict()
        else:
            params = ParamsVrs(*args, **kwargs).to_dict()
        json_obj = self.api_request('/session/vrs', params=params, method='post')
        sess = Session(json_obj, self)
        if wait:
            self.logger.info("VRS created id:%d", sess._id)
            sess.wait(refresh_rate)
        return sess
    
    def geoRef(self, sess_file=None, link=None, antenna_height=None, format=None, params=None, refresh_rate=10, wait_retry='yes', **kwargs):
        """Upload a session, launch a diff process and get the result
        
        Example:
            
        .. code-block:: python
            
            >>> log = client.geoRef('my-session-file', mode='static', n=4)
        
        
        Args:
            sess_file (str or file): The file location or file-like object (default is None)
            link (str): The file url (default is None)
            antenna_height (float): The antenna height (default is None)
            format (str): The file format (default is None)
            params(ParamsDiff): The parameters of the algorithm (default is None)
            refresh_rate (int): The time in second between each update (default is 10)
            wait_retry (str): Should it wait for the preprocessing to retry (default is ask)
            **kwarg: The same parameters ParamsDiff.__init__(), used when params is None
        
        Returns:
            LogDiff, Process, Session: return LogDiff on success
        """
        self.logger.info("GeoRef step 1/3 : upload session")
        sess = self.uploadSession(sess_file, link, antenna_height, format, True, refresh_rate, wait_retry)
        if sess.status != SessionStatus.NAV_SUCCESS:
            self.logger.info("GeoRef step 1 failed")
            return sess
        self.logger.info("GeoRef step 2/3 : run diff algorithm")
        p = sess.newProcess('diff', params, wait=True, refresh_rate=refresh_rate, **kwargs)
        if p.status != ProcessStatus.PROC_SUCCESS:
            self.logger.info("GeoRef step 2 failed")
            return p
        self.logger.info("GeoRef step 3/3 : get diff log")
        return p.getLog()
    
    
    def ppp(self, sess_file=None, link=None, antenna_height=None, format=None, params=None, refresh_rate=10, wait_retry='yes', **kwargs):
        """Upload a session, launch a ppp process and get the result
        
        Example:
            
        .. code-block:: python
            
            >>> log = client.ppp('my-session-file', mode='kinematic')
        
        Args:
            sess_file (str or file): The file location or file-like object (default is None)
            link (str): The file url (default is None)
            antenna_height (float): The antenna height (default is None)
            format (str): The file format (default is None)
            params(ParamsDiff): The parameters of the algorithm (default is None)
            refresh_rate (int): The time in second between each update (default is 10)
            wait_retry (str): Should it wait for the preprocessing to retry (default is ask)
            **kwarg: The same parameters ParamsDiff.__init__(), used when params is None
        
        Returns:
            LogPPP, Process, Session: return LogPPP on success
        """
        self.logger.info("PPP step 1/3 : upload session")
        sess = self.uploadSession(sess_file, link, antenna_height, format, True, refresh_rate, wait_retry)
        if sess.status != SessionStatus.NAV_SUCCESS:
            self.logger.info("PPP step 1 failed")
            return sess
        self.logger.info("PPP step 2/3 : run ppp algorithm")
        p = sess.newProcess('ppp', params, wait=True, refresh_rate=refresh_rate, **kwargs)
        if p.status != ProcessStatus.PROC_SUCCESS:
            self.logger.info("PPP step 2 failed")
            return p
        self.logger.info("ppp step 3/3 : get ppp log")
        return p.getLog()
    
    def vrs(self, *args, refresh_rate=10, save_to='', **kwargs):
        """Create a VRS, save the Obs file and get the log
        
        Example:
            
        .. code-block:: python
            
            >>> log = client.vrs('my-session-file', 'MYVRS', 64.03, 12.91, "2019-01-21 12:33:05",
                                 "2019-01-21 15:15:35", 30, save_to='new_obs_file')
        
        Args:
            *args: The virtualSession parameters
            refresh_rate (int): The time in second between each update (default is 10)
            save_to (str): The path to save the obs file (default is '')
            **kwargs: The virtualSession parameters
            
        
        """
        nb_steps = 2 if save_to == '' else 3
        self.logger.info("VRS step 1/%d : creating vrs" % (nb_steps))
        if len(args) >= 1  and isinstance(args[0], ASession):
            name = args[1] if len(args) == 2 else kwargs['name']
            sess = args[0].virtualSession(name, True, refresh_rate)
        else:
            sess = self.virtualSession(*args, wait=True, refresh_rate=refresh_rate, **kwargs)
        if save_to != '':
            self.logger.info("VRS step 2/%d : saving obs file" % (nb_steps))
            if sess.status != SessionStatus.VRS_SUCCESS:
                self.logger.info("VRS failed")
                return sess
            sess.getFile('obs', save_to=save_to)
        self.logger.info("VRS step %d/%d : get vrs log" % (nb_steps, nb_steps))
        return sess.processes[0].getLog()
        