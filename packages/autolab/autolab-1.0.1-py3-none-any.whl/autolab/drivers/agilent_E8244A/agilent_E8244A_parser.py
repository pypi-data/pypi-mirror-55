#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import agilent_E8244A as MODULE
from argparse import ArgumentParser


class Driver_parser():
    def __init__(self,args,utilities,**kwargs):
        self.utilities = utilities
        """Set the connection up"""
        self.classes_list = self.utilities.list_classes(MODULE)
        Driver_class      = self.utilities.identify_device_class(MODULE,self.classes_list,args.connection)
        
        # pass the argument board_index or libpath argument through port one
        kwargs = self.utilities.parsekwargs_connectiondependant(kwargs=kwargs,Driver_class=Driver_class)
        self.Instance     = Driver_class(address=args.address,**kwargs)
        
        self.methods_list = self.utilities.list_methods(self.Instance)
        
        
    def add_parser_arguments(self,parser):
        """Add arguments and help to the parser passed as input"""
        usage = f"""
----------------  Driver informations:  ----------------
{self.help()}

----------------  Examples:  ----------------

usage:    autolab-drivers [options] arg 
            
    autolab-drivers -D {MODULE.__name__} -A TCPIP::192.168.0.4::INSTR -C VISA -a 0.5 -f 500
    load {MODULE.__name__} driver using VISA communication protocol with address TCPIP... and set the amplitude to 0.5V and frequency to 500Hz.
    
    autolab-drivers -D nickname -a 0.5 -f 500
    same as before but using the device nickname as defined in local_config.ini
    
    autolab-drivers -D nickname -m some_methods1,arg1,arg2=23 some_methods2,arg1='test'
    Execute some_methods of the driver. A list of available methods is present at the top of this help along with arguments definition.
            """
        parser = ArgumentParser(usage=usage,parents=[parser])
        parser.add_argument("-a", "--amplitude", type=str, dest="amplitude", default=None, help="Set the amplitude." )
        parser.add_argument("-f", "--frequency", type=str, dest="frequency", default=None, help="Set the frequency." )
        
        return parser

    def do_something(self,args):
        if args.amplitude:
            getattr(self.Instance,'amplitude')(args.amplitude)
        if args.frequency:
            getattr(self.Instance,'frequency')(args.frequency)
        if args.methods:
            methods = [args.methods[i].split(',') for i in range(len(args.methods))]
            message = self.utilities.parse_commands(self.Instance,methods,self.methods_list)

    def help(self):
        """Add to the help lists of module: classes, methods and arguments"""
        classes_list = self.utilities.print_help_classes(self.classes_list)                  # display list of classes in module
        methods_list = self.utilities.print_help_methods(self.methods_list)                  # display list of methods in module
        methods_args = self.utilities.print_help_methods_arguments(self.Instance,self.methods_list)      # display list of methods arguments
        return classes_list + methods_list + methods_args

    def exit(self):
        self.Instance.close()
