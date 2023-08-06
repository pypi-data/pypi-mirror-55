# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 10:47:39 2019

@author: andres_c
"""

from collections import UserList
from datetime import datetime
import pandas as pd
import simplekml
import geojson
import math

class RepType:
    Points = 1 
    LineString = 1 << 1
    Camera = 1 << 2
    Track = 1 << 3
    
    PointsLine = LineString | Points
    PointsCam = Points | Camera
    PointsTrack = Points | Track
    LineCam = LineString | Camera
    LineTrack = LineString | Track
    TrackCam = Track | Camera
    
    def __init__(self, str):
        self.rep = 0
        for s in str.split('|'):
            if s == 'Points':
                self.rep |= RepType.Points
            elif s == 'LineString':
                self.rep |= RepType.LineString
            elif s == 'Camera':
                self.rep |= RepType.Camera
            elif s == 'Track':
                self.rep |= RepType.Track
            else:
                raise ValueError('In "%s" invalid value "%s" for RepType expected "Points", "LineString", "Camera" and/or "Track"' % (str, s))
        
class Crs:
    """A crs
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.ellipsoid = json_obj['ellipsoid']
        self.epoch = json_obj['epoch']
        if 'frame' in json_obj:
            self.frame = json_obj['frame']
        if 'frames' in json_obj:
            self.frames = []
            for f in json_obj['frames']:
                self.frames.append(f)

class Projection:
    """A projection
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.meridian_convergence = json_obj["meridian_convergence"]
        self.scale_factor = json_obj["scale_factor"]
        self.zone = json_obj["zone"]

class APosition:
    """An abstract class for position
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.cartesian = []
        for cart in json_obj['cartesian']:
            self.cartesian.append(cart)
        self.geographic = []
        for geo in json_obj['geographic']:
            self.geographic.append(geo)
        self.projection = Projection(json_obj['projection'])
        self.utm = []
        for utm in json_obj['utm']:
            self.utm.append(utm)

class ApproxPosition(APosition):
    """An approximated position
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)

class Position(APosition):
    """A postion
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        if 'quality' in json_obj:
            self.quality = []
            for quality in json_obj['quality']:
                self.quality.append(quality)
        if 'stddev_utm' in json_obj:
            self.stddev_utm = []
            for std in json_obj['stddev_utm']:
                self.stddev_utm.append(std)

class ATrajectoryElem:
    """An abstract class for a position of the trajectory"""
    def __init__(self, json_obj):
        """Initialize the object
        
        Args:
            json_obj (object): The parsed json
        """
        self.geographic = []
        for geo in json_obj['geographic']:
            self.geographic.append(geo)
        self.time = datetime.strptime(json_obj["time"], "%Y-%m-%d %H:%M:%S.%f")
    
    def to_dict(self):
        """Repsent the object as a dict
        
        Returns:
            dict(str,object): the dict
        """
        return {'lg': self.geographic[0], 'lat': self.geographic[1], 'h': self.geographic[2]}

class ApproxTrajectoryElem(ATrajectoryElem):
    """One approximated position of the trajectory        
        
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        
    def to_dict(self, inc_coord=True):
        """Repsent the object as a dict
        
        Args:
            inc_coord (bool): Include the coords in the dict (default is True)
        
        Returns:
            dict(str,object): object: the dict
        """
        if inc_coord == True:
            ret = super().to_dict()
        else:
            ret = {}
        return ret
            
class TrajectoryElem(ATrajectoryElem):
    """One position of the trajectory
        
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.stddev_utm = []
        for dev in json_obj["stddev_utm"]:
            self.stddev_utm.append(dev)
        self.nb_fixed_sat = json_obj["nb_fixed_sat"]
        self.nb_sat = json_obj["nb_sat"]
        self.pdop = json_obj["pdop"]
        self.solution = json_obj["solution"]
    
    def to_dict(self, inc_coord=True):
        """Repsent the object as a dict
        
        Args:
            inc_coord (bool): Include the coords in the dict (default is True)
        
        Returns:
            dict(str,object): the dict
        """
        if inc_coord == True:
            ret = super().to_dict()
        else:
            ret = {}
        ret['stddev_utm_e'] = self.stddev_utm[0]
        ret['stddev_utm_n'] = self.stddev_utm[1]
        ret['stddev_utm_h'] = self.stddev_utm[2]
        ret['nb_fixed_sat'] = self.nb_fixed_sat
        ret['nb_sat'] = self.nb_sat
        ret['pdop'] = self.pdop
        ret['solution'] = self.solution
        return ret
    
