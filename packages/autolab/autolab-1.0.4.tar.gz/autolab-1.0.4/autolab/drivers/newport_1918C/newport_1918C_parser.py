#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import newport_1918C as MODULE
from argparse import ArgumentParser


class Driver_parser():
    def __init__(self,args,utilities,**kwargs):
        self.utilities = utilities
        """Set the connection up"""
        self.classes_list = self.utilities.list_classes(MODULE)
        Driver_class      = self.utilities.identify_device_class(MODULE,self.classes_list,args.connection)
        
        # pass the argument board_index or libpath argument through port one
        kwargs = self.utilities.parsekwargs_connectiondependant(kwargs=kwargs,Driver_class=Driver_class)
        self.Instance     = Driver_class(**kwargs)
        
        self.methods_list = self.utilities.list_methods(self.Instance)
        
        
    def add_parser_arguments(self,parser):
        """Add arguments and help to the parser passed as input"""
        usage = rf"""
        ----------------  Driver informations:  ----------------
        {self.help()}
        ----------------  Examples:  ----------------
        
        usage:    autolab-drivers [options] arg 
                
            autolab-drivers -D {MODULE.__name__} -C DLL --port C:\Program Files\Newport\Newport USB Driver\Bin\usbdll.dll -m some_methods,arg1,arg2
            In this particular case the --port option indicate the dll library location. Execute some_methods of the driver. A list of available methods is present at the top of this help along with arguments definition.
            
            autolab-drivers -D nickname -m some_methods1,arg1 some_methods2,arg1,arg2
            Same as before using the nickname defined in local_config.ini
            
            autolab-drivers -D nickname -m some_methods1,arg1,arg2=23 some_methods2,arg1='test'
            Execute some_methods of the driver. A list of available methods is present at the top of this help along with arguments definition."""
        
        parser = ArgumentParser(usage=usage,parents=[parser])
        #parser.add_argument("-c", "--channels", type=str, dest="channels", default=None, help="Set the traces to act on/acquire from." )
        #parser.add_argument("-o", "--filename", type=str, dest="filename", default=None, help="Set the name of the output file" )
        #parser.add_argument("-F", "--force",action="store_true", dest="force", default=None, help="Allows overwriting file" )
        #parser.add_argument("-t", "--trigger", dest="trigger",action="store_true", help="Trigger the scope once" )
        
        return parser
    
    def do_something(self,args):
        #if args.filename:
            ##getattr(self.Instance,'get_data_traces')(traces=args.channels,single=args.trigger)
            #getattr(self.Instance,'get_data_traces')(traces=args.channels)
            #getattr(self.Instance,'save_data_traces')(filename=args.filename,traces=args.channels,FORCE=args.force)
  
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

