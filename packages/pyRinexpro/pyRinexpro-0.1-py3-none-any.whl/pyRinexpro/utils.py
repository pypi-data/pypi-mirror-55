# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:25:15 2019

@author: andres_c
"""

def list_to_dict(obj_list, *args):
    ret = {}
    for a in args:
        ret[a.split(':')[0]] = []
    for a in args:
        splits = a.split(':', 1)
        if len(splits) > 1:
            for obj in obj_list:
                attr = obj.__getattribute__(splits[0])
                if attr is not None:
                    ret[splits[0]].append(("{:" + splits[1] + "}").format(attr))
                else:
                    ret[splits[0]].append(None)
        else:
            for obj in obj_list:
                ret[splits[0]].append(obj.__getattribute__(splits[0]))
    return ret