class ATrajectory(UserList):
    """An abstract class for a trajectory"""

    def df(self):
        """Format the object to pandas DataFrame
        
        Returns:
            pandas.DataFrame: The DataFrame
        """
        df = pd.DataFrame()
        for l in self.data:
            df = df.append(pd.Series(l.to_dict(), name=l.time))
        return df
    
    def to_csv(self, path_or_buf=None, sep=','):
        """Format and save the object to a csv file
        
        Example:
        
        .. code-block:: python
            
            >>> trajectory.to_csv('trajectory.csv')
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
            sep (str): the csv separator (default is ',')
        
        Returns:
            str or None : The csv as a string is path_or_buf is None
        """
        return self.df().to_csv(path_or_buf, sep)
    
    def to_kml_obj(self, type='LineString', time_ratio=1.0, color='ff0000ff', kml=None):
        """Format the object to a kml object
        
        Args:
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
            time_ratio (float): The time ratio used only when type is 'Camera' (default is 1.0)
            color (str): The hexadecimal color with or without the alpha channel at the end (default is 'ff0000ff')
            kml (object): The kml object, if node a kml object is created (default is None)
        
        Returns:
            object : The kml object
        """
        if isinstance(type, str):
            type = RepType(type).rep
        if len(color) == 6:
            color += 'ff'
        if kml is None:
            kml = simplekml.Kml()
        style = simplekml.Style()
        style.iconstyle.color = simplekml.Color.hex(color[:-2])
        style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/open-diamond.png'
        style.linestyle.color = simplekml.Color.hexa(color)
        style.linestyle.width = 2
        style.labelstyle.scale = 0
        style_h = simplekml.Style()
        style_h.iconstyle.color = simplekml.Color.hex(color[:-2])
        style_h.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/open-diamond.png'
        style_h.linestyle.color = simplekml.Color.hexa(color)
        style_h.linestyle.width = 2
        style_h.labelstyle.scale = 1
        stylemap = simplekml.StyleMap(style, style_h)
        if type & RepType.Camera:
            tour = kml.newgxtour(name='camera')
            play = tour.newgxplaylist()
            heading = 0
            for i in range(0, len(self.data)):
                l = self.data[i]
                if i != len(self.data) - 1:
                    l1 = self.data[i + 1]
                    y = l1.geographic[0] - l.geographic[0]
                    x = l1.geographic[1] - l.geographic[1]
                    heading = math.degrees(math.atan2(y, x))
                    gxduration = (l1.time - l.time).total_seconds() * time_ratio
                camera = simplekml.Camera(latitude=l1.geographic[1], longitude=l1.geographic[0], altitude=l1.geographic[2],
                                             gxtimestamp=l.time.strftime("%Y-%m-%dT%H:%M:%S"), 
                                             tilt=90, altitudemode='absolute', heading=heading)
                fly = play.newgxflyto(gxduration=gxduration, camera=camera)
                fly._kml['gx:flyToMode'] = 'smooth'
        if type & RepType.Track:
            times = []
            coords = []
            for l in self.data:
                coords.append(tuple(l.geographic))
                times.append(l.time.strftime("%Y-%m-%dT%H:%M:%S"))
            trk = kml.newgxtrack()
            trk.newwhen(times)
            trk.newgxcoord(coords)
            trk.altitudemode = 'absolute'
            trk.style = style
            trk.extendeddata = simplekml.ExtendedData()
            for k, v in self.data[0].to_dict().items():
                trk.extendeddata.newdata(k, v)
        if type & RepType.LineString:
            coords = []
            for l in self.data:
                coords.append(tuple(l.geographic))
            lin = kml.newlinestring(coords=coords, altitudemode='absolute')
            lin.timespan.begin = self.data[0].time.strftime("%Y-%m-%dT%H:%M:%S")
            lin.timespan.end = self.data[-1].time.strftime("%Y-%m-%dT%H:%M:%S")
            lin.style = style
        if type & RepType.Points:
            for i in range(0, len(self.data)):
                l = self.data[i]
                if i % 100 == 0:
                    l2 = self.list[i + 100] if i + 100 < len(self.data) else self.data[-1]
                    name = l.time.strftime("%H:%M:%S") + " - " + l2.time.strftime("%H:%M:%S")
                    f = kml.newfolder(name=name)
                    f.visibility = 1 if int(i / 50) == 0 else 0
                pt = f.newpoint(name=l.time.strftime("%H:%M:%S"), coords=[tuple(l.geographic)], 
                                timestamp=simplekml.TimeStamp(l.time.strftime("%Y-%m-%dT%H:%M:%S")), altitudemode='absolute')
                pt.stylemap = stylemap
                pt.extendeddata = simplekml.ExtendedData()
                pt.visibility = 1 if int(i / 100) == 0 else 0
                for k, v in l.to_dict().items():
                    pt.extendeddata.newdata(k, v)
                i += 1
        return kml
    
    def to_kml(self, path_or_buf=None, type='LineString', time_ratio=1.0):
        """Format and save the object to a kml file
        
        Example:
        
        .. code-block:: python
            
            >>> trajectory.to_kml('trajectory.kml')
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
            time_ratio (float): The time ratio used only when type is 'Camera' (default is 1.0)
        
        Returns:
            str or None : The kml as a string if path_or_buf is None
        """
        kml = self.to_kml_obj(type, time_ratio)
        if path_or_buf is None:
            return kml.kml()
        elif isinstance(path_or_buf, str):
            kml.save(path_or_buf)
        else:
            path_or_buf.write(kml.kml())
            
    def to_kmz(self, path, type='LinesString', time_ratio=1.0):
        """Format and save the object to a kmz file
        
        Example:
        
        .. code-block:: python
            
            >>> trajectory.to_kmz('trajectory.kmz')
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
            type (str): The geojson object type can be 'LineString', 'Points' or 'Camera' (default is 'LineString')
            time_ratio (float): The time ratio used only when type is 'Camera' (default is 1.0)
        """
        kml = self.to_kml_obj(type, time_ratio)
        kml.savekmz(path)
        
    def to_geojson_obj(self, type='LineString', geojson_obj=None, name=''):
        """Format the object to a geojson file
        
        Args:
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
            name (str): The name of the object (default is '')
            geojson_obj (object): The geojson object, if None a geojson object is created (default is None)
        
        Returns:
            object : The geojson object
        """ 
        if isinstance(type, str):
            type = RepType(type).rep
        if geojson_obj == None:
            geojson_obj = geojson.FeatureCollection([])
        if type & RepType.LineString:
            coords = []
            for l in self.data:
                coords.append(tuple(l.geographic))
            geojson_obj['features'].append(geojson.Feature(geometry=geojson.LineString(coords), properties={'name':name}))
        if type & RepType.Points:
            i = 0
            for l in self.data:
                prop = l.to_dict(False)
                prop['time'] = l.time.strftime("%Y-%m-%d %H:%M:%S")
                prop['name'] = name
                if i % 50 == 0:
                    geojson_obj['features'].append(geojson.Feature(geometry=geojson.Point(tuple(l.geographic)),
                                                   properties=prop))
                i += 1
        return geojson_obj
        
        
    def to_geojson(self, path_or_buf=None, type='LineString'):
        """Format and save the object to a geojson file
        
        Example:
        
        .. code-block:: python
            
            >>> trajectory.to_geojson('trajectory.json')
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
        
        Returns:
            str or None : The geojson as a string if path_or_buf is None
        """
        geo_obj = self.to_geojson_obj(type)
        if path_or_buf is None:
            return geojson.dumps(geo_obj)
        elif isinstance(path_or_buf, str):
            f = open(path_or_buf, 'w+')
            geojson.dump(geo_obj, f)
            f.close()
        else:
            geojson.dump(geo_obj, path_or_buf)

