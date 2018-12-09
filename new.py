#!/usr/bin/env python
import argparse
from cp_modules.configure import configuration
import configparser
import sys
from cp_modules.option_menus import  mainmenu
from cp_modules.utility import colorize,header

if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='Multiprocess',
                                     add_help=True,
                                     description='A multi-process scraper')
    configuration(parser)

    # make a sweet intro to impress Jason
    print(colorize(header, 'blue'))
    print(colorize('version 1.0\n', 'green'))

    try:
        mainmenu()
    except KeyboardInterrupt:
        print("Keyboard interrupted")
    finally:
        sys.exit()   