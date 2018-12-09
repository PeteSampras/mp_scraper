import argparse
import configparser

def configuration(parser):
    #add global parses
    parser.add_argument('--mode','-m',
                        nargs=1,
                        help='Specific mode you want to use: QUIET, ALL',
                        choices=['ALL','PASSIVE','STEALTH','ACTIVE'],
                        default="ALL")
    parser.add_argument('--ip','-i',
                        nargs='*',
                        help='List of IP address you want to target')
    parser.add_argument('--port','-p',
                        nargs='?',
                        help='List of ports you want to target')
    parser.add_argument('--udp','-u', action='store_true',
                        help='Scan UDP?')
    args = parser.parse_args()