class ApproxTrajectory(ATrajectory):
    """A list of approximated position that represent a trajectory
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.data = []
        for t in json_obj:
            self.data.append(ApproxTrajectoryElem(t))

class Trajectory(ATrajectory):
    """A list of position that represent a trajectory
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.data = []
        for t in json_obj:
            self.data.append(TrajectoryElem(t))

class Pcv:
    """The pcv
        
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        if 'receiver' in json_obj:
            self.receiver = json_obj['receiver']
        if 'receivers' in json_obj:
            if isinstance(json_obj['receivers'], dict):
                self.receivers_base = json_obj['receivers']['base']
                self.receivers_mobile = json_obj['receivers']['mobile']
            else:
                self.receivers = json_obj['receivers']
        self.satellites = json_obj['satellites']
    
class Product:
    """The product
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        if 'clocks' in json_obj:
            self.clocks = []
            for c in json_obj['clocks']:
                self.clocks = json_obj['clocks']
        if 'ionosphere' in json_obj:
            self.ionosphere = []
            for iono in json_obj['ionosphere']:
                self.ionosphere.append(iono)
        self.orbits = []
        for orbit in json_obj['orbits']:
            self.orbits.append(orbit)
        self.pcv = Pcv(json_obj['pcv'])
    
class Solution:
    """The solution
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.ambfix = json_obj["ambfix"]
        if not 'trajectory' in json_obj:
            self.baseline_azimut = json_obj["baseline_azimut"]
            self.baseline_dheight = json_obj["baseline_dheight"]
            self.baseline_length = json_obj["baseline_length"]
            self.baseline_xyz = []
            for xyz in json_obj["baseline_xyz"]:
                self.baseline_xyz.append(xyz)
        self.duration_hours = json_obj["duration_hours"]
        self.duration_minutes = json_obj["duration_minutes"]
        self.elevation_mask = json_obj["elevation_mask"]
        self.end_time = datetime.strptime(json_obj["end_time"], "%Y-%m-%d %H:%M:%S")
        self.interval = json_obj["interval"]
        self.number_frequencies = json_obj["number_frequencies"]
        self.pdop = []
        for pdop in json_obj["pdop"]:
            self.pdop.append(pdop)
        self.precise_eph = json_obj["precise_eph"]
        self.processing_type = json_obj["processing_type"]
        self.ref_antenna_height = json_obj["ref_antenna_height"]
        self.ref_antenna_type = json_obj["ref_antenna_type"]
        self.ref_llh = []
        for llh in json_obj["ref_llh"]:
            self.ref_llh.append(llh)
        self.ref_name_file = json_obj["ref_name_file"]
        self.ref_name_long = json_obj["ref_name_long"]
        self.ref_name_short = json_obj["ref_name_short"]
        self.ref_receiver = json_obj["ref_receiver"]
        self.ref_receiver_number = json_obj["ref_receiver_number"]
        self.ref_receiver_version = json_obj["ref_receiver_version"]
        self.ref_utm = []
        for utm in json_obj["ref_utm"]:
            self.ref_utm.append(utm)
        self.ref_xyz = []
        for xyz in json_obj["ref_xyz"]:
            self.ref_xyz.append(xyz)
        self.rov_antenna_height = json_obj["rov_antenna_height"]
        self.rov_antenna_type = json_obj["rov_antenna_type"]
        self.rov_name_file = json_obj["rov_name_file"]
        self.rov_name_long = json_obj["rov_name_long"]
        self.rov_name_short = json_obj["rov_name_short"]
        self.rov_receiver = json_obj["rov_receiver"]
        self.rov_receiver_number = json_obj["rov_receiver_number"]
        self.rov_receiver_version = json_obj["rov_receiver_version"]
        if not 'trajectory' in json_obj:
            self.reweighted_obs = json_obj["reweighted_obs"]
            self.rov_llh = []
            for llh in json_obj["rov_llh"]:
                self.rov_llh.append(llh)
            self.rov_utm = []
            for utm in json_obj["rov_utm"]:
                self.rov_utm.append(utm)
            self.rov_xyz = []
            for xyz in json_obj["rov_xyz"]:
                self.rov_xyz.append(xyz)
        self.s0 = json_obj["s0"]
        self.s0_m = json_obj["s0_m"]
        self.selected_frequencies = {}
        for k, v in json_obj["selected_frequencies"].items():
            self.selected_frequencies[k] = v
        self.solution_type = json_obj["solution_type"]
        self.start_time = datetime.strptime(json_obj["start_time"], "%Y-%m-%d %H:%M:%S")
        if not 'trajectory' in json_obj:
            self.solution_quality = json_obj["solution_quality"]
            self.stddev_utm = []
            for utm in json_obj["stddev_utm"]:
                self.stddev_utm.append(utm)
            self.stddev_xyz = []
            for xyz in json_obj["stddev_xyz"]:
                self.stddev_xyz.append(xyz)
        else:
            self.trajectory = Trajectory(json_obj['trajectory'])
                
        self.sv = []
        for sv in json_obj["sv"]:
            self.sv.append(sv)
        self.tropo_parameters = json_obj["tropo_parameters"]

class Atmo:
    """The atmo
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.G95 = json_obj['G95']
        self.I95 = json_obj['I95']
        self.doy = json_obj['doy']
        self.hour = json_obj['hour']
        self.nb_obs = json_obj['nb_obs']
    
