#!/usr/bin/env python

__author__      = 'Radoslaw Matusiak'
__copyright__   = 'Copyright (c) 2017 Radoslaw Matusiak'
__license__     = 'MIT'
__version__     = '0.1'

import cmd
import pprint
import sys
from functools import wraps

from pyamaha import Device, System

DEV = None

def device_decorator(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if DEV is not None:
            func(*args, **kwargs)
        else:
            print '[!] Please set device ip with "device" command.'
    return func_wrapper
# end-of-function
    

class BaseCmds():
    def do_exit(self, _):
        sys.exit(0)
    # end-of-method do_exit
    
    def do_back(self, _):
        return True
    # end-of-method do_back
    
    def do_device(self, ip):
        global DEV
        ip = ip.strip()
        DEV = Device(ip)
    # end-of-method do_device
    
    pass
# end-of-class BaseCmds    


class SystemCli(cmd.Cmd, BaseCmds):
    PROMPT = 'system'
    
    def __init__(self, top):
        cmd.Cmd.__init__(self)
        self.prompt = '{}\{}>'.format(top, SystemCli.PROMPT)
    # end-of-method __init__
    
    @device_decorator
    def do_getDeviceInfo(self, _):
        resp = DEV.request(System.get_device_info())
        pprint.pprint(resp.json())
    # end-of-method do_getDeviceInfo
    
    @device_decorator    
    def do_getFeatures(self, _):
        resp = DEV.request(System.get_features())
        pprint.pprint(resp.json())
    # end-of-method getFeatures    
    
    @device_decorator    
    def do_getNetworkStatus(self, _):
        resp = DEV.request(System.get_network_status())
        pprint.pprint(resp.json())
    # end-of-method getNetworkStatus    
    
    @device_decorator
    def do_getFuncStatus(self, _):
        resp = DEV.request(System.get_network_status())
        pprint.pprint(resp.json())
    # end-of-method getFuncStatus    
    
    @device_decorator
    def do_setAutoPowerStandby(self, _):
        resp = DEV.request(System.set_autopower_standby())
        pprint.pprint(resp.json())
    # end-of-method setAutoPowerStandby    
    
    @device_decorator
    def do_getLocationInfo(self, _):
        resp = DEV.request(System.get_location_info())
        pprint.pprint(resp.json())
    # end-of-method getLocationInfo    
    
    @device_decorator
    def do_sendIrCode(self, code):
        code = code.strip()
        resp = DEV.request(System.send_ir_code(code))
        pprint.pprint(resp.json())
    # end-of-method sendIrCode     
    
    pass
# end-of-class System    


class RootCli(cmd.Cmd, BaseCmds):
    PROMPT = 'yxc'
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '{}>'.format(RootCli.PROMPT)
    # end-of-method __init__
    
    def do_discover(self, _):
        raise NotImplementedError()
    # end-of-method do_discover    
    
    def do_show(self, _):
        raise NotImplementedError()
    # end-of-method do_show
    
    def do_system(self, _):
        system = SystemCli(RootCli.PROMPT)
        system.cmdloop()
    # end-of-method do_system
    
    def do_back(self, _):
        pass
    # end-of-method do_back
    
    pass
# end-of-class Root

if __name__ == '__main__':
    r = RootCli()
    r.cmdloop()