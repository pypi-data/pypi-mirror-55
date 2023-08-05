# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:01:00 2019

@author: andres_c
"""

from collections import UserList
from datetime import datetime
from enum import Enum
from time import sleep
from .logs import LogRineqc, LogRinexnav, LogDiff, LogPPP, LogVrs

class ProcessStatus(Enum):
    """The process status"""
    PROC_WAITING = 100
    PROC_RUNNING = 101
    PROC_RETRY = 102
    PROC_ERROR = 103
    PROC_SUCCESS = 104
    
class AProcess:
    """An abstract class that containt the minimal Process data to request the api
    
    Args:
        client (Client): The client to request the api
        id (int): The process id
    """
    def __init__(self, client, id):
        self._client = client
        self._id = id
    
    def getLog(self):
        """Get the process log data
        
        Returns:
            LogRineqc, LogRinexnav, LogPPP or LogDiff : The log data depending on the process algorithm 
        """
        json_obj = self._client.api_request("/process/%d/GetLog" % (self._id))
        if self.algo == 'rineqc':
            return LogRineqc(json_obj)
        elif self.algo == 'rinexnav':
            return LogRinexnav(json_obj)
        elif self.algo == 'diff':
            return LogDiff(json_obj)
        elif self.algo == 'ppp':
            return LogPPP(json_obj)
        elif self.algo == 'vrs':
            return LogVrs(json_obj)
    

class Process(AProcess):
    """A process
    
    Args:
        json_obj (object): The parsed json
        client (Client): The client to request the api
    """
    def __init__(self, json_obj, client):
        super().__init__(client, json_obj['id'])
        self.uri = json_obj['uri']
        self.algo = json_obj['algo']
        if self.algo == "rineqc" and json_obj['params'] is not None:
            self.params = ParamsRineqc._from_json(json_obj['params'])
        elif self.algo == "ppp":
            self.params = ParamsPPP._from_json(json_obj['params'])
        elif self.algo == "diff":
            self.params = ParamsDiff._from_json(json_obj['params'])
        elif self.algo == "vrs":
            self.params = ParamsVrs._from_json(json_obj['params'])
        else:
            self.params = None
        self.posted_at = datetime.strptime(json_obj['posted_at'], "%a, %d %b %Y %H:%M:%S GMT")
        if json_obj['started_at'] != None:
            self.started_at = datetime.strptime(json_obj['started_at'], "%a, %d %b %Y %H:%M:%S GMT")
        if json_obj['ended_at'] != None:
            self.ended_at = datetime.strptime(json_obj['ended_at'], "%a, %d %b %Y %H:%M:%S GMT")
        self.status = ProcessStatus(json_obj['status']) 
        self.session = SessionOverview(json_obj['session'], client)
        
    def __repr__(self):
       return "Process(id={}, algo={})".format(self._id, self.algo)
        
    def update(self):
        """Update the object data
        
        Returns:
            Process: self
        """
        json_obj = self._client.api_request("/process/%d" % (self._id))
        self.__init__(json_obj, self._client)
        return self
    
    def wait(self, refresh_rate=10):
        """Wait for the process to finsh
        
        Args:
            refresh_rate (int): The time in second between each update (default is 10)
            
        Returns:
            Process: self
        """
        prev_status = self.status 
        while True:
            if self.status != prev_status:
                if self.status == ProcessStatus.PROC_RUNNING:
                    self._client.logger.info("Process started")
                elif self.status == ProcessStatus.PROC_RETRY:
                    self._client.logger.warning("Process failed, retry")
                elif self.status == ProcessStatus.PROC_ERROR:
                    self._client.logger.error("Process error")
                    break
                elif self.status == ProcessStatus.PROC_SUCCESS:
                    self._client.logger.info("Process sucessed")
                    break
            sleep(refresh_rate)
            prev_status = self.status
            self.update()
        return self
    
class ProcessList(UserList):
    """A list of Processes
    
    Args:
        json_obj (object): The parsed json
        client (Client): The client to request the api
    """
    def __init__(self, json_obj, client):
        self.data = []
        self._client = client
        for obj in json_obj:
            self.data.append(Process(obj, self._client))
        
from .session import ASession, Session

class SessionOverview(ASession):
    """The session overview
    
    Args:
        json_obj (object): The parsed json
        client (Client): The client to request the api
    """
    def __init__(self, json_obj, client):
        super().__init__(client, json_obj['id'])
        self.uri = json_obj['uri']
        self.rinex_filename = json_obj['rinex_filename']

    def __repr__(self):
       return "SessionOverview(id={})".format(self._id)
    
    def get(self):
        """Get the actual session
        
        Returns:
            Session: The actual session
        """
        json_obj = self._client.api_request("/session/%s" % (self._id))
        return Session(json_obj, self._client)
    
    
class Params:
    pass

class ParamsRineqc(Params):
    """The parameters for the diff algorithm
    
    Args:
        format (str): The session file format (default is None)
        antenna_height (float): The antenna height (default is None)
    """
    def __init__(self, format=None, antenna_height=None):
        if format is not None:
            self.format = format
        if antenna_height is not None:
            self.antenna_height = antenna_height
    
    def _from_json(json_obj):
        return ParamsRineqc(json_obj.get('format'), json_obj.get('antenna_height'))
 
class ParamsDiff(Params):
    """The parameters for the diff algorithm
    
    Args:
        mode (str): The mode parameter (default is None)
        bases (str): The base parameter (default is None)
        bases_source (str or list(str)): The bases source parameter. If parameter is string the separator is '|' (default is None)
        n (int): The n parameter (default is None)
        m (int): The m parameter (default is None)
        reject (str or list(str)): The reject parameter. If parameter is string the separator is '|' (default is None)
    """
    def __init__(self, mode=None, bases=None, bases_source=None, n=None, m=None, reject=None):
        self.mode = mode
        if isinstance(bases, str) and bases != 'auto':
            self.bases = bases.split('|')
        else:
            self.bases = bases
        self.bases_source = bases_source
        self.n = n
        self.m = m
        if isinstance(reject, str):
            self.reject = reject.split('|')
        else:
            self.reject = reject
    
    def _from_json(json_obj):
        kwargs = {'mode': json_obj['mode'], 'bases': json_obj['bases'], 'bases_source': json_obj['bases_source'],
                  'n': json_obj.get('n'), 'm': json_obj.get('m'), 'reject': json_obj['reject']}
        return ParamsDiff(**kwargs)
          
    def __repr__(self):
        return "ParamDiff(mode={}, bases={}, bases_source={}, n={}, m={}, reject={})".format(
                self.mode, self.bases, self.bases_source, self.n, self.m, self.reject)
    
    def to_dict(self):
        """Repsent the object as a dict
        
        Returns:
            dict(str,object): the dict
        """
        ret = {}
        if self.mode is not None:
            ret['mode'] = self.mode
        if isinstance(self.bases, list):
            ret['bases'] = '|'.join(self.bases)
        elif self.bases is not None:
            ret['bases'] = self.bases
        if self.n is not None:
            ret['n'] = self.n
        if self.m is not None:
            ret['m'] = self.m
        if self.reject is not None:
            ret['reject'] = '|'.join(self.reject)
        return ret

class ParamsPPP(Params):
    """The parmaeters for the ppp algorithm
    
    Args:
        mode (str): The mode parameter (default is None)
    """
    def __init__(self, mode=None):
        self.mode = mode
            
    def _from_json(json_obj):
        return ParamsPPP(json_obj['mode'])
        
    def __repr__(self):
        return "ParamPPP(mode={})".format(self.mode)
    
    def to_dict(self):
        """Repsent the object as a dict
        
        Returns:
            dict(str,object): the dict
        """
        ret = {}
        if self.mode is not None:
            ret["mode"] = self.mode
        return ret

class ParamsVrs(Params):
    """The parameters for the vrs algorithm
    
    Args:
        name (str): The name of the virtual session
        lat (float): The latitude parameter
        lg (float): The longitude parameter
        first_epoch (datetime or str): The first epoch. If the paramter is a string the format should be "%Y%m%d%H%M" or "%Y-%m-%d %H:%M:%S"
        last_epoch (datetime or str): The last epoch. If the paramter is a string the format should be "%Y%m%d%H%M" or "%Y-%m-%d %H:%M:%S"
        rate (int): The rate parameter
    """
    def __init__(self, name, lat, lg, first_epoch, last_epoch, rate, h=None, hq=None, reject=None, session_id=None):
        self.name = name
        self.lat = lat
        self.lg = lg
        if isinstance(first_epoch, str):
            if len(first_epoch) == 12:
                self.first_epoch = datetime.strptime(first_epoch, "%Y%m%d%H%M")
            else:
                self.first_epoch = datetime.strptime(first_epoch, "%Y-%m-%d %H:%M:%S")
        else:
            self.first_epoch = first_epoch
        if isinstance(last_epoch, str):
            if len(last_epoch) == 12:
                self.last_epoch = datetime.strptime(last_epoch, "%Y%m%d%H%M")
            else:
                self.last_epoch = datetime.strptime(last_epoch, "%Y-%m-%d %H:%M:%S")
        else:
            self.last_epoch = last_epoch
        self.rate = rate
        self.h = h
        self.hq = hq
        if isinstance(reject, str):
            self.reject = reject.split('|')
        else:
            self.reject = reject
        if session_id is not None:
            self.session_id = session_id
        
    def _from_json(json_obj):
        args = [json_obj['name'], json_obj['lat'], json_obj['lg'], 
                json_obj['first_epoch'], json_obj['last_epoch'], json_obj['rate']]
        kwargs = {'h': json_obj['h'], 'hq': json_obj['hq'], 'reject': json_obj['reject'], 'session_id': json_obj.get('session_id')}
        return ParamsVrs(*args, **kwargs)
        
        
    def __repr__(self):
        return "ParamVrs(name={}, lat={}, lg={}, first_epoch={}, last_epoch={}, rate={}, h={}, hq={}, reject={})".format(
                self.name, self.lat, self.lg, self.first_epoch, self.last_epoch, self.rate, self.h, self.hq, self.reject)
        
    def to_dict(self):
        """Repsent the object as a dict
        
        Returns:
            dict(str,object): The dict
        """
        first_epoch_str = self.first_epoch.strftime("%Y%m%d%H%M")
        last_epoch_str = self.last_epoch.strftime("%Y%m%d%H%M")
        ret = {'name': self.name, 'lat': self.lat, 'lg': self.lg, 'first_epoch': first_epoch_str,
               'last_epoch': last_epoch_str, 'rate': self.rate}
        if self.h is not None:
            ret['h'] = self.h
        if self.hq is not None:
            ret['hq'] = self.hq
        if self.reject is not None:
            ret['reject'] = "|".join(self.reject)
        return ret