class Baseline:
    """The baseline
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.amb_fixing = json_obj['amb_fixing']
        self.dist = json_obj['dist']
        self.ref = json_obj['ref']
        self.rov = json_obj['rov']
    
class Station:
    """The station
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.antenna = json_obj['antenna']
        self.dist_to_vrs = json_obj['dist_to_vrs']
        self.latitude = json_obj['latitude']
        self.longitude = json_obj['longitude']
        self.receiver = json_obj['receiver']
        self.station = json_obj['station']
        self.systems = json_obj['systems']
       
class Network:
    """The network
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.master = json_obj['master']
        self.atmo = []
        for atmo in json_obj['atmo']:
            self.atmo.append(Atmo(atmo))
        self.baselines = []
        for base in json_obj['baselines']:
            self.baselines.append(Baseline(base))
        self.stations = []
        for station in json_obj['stations']:
            self.stations.append(Station(station))

class Log:
    """The general logs data
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        self.history = []
        for hist in json_obj['history']:
            self.history.append(hist)
            
class LogRineqc(Log):
    """The log data for the rineqc algorithm
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.orig_file = json_obj['orig_file']
        self.obs_file = json_obj['obs_file']


class LogRinexnav(Log):
    """The log data for the rinexnav algorithm
        
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.nav_file = json_obj['nav_file']
        self.obs_file = json_obj['obs_file']
        self.trajectory = ApproxTrajectory(json_obj['trajectory'])
        self.position = ApproxPosition(json_obj['position'])
        

