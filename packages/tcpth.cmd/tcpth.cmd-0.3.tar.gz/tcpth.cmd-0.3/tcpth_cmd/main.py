# -*- coding:utf8 -*-
import sys
from optparse import OptionParser
import readline
from color_string import UseStyle
from cmd import Executor
import re
from pyfiglet import Figlet


LINE_HEADER = UseStyle("tcpthrough> ", fore='cyan')


def main():
    usage = "usage: %prog [options] [arg]"
    parser = OptionParser(usage)
    parser.add_option('-p', '--port', action='store', dest="port", default=8080, help=u"the http port for tcpserver")

    (option, args) = parser.parse_args()
    opt_dict = eval(str(option))
    opt_values = opt_dict.values()

    port = int(option.port)
    if not port:
        port = 8080


    print UseStyle("Welcome to use the tcp through.", fore='green')
    f = Figlet(font='slant')
    print UseStyle(f.renderText('Tcp Through'), fore='green')
    excutor = Executor(port)
    print ""
    while True:
        try:
            cmd = raw_input(LINE_HEADER)
            cmd = cmd.strip()
            if cmd == 'exit':
                print ""
                print UseStyle("Tcp Through Interaction Exit!", fore='red')
                break
            if cmd.startswith("list"):
                excutor.list()
            elif cmd.startswith("get "):
                excutor.get(cmd[3:])
            elif cmd.startswith("register "):
                cmd = cmd[len("register"):].strip()
                if cmd.startswith('add '):
                    args = cmd[3:].strip()
                    search_obj = re.search(r'(\S*)\s*(\S*)\s*(\S*)', args, re.M | re.I)
                    if search_obj and search_obj.lastindex == 3:
                        res = excutor.reg_add(search_obj.group(1), search_obj.group(2), search_obj.group(3))
                        if res is True:
                            continue
                elif cmd.startswith('delete '):
                    args = cmd[6:].strip()
                    search_obj = re.search(r'(\S*)\s*(\S*)', args, re.M | re.I)
                    if search_obj and search_obj.lastindex == 2:
                        res = excutor.reg_rm(search_obj.group(1), search_obj.group(2))
                        if res is True:
                            continue
                printHelp()
            elif cmd.startswith("trust "):
                cmd = cmd[len("trust"):].strip()
                if cmd.startswith('add '):
                    args = cmd[3:].strip()
                    search_obj = re.search(r'(\S*)\s*(\S*)\s*(\S*)', args, re.M | re.I)
                    if search_obj:
                        if search_obj.group(3) == '':
                            excutor.trust_ip_add(search_obj.group(1), search_obj.group(2))
                        else:
                            excutor.trust_ip_add_by_port(search_obj.group(1), search_obj.group(2), search_obj.group(3))
                    else :
                        printHelp()
                elif cmd.startswith('delete '):
                    args = cmd[6:].strip()
                    search_obj = re.search(r'(\S*)\s*(\S*)\s*(\S*)', args, re.M | re.I)
                    if search_obj:
                        if search_obj.group(3) == '':
                            excutor.trust_ip_rm(search_obj.group(1), search_obj.group(2))
                        else:
                            excutor.trust_ip_rm_by_port(search_obj.group(1), search_obj.group(2), search_obj.group(2))
                    else:
                        printHelp()
                elif cmd.startswith('get '):
                    args = cmd[3:].strip()
                    search_obj = re.search(r'(\S*)\s*(\S*)', args, re.M | re.I)
                    if search_obj:
                        if search_obj.group(2) == '':
                            excutor.trust_ip_get(search_obj.group(1))
                        else:
                            excutor.trust_ip_get_by_port(search_obj.group(1), search_obj.group(2))

                    else:
                        printHelp()
                else:
                    printHelp()
            elif cmd == 'help':
               printHelp()
            elif cmd.strip() == '':
                continue
            else:
               print UseStyle("use command 'help' for get more infomation", fore='red')
        except Exception, e:
            print ""
            print ""
            print UseStyle("Tcp Through Interaction Exit!", fore='red')
            break


def printHelp():
    help_info = "    " + UseStyle("list",fore='green') + "                                 -- get all registration\n" \
            +   "    " + UseStyle("get <name>",fore='green') + "                           -- get special name information\n" \
            +   "    " + UseStyle("register add <name> <localhost:port> <proxy port>",fore='green') + "    -- add registration\n" \
            +   "    " + UseStyle("register delete <name> <proxy port>",fore='green') + "                  -- delete registration\n" \
            +   "    " + UseStyle("trust add <name> [<proxy port>] <trusted ip>",fore='green') + "        -- add trust ip\n" \
            +   "    " + UseStyle("trust delete <name> [<proxy port>]  <trusted ip>",fore='green') + "     -- delete trust ip\n"\
            +   "    " + UseStyle("trust get <name> [<proxy port>]",fore='green') + "     -- get trust ip"
    print help_info

def intur_hander(signal, frame):
    sys.exit(0)

#
#
if __name__ == "__main__":
    main()
#     import signal
#     signal.signal(signal.SIGINT, intur_hander)
#
#     usage = "usage: %prog [options] [arg]"
#     parser = OptionParser(usage)
#     parser.add_option('-p', '--port', action='store', dest="port",default=8080, help=u"the http port for tcpserver")
#
#     (option, args) = parser.parse_args()
#     opt_dict = eval(str(option))
#     opt_values = opt_dict.values()
#
#     port = int(option.port)
#     if not port:
#         port = 8080
#
#     main(port)














    # print "\033[1;35m [tcpserver] \033[0m",
    # input_v = raw_input()
    # print input_v
    # print "end"
    # print 'This is a \033[1;35m test \033[0m!'

    #
    # def log(func):
    #     def wrapper(*args, **kw):
    #         print('call before %s():' % func.__name__)
    #         res = func(*args, **kw)
    #         print('call after %s():' % func.__name__)
    #         return res
    #     return wrapper
    #
    # @log
    # def now():
    #     print('2015-3-25')
    #
    #
    # now()
