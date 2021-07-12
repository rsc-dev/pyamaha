#!/usr/bin/env python

__author__      = 'Radoslaw Matusiak'
__copyright__   = 'Copyright (c) 2017 Radoslaw Matusiak'
__license__     = 'MIT'
__version__     = '0.3'

import cmd
import pprint
import sys
from functools import wraps

from pyamaha import Device, System, Zone

DEV = None

def device_decorator(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if DEV is not None:
            func(*args, **kwargs)
        else:
            print('[!] Please set device ip with "device" command.')
    return func_wrapper
# end-of-function


class BaseCmds():
    def do_exit(self, _):
        """
        Exit.

        Usage: exit <enter>
        """
        sys.exit(0)
    # end-of-method do_exit

    def do_back(self, _):
        """
        Exit submenu.

        Usage: back <enter>
        """
        return True
    # end-of-method do_back

    def do_device(self, ip):
        """
        Set device IP.

        Usage: device <ip> <enter>
        """
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
        """
        For retrieving basic information of a Device.

        Usage: getDeviceInfo <enter>
        """
        resp = DEV.request(System.get_device_info())
        pprint.pprint(resp.json())
    # end-of-method do_getDeviceInfo

    @device_decorator
    def do_getFeatures(self, _):
        """
        For retrieving feature information equipped with a Device.

        Usage: getFeatures <enter>
        """
        resp = DEV.request(System.get_features())
        pprint.pprint(resp.json())
    # end-of-method getFeatures

    @device_decorator
    def do_getNetworkStatus(self, _):
        """
        For retrieving network related setup/information.

        Usage: getNetworkStatus <enter>
        """
        resp = DEV.request(System.get_network_status())
        pprint.pprint(resp.json())
    # end-of-method getNetworkStatus

    @device_decorator
    def do_getFuncStatus(self, _):
        """
        For retrieving setup/information of overall system function.
        Parameters are readable only when corresponding functions are available in "func_list" of /system/getFeatures.

        Usage: getFuncStatus <enter>
        """
        resp = DEV.request(System.get_network_status())
        pprint.pprint(resp.json())
    # end-of-method getFuncStatus

    @device_decorator
    def do_setAutoPowerStandby(self, enable):
        """
        For setting Auto Power Standby status.
        Actual operations/reactions of enabling Auto Power Standby depend on each Device.

        Usage: setAutoPowerStandby <true|false> <enter>
        """
        enable = True if enable == 'true' else False
        resp = DEV.request(System.set_autopower_standby(enable))
        pprint.pprint(resp.json())
    # end-of-method setAutoPowerStandby

    @device_decorator
    def do_getLocationInfo(self, _):
        """
        For retrieving Location information.

        Usage: getLocationInfo <enter>
        """
        resp = DEV.request(System.get_location_info())
        pprint.pprint(resp.json())
    # end-of-method getLocationInfo

    @device_decorator
    def do_sendIrCode(self, code):
        """
        For sending specific remote IR code.
        A Device is operated same as remote IR code reception. But continuous IR code cannot be used in this command.
        Refer to each Device's IR code list for details..

        Usage: sendIrCode <code> <enter>
        """
        code = code.strip()
        resp = DEV.request(System.send_ir_code(code))
        pprint.pprint(resp.json())
    # end-of-method sendIrCode

    @device_decorator
    def do_setWiredLan(self, line):
        """
        For setting Wired Network. Network connection is switched to wired by using this API. If no
        parameter is specified, current parameter is used. If set parameter is incomplete, it is possible not
        to provide network avalability.

        Usage: setWiredLan [dhcp=<true|false>] [ip_address=] [subnet_mask=] [default_gateway=] [dns_server_1=] [dns_server_2=] <enter>
        Example: setWiredLan dhcp=false dns_server_2=8.8.4.4 <enter>
        """
        data = {'dhcp':None, 'ip_address':None, 'subnet_mask':None, 'default_gateway':None, 'dns_server_1':None, 'dns_server_2':None}

        args = line.split()
        for arg in args:
            k, v = arg.split('=')
            if k in data.keys():
                data[k] = v

        resp = DEV.request(System.set_wired_lan(**data))
        pprint.pprint(resp.json())
    # end-of-method do_setWiredLan

    @device_decorator
    def do_setWirelessLan(self, line):
        pass
    # end-of-method do_setWirelessLan

    pass
# end-of-class System

class ZoneCli(cmd.Cmd, BaseCmds):
    PROMPT = 'zone'

    def __init__(self, top):
        cmd.Cmd.__init__(self)
        self.prompt = '{}\{}>'.format(top, ZoneCli.PROMPT)
    # end-of-method __init__

    @device_decorator
    def do_setPower(self, line):
        """
        For setting power status of each Zone.
        If no parameter is specified: Default zone=main and power=toggle

        Usage: do_setPower [zone=<main|zone2|zone3|zoneN>] [power=<on|standby|toggle>] <enter>
        Example: do_setPower zone=main power=on <enter>
        """
        data = {'zone':'main', 'power':'toggle'}

        args = line.split()
        for arg in args:
            k, v = arg.split('=')
            if k in data.keys():
                data[k] = v

        resp = DEV.request(Zone.set_power(**data))
        pprint.pprint(resp.json())
    # end-of-method do_setPower

    @device_decorator
    def do_getSceneInfo(self, line):
        """
        For retrieving possible scene values
        If no parameter is specified: Default zone=main

        Usage: do_getSceneInfo [zone=<main|zone2|zone3|zoneN>] <enter>
        Example: do_getSceneInfo zone=main <enter>
        """
        data = {'zone':'main'}

        args = line.split()
        for arg in args:
            k, v = arg.split('=')
            if k in data.keys():
                data[k] = v

        resp = DEV.request(Zone.get_scene_info(**data))
        pprint.pprint(resp.json())

    # end-of-method do_getSceneInfo

    @device_decorator
    def do_setScene(self, line):
        """
        For setting the current scene
        If no parameter is specified: Default zone=main and scene=1

        Usage: do_setScene [zone=<main|zone2|zone3|zoneN>] [scene=<1,2,..8>] <enter>
        Example: do_getSceneInfo zone=main scene=1 <enter>
        """
        data = {'zone':'main', 'scene':1}

        args = line.split()
        for arg in args:
            k, v = arg.split('=')
            if k in data.keys():
                data[k] = v

        resp = DEV.request(Zone.set_scene(**data))
        pprint.pprint(resp.json())

    # end-of-method do_setScene

    pass
# end-of-class Zone

class RootCli(cmd.Cmd, BaseCmds):
    PROMPT = 'yxc'

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '{}>'.format(RootCli.PROMPT)
    # end-of-method __init__

    def do_system(self, _):
        """
        System submenu.

        Usage: system <enter>
        """
        system = SystemCli(RootCli.PROMPT)
        system.cmdloop()
    # end-of-method do_system

    def do_zone(self, _):
        """
        Zone submenu.

        Usage: system <enter>
        """
        zone = ZoneCli(RootCli.PROMPT)
        zone.cmdloop()
    # end-of-method do_zone

    def do_back(self, _):
        """
        Nothing.

        Usage: back <enter>
        """
        pass
    # end-of-method do_back

    pass
# end-of-class Root

if __name__ == '__main__':
    r = RootCli()
    r.cmdloop()