class LogPPP(Log):
    """The log data for the ppp algorithm
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.crs = Crs(json_obj['crs'])
        if 'position' in json_obj:
            self.position = Position(json_obj['position'])
        else:
            self.trajectory = Trajectory(json_obj['trajectory'])
        self.products = Product(json_obj['products'])
    
class LogDiff(Log):
    """The log data for the diff algorithm
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.crs = Crs(json_obj['crs'])
        if 'position' in json_obj:
            self.position = Position(json_obj['position'])
        else:
            self.trajectory = Trajectory(json_obj['trajectory'])
        self.products = Product(json_obj['products'])
        self.solutions = []
        for sol in json_obj['solutions']:
            self.solutions.append(Solution(sol))
            
     
    def to_kml_obj(self, type='LineString', time_ratio=1.0, kml=None):
        """Format the object to a kml object
        
        Args:
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
            time_ratio (float): The time ratio used only when type is 'Camera' (default is 1.0)
            kml (object): The kml object, if None a kml object is created (default is None)
        
        Returns:
            object : The kml object
        """
        if kml is None:
            kml = simplekml.Kml()
        fold = kml.newfolder(name='mean')
        self.trajectory.to_kml_obj(kml=fold, type=type, time_ratio=time_ratio, color='ffffff')
        solutions = kml.newfolder(name='solutions')
        i = 0
        colors = ['ff0000', '00ff00', 'ffff00', '00ffff', 'ff00ff', 'ff8800', '00bbff', 'bb00ff', 'b0bbb0', 'b0ffb0']
        for s in self.solutions:
            sol = solutions.newfolder(name='solution_%d'% (i))
            s.trajectory.to_kml_obj(kml=sol, type=type, time_ratio=time_ratio, color=colors[i%len(colors)])
            i+=1
        return kml
    
    def to_kml(self, path_or_buf=None, type='LineString', time_ratio=1.0):
        """Format and save the object to a kml file
        
        Example:
        
        .. code-block:: python
            
            >>> log.to_kml('diff-trajectory.kml')
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
            time_ratio (float): The time ratio used only when type is 'Camera' (default is 1.0)
        
        Returns:
            str or None : The kml as a string if path_or_buf is None
        """
        kml = self.to_kml_obj(type=type, time_ratio=time_ratio)
        if path_or_buf is None:
            return kml.kml()
        elif isinstance(path_or_buf, str):
            kml.save(path_or_buf)
        else:
            path_or_buf.write(kml.kml())
            
    def to_kmz(self, path, type='LinesString', time_ratio=1.0):
        """Format and save the object to a kmz file
        
        Example:
        
        .. code-block:: python
            
            >>> log.to_kmz('diff-trajectory.kmz')
        
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
            time_ratio (float): The time ratio used only when type is 'Camera' (default is 1.0)
        """
        kml = self.to_kml_obj(type, time_ratio)
        kml.savekmz(path)
        
    def to_geojson_obj(self, type='LineString', geojson_obj=None):
        """Format the object to a geojson file
        
        Args:
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
            geojson_obj (object): The geojson object, if None a geojson object is created (default is None)
        
        Returns:
            object : The geojson object
        """        
        if geojson_obj == None:
            geojson_obj = geojson.FeatureCollection([])
        self.trajectory.to_geojson_obj(geojson_obj=geojson_obj, type=type, name='mean')
        i = 0
        for s in self.solutions:
            s.trajectory.to_geojson_obj(geojson_obj=geojson_obj, type=type, name='solution_%d' % (i))
            i+=1
        return geojson_obj
    
    def to_geojson(self, path_or_buf=None, type='LineString'):
        """Format and save the object to a geojson file
        
        Example:
        
        .. code-block:: python
            
            >>> log.to_geojson('diff-trajectory.json')
            
        Args:
            path_or_buf (str or file): The path or the file-like object to save the file (default is None)
            type (str or RepType): Multiple type can be used with | or '|' for string (default is 'LineString')
        
        Returns:
            str or None : Return the geojson as a string if path_or_buf is None
        """
        geo_obj = self.to_geojson_obj(type)
        if path_or_buf is None:
            return geojson.dumps(geo_obj)
        elif isinstance(path_or_buf, str):
            f = open(path_or_buf, 'w+')
            geojson.dump(geo_obj, f)
            f.close()
        else:
            geojson.dump(geo_obj, path_or_buf)

class LogVrs(Log):
    """The log data for the vrs algorithm
    
    Args:
        json_obj (object): The parsed json
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.crs = Crs(json_obj['crs'])
        if 'position' in json_obj:
            self.position = ApproxPosition(json_obj['position'])
        self.products = Product(json_obj['products'])
        self.network = Network(json_obj['network'])