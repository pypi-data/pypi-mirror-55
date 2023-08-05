# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 14:57:50 2019

@author: andres_c
"""

from collections import UserList
import simplekml
import geojson
from time import sleep
from datetime import datetime
from enum import Enum
import pandas as pd
from .utils import list_to_dict

class SessionStatus(Enum):
    """The session status"""
    PRE_WAITING = 100
    PRE_RUNNING = 101
    PRE_ERROR = 102
    PRE_SUCCESS = 103
    NAV_RUNNING = 104
    NAV_RETRY = 105
    NAV_SUCCESS = 106
    VRS_WAITING = 200
    VRS_RUNNING = 201
    VRS_ERROR = 202
    VRS_SUCCESS = 203
    SESS_DELETED = 999


class ASession():
    """An abstract class that containt the minimal Session data to request the api
    
    Args:
        client (Client): The client to request the api
        id (int): The session id
    """
    def __init__(self, client, id):
        self._client = client
        self._id = id
    
    def delete(self):
        """Delete this session"""
        self._client.api_request("/session/%d" % (self._id), method='delete')
    
    def getFile(self, file_type, save_to=''):
        """Get a file associated to the session
        
        Example:
            
        .. code-block:: python
            
            >>> session.getFile('nav', 'new_nav_file')
            
        
        Args:
            file_type (str): The file type, 'orig', 'obs' or 'nav', not case sensitive
            save_to (str): The path to save the file (default is '')

        Returns:
            list(byte) or ASession : The content of the file if save_to is '' or self
        """
        if file_type.lower() == 'orig':
            file_type = 'Orig'
        elif file_type.lower() == 'obs':
            file_type = 'Obs'
        elif file_type.lower() == 'nav':
            file_type = 'Nav'
        else:
            raise ValueError('file_type should be "orig", "obs" or "nav"')
        txt = self._client.api_request("/session/%d/Get%s" % (self._id, file_type), parse_resp=False)
        if save_to == '':
            return txt
        f = open(save_to, 'wb+')
        f.write(txt)
        f.close()
        return self
    
    def setAccess(self, access):
        """Set the access of the session, this method update self
                
        Example:
            
        .. code-block:: python
            
            >>> session.setAccess('public')
            
        Args:
            access (str): The access type, 'public' or 'private', not case sensitive

        Returns:
            ASession: self
        """
        if access.lower() == 'private':
            access = 'Private'
        elif access.lower() == 'public':
            access = 'Public'
        else:
            raise ValueError('file_type should be "public" or "private"')
        json_obj = self._client.api_request("/session/%d/Set%s" % (self._id, access), method='put')
        self.__init__(json_obj, self._client)
        return self
    
    def newProcess(self, algo, *args, params=None, wait=False, refresh_rate=10, **kwarg):
        """Create a new process for the session
       
        Example:
            
        .. code-block:: python
            
            >>> process = session.newProcess('ppp', mode='kinematic')
            
        
        Args:
            algo (str): The algorithm name 'ppp' or 'diff', case sensitive
            *args: The same parameter as ParamsPPP.__init__() or ParamsDiff.__init__(), used when params is None
            params(ParamsPPP or ParamsDiff): The parameters of the algorithm (default is None)
            wait (bool): wait for the process to finish (default is None)
            refresh_rate (int): The time in second between each update, used when wait is True (default is 10)
            **kwarg: The same parameters as ParamsPPP.__init__() or ParamsDiff.__init__(), used when params is None
        
        Returns:
            Process: The created Process
        """
        if algo == 'ppp':
            if params == None:
                params = ParamsPPP(*args, **kwarg)
            elif isinstance(params, ParamsPPP) == False:
                raise ValueError("algo is 'ppp' expected params to be ParamPPP")
        elif algo == 'diff':
            if params == None:
                params = ParamsDiff(*args, **kwarg)
            elif isinstance(params, ParamsDiff) == False:
                raise ValueError("algo is 'diff' expected params to be ParamDiff")
        else:
            raise ValueError("algo should be ppp or diff")
        json_obj = self._client.api_request("/process/%s/%d" % (algo, self._id),
                                             params=params.to_dict(), method='post')
        proc = Process(json_obj, self._client) 
        if wait:
            self._client.logger.info("Process created id:%d", proc._id)
            proc.wait(refresh_rate)
        return proc
     
    def virtualSession(self, name, wait=False, refresh_rate=10):
        """Create a virtual session
        
        Example:
            
        .. code-block:: python
            
            >>> vrs_session = session.virtualSession('MYVRS')
            
        
        Args:
            name (str): The session name
        
        Returns:
            Session: The created Session
        """
        params = {'name': name, 'session_id': self._id}
        json_obj = self._client.api_request('/session/vrs', params=params, method='post')
        sess = Session(json_obj, self)
        if wait:
            self.logger.info("VRS created id:%d", sess._id)
            sess.wait(refresh_rate)
        return sess


class Session(ASession):
    """A session
    
    Args:
        json_obj (object): The parsed json
        client (Client): The client to request the api
    """
    def __init__(self, json_obj, client):
        """A session
        
        Args:
            json_obj (object): The parsed json
            client (Client): The client to request the api
        """
        super().__init__(client, json_obj['id'])
        self.uri = json_obj['uri']
        self.antenna_type = json_obj['antenna_type']
        self.antenna_height = json_obj['antenna_height']
        self.receiver = json_obj['receiver']
        self.bands = json_obj['bands']
        self.delta_e = json_obj['delta_e']
        self.delta_n = json_obj['delta_n']
        self.h = json_obj['h']
        if json_obj['first_epoch'] != None:
            self.first_epoch = datetime.strptime(json_obj['first_epoch'], "%Y-%m-%d %H:%M:%S.%f")
        else:
            self.first_epoch = None
        if json_obj['last_epoch'] != None:
            self.last_epoch = datetime.strptime(json_obj['last_epoch'], "%Y-%m-%d %H:%M:%S.%f")
        else:
            self.last_epoch = None
        self.rate = json_obj['rate']
        self.lat = json_obj['lat']
        self.lg = json_obj['lg']
        self.station = json_obj['station']
        self.systems = json_obj['systems']
        self.original_filename = json_obj['original_filename']
        self.rinex_filename = json_obj['rinex_filename']
        self.posted_at = datetime.strptime(json_obj['posted_at'], "%a, %d %b %Y %H:%M:%S GMT")
        self.is_public = bool(json_obj['public'])
        self.public_url = json_obj['public_url']
        self.status = SessionStatus(json_obj['status'])
        self.processes = []
        for json_process in json_obj['processes']:
            self.processes.append(ProcessOverview(json_process, client))
    
    def __repr__(self):
       return "Session(id={})".format(self._id)
   
    def update(self):
        """Update the object data
        
        Returns:
            Session: self
        """
        json_obj = self._client.api_request("/session/%d" % (self._id))
        self.__init__(json_obj, self._client)
        return self
    
    def to_dict(self):
        ret = {'lat': self.lat, 'lg': self.lg, 'h': self.h, 
               'first_epoch': self.first_epoch.strftime("%Y-%m-%d %H:%M:%S.%f"),
               'last_epoch': self.last_epoch.strftime("%Y-%m-%d %H:%M:%S.%f"),
               'rate': self.rate, 'delta_n': self.delta_n, 'delta_e': self.delta_e,
               'bands': self.bands, 'station': self.station, 'systems': self.systems,
               'original_filename': self.original_filename, 'rinex_filename': self.rinex_filename,
               'posted_at': self.posted_at.strftime("%a, %d %b %Y %H:%M:%S GMT"), 'status': self.status.value,
               'is_public': self.is_public, 'public_url': self.public_url, 'uri': self.uri}
        return ret
    
    def wait(self, refresh_rate=10, wait_retry='ask'):
        """Wait for the preprocessing of the session to finsh
        
        Args:
            refresh_rate (int): The time in second between each update (default is 10)
            wait_retry (str): Should it wait for the preprocessing to retry (default is ask)
            
        Returns:
            Session: self
        """
        prev_status = self.status
        while True:
            if self.status != prev_status:
                if self.status == SessionStatus.SESS_DELETED:
                    self._client.logger.error("Session is deleted")
                    break
                elif self.status == SessionStatus.NAV_RETRY:
                    self._client.logger.warning("Failed to obtain navigation data, retry in 1 hours")
                    while wait_retry not in ['y', 'yes' 'ye', 'n', 'no', '']:
                        wait_retry = input("Do you want to wait [y/N] ").lower()
                    if wait_retry[0] == 'y':
                        sleep(3600)
                    else:
                        break
                elif self.status == SessionStatus.PRE_RUNNING:
                    self._client.logger.info("Start preprocessing")
                elif self.status == SessionStatus.PRE_ERROR:
                    self._client.logger.error("Preprocessing error, session will be deleted")
                    break
                elif self.status == SessionStatus.PRE_SUCCESS:
                    self._client.logger.info("Preprocessing sucessed")
                elif self.status == SessionStatus.NAV_RUNNING:
                    self._client.logger.info("Start navigation")
                elif self.status == SessionStatus.NAV_SUCCESS:
                    self._client.logger.info("Navigation sucessed")
                    break
                elif self.status == SessionStatus.VRS_RUNNING:
                    self._client.logger.info("Start VRS processing")
                elif self.status == SessionStatus.VRS_ERROR:
                    self.logger.error("VRS error")
                    break
                elif self._client.status == SessionStatus.VRS_SUCCESS:
                    self.logger.info("VRS sucessed")
                    break
            sleep(refresh_rate)
            prev_status = self.status
            self.update()
        return self

class SessionList(UserList):
    """A list of Session
    
    Args:
        json_obj (object): The parsed json
        client (Client): The client to request the api
    """
    def __init__(self, json_obj, client):
        self.data = []
        self._client = client
        for obj in json_obj:
            self.data.append(Session(obj, self._client))
    
    def df(self):
        """Format the object to pandas DataFrame
        
        Returns:
            pandas.DataFrame: The DataFrame
        """
        data = list_to_dict(self.data, 'lat', 'lg', 'h', 'first_epoch:%Y-%m-%d %H:%M:%S.%f', 
                            'last_epoch:%Y-%m-%d %H:%M:%S.%f', 'rate', 'delta_n', 'delta_e',
                            'bands', 'station', 'systems', 'original_filename', 'rinex_filename',
                            'posted_at:%a, %d %b %Y %H:%M:%S GMT', 'status', 'is_public', 'public_url', 'uri')
        ids = [d._id for d in self.data]
        df = pd.DataFrame(data, ids)
        return df
        
    def to_csv(self, path_or_buf=None, sep=','):
        """Format and save the object to a csv file
        
        Example:
            
        .. code-block:: python
            
            >>> sessions.to_csv('sessions.csv')
            
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
            sep (str): the csv separator (default is ',')
        
        Returns:
            str or None : Return the csv as a string is path_or_buf is None
        """
        return self.df().to_csv(path_or_buf, sep)
    
    def to_kml_obj(self, kml=None):
        """Format the object to a kml object
        
        Args:
            kml (object): The kml object, if None a kml object is created (default is None)
        
        Returns:
            object : Return the kml object
        """
        if kml is None:
            kml = simplekml.Kml()
        for d in self.data:
            if d.lg is not None and d.lat is not None and d.h is not None:
                pt = kml.newpoint(name=d.original_filename, coords=[(d.lg, d.lat, d.h)], 
                    timestamp=simplekml.TimeStamp(d.first_epoch.strftime("%Y-%m-%dT%H:%M:%S")), altitudemode='absolute')
                pt.extendeddata = simplekml.ExtendedData()
                sess_tab = "<table>"
                pt.extendeddata.newdata("session_id", d._id)
                sess_tab += "<tr><th>ID</th><td>$[session_id]</td></tr>"
                names_dict = {'lat':'Latiude (deg)', 'lg': 'Longitude (deg)', 'h': 'Height (meter)',
                              'first_epoch': 'First Epoch (GPS time)', 'last_epoch': 'Last Epoch (GPS time)', 'rate': 'Rate (second)',
                              'delta_n': 'Delta N (meter)', 'delta_e': 'Delta E (meter)', 'bands' : 'Bands', 'station': 'Station',
                              'systems': 'Systems', 'original_filename': 'Original Filename', 'rinex_filename': 'Rinex Filename',
                              'posted_at': 'Posted At', 'status': 'Status', 'is_public': 'Public', 'public_url': 'Public URL', 'uri': 'URI'}
                for k, v in d.to_dict().items():
                    sess_tab += "<tr><th>"+names_dict[k]+"</th><td>$["+k+"]</td></tr>"
                    pt.extendeddata.newdata(k, v)
                sess_tab +=  "</table>"
                pt.extendeddata.newdata("nb_processes", len(d.processes))
                i = 0
                process_tab = "<table><tr><th>ID</th><th>Algorithm</th><th>Status</th><th>Posted At</th><th>URI</th></tr>"
                for p in d.processes:
                    name = 'process_%d' % (i) 
                    pt.extendeddata.newdata(name+'_id', p._id)
                    pt.extendeddata.newdata(name+'_algo', p.algo)
                    pt.extendeddata.newdata(name+'_status', p.status.value)
                    pt.extendeddata.newdata(name+'_posted_at', p.posted_at.strftime("%a, %d %b %Y %H:%M:%S GMT"))
                    pt.extendeddata.newdata(name+'_uri', p.uri)
                    process_tab += "<tr><td>$["+name+"_id]</td><td>$["+name+"_algo]</td><td>$["+name+"_status]</td>"
                    process_tab += "<td>$["+name+"_posted_at]</td><td>$["+name+"_uri]</td></tr>"
                    i += 1
                process_tab += "</table>"
                css="""<head>
                        <style>
                        table, th, td {
                          border: 1px solid black;
                          border-collapse: collapse;
                        }
                        th, td {
                          padding: 5px;
                          text-align: left;    
                        }
                        </style>
                        </head>
                        <body>
                """
                pt.balloonstyle.text = css+"<body><h3>Session :</h3>"+sess_tab+"<h3>Processes :</h3>"+process_tab+"</body>"
        return kml
                    
    def to_kml(self, path_or_buf=None):
        """Format and save the object to a kml file
        
        Example:
            
        .. code-block:: python
            
            >>> sessions.to_kml('sessions.kml')
            
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
        
        Returns:
            str or None : Return the kml as a string if path_or_buf is None
        """
        kml = self.to_kml_obj()
        if path_or_buf is None:
            return kml.kml()
        elif isinstance(path_or_buf, str):
            kml.save(path_or_buf)
        else:
            path_or_buf.write(kml.kml())
            
    def to_kmz(self, path):
        """Format and save the object to a kmz file
        
        Example:
            
        .. code-block:: python
            
            >>> sessions.to_kmz('sessions.kmz')
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
        """
        kml = self.to_kml_obj()
        kml.savekmz(path)
    
    def to_geojson_obj(self, geojson_obj=None):
        """Format the object to a geojson file
        
        Args:
            geojson_obj (object): The geojson object, if None a geojson object is created (default is None)
        
        Returns:
            object : The geojson object
        """ 
        if geojson_obj == None:
            geojson_obj = geojson.FeatureCollection([])
        for d in self.data:
            if d.lg is not None and d.lat is not None and d.h is not None:
                prop = d.to_dict()
                prop['processes'] = []
                for p in d.processes:
                    prop['processes'].append({'id': p._id, 'algo': p.algo, 'status': p.status.value, 
                        'posted_at': p.posted_at.strftime("%a, %d %b %Y %H:%M:%S GMT"), 'uri': p.uri})
                geojson_obj['features'].append(geojson.Feature(geometry=geojson.Point((d.lg, d.lat, d.h)), properties=prop))
        return geojson_obj
        
        
    def to_geojson(self, path_or_buf=None):
        """Format and save the object to a geojson file

        Example:
            
        .. code-block:: python
            
            >>> sessions.to_geojson('sessions.json')
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
        
        Returns:
            str or None : Return the geojson as a string if path_or_buf is None
        """
        geo_obj = self.to_geojson_obj()
        if path_or_buf is None:
            return geojson.dumps(geo_obj)
        elif isinstance(path_or_buf, str):
            f = open(path_or_buf, 'w+')
            geojson.dump(geo_obj, f)
            f.close()
        else:
            geojson.dump(geo_obj, path_or_buf)
    
       
from .process import AProcess, Process, ProcessStatus, ParamsDiff, ParamsPPP

class ProcessOverview(AProcess):
    """The process overview

    Args:
        json_obj (object): The parsed json
        client (Client): The client to request the api
    """
    def __init__(self, json_obj, client):
        super().__init__(client, json_obj['id'])
        self.status = ProcessStatus(json_obj['status'])
        self.algo = json_obj['algo']
        self.uri = json_obj['uri']
        self.posted_at = datetime.strptime(json_obj['posted_at'],  "%a, %d %b %Y %H:%M:%S GMT")
        
    def __repr__(self):
         return "ProcessOverview(id={}, algo={})".format(self._id, self.algo)
    
    def get(self):
        """Get the actual process
        
        Returns:
            Process: The actual process
        """
        json_obj = self._client.api_request("/process/%s" % (self._id))
        return Process(json_obj, self._client)