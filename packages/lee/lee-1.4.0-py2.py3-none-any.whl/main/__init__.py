from core.cli import Cli
from core.enhancer import *
import sys
import os
import argparse
from halo import Halo


def pull(args,b):
    b.pull(args.id)

def push(args,b):
    assert args.filepath
    if args.test:
        print("test------------")
        b.test(args.filepath)
    else:
        print("submit")
        b.submit(args.filepath)

def ls(args,b):
    if args.solution_count:
        assert args.ids
        b.solution(args.ids,args.solution_count,args.markdown,args.language)
    else:
        b.show(args.ids)

def log(args,b):
    b.log()

def login(args,b):
    b.login()
def main(args):
    cli = Cli()
    b =Enhancer(cli,args)
    args.func(args,b)

def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    subparsers = parser.add_subparsers()

########################################################################
#   show  commands 
    show_parser = subparsers.add_parser('show',formatter_class=argparse.ArgumentDefaultsHelpFormatter,aliases=["ls"], description="",  help='show questions, solution')
    show_parser.set_defaults(func=ls)
    show_parser.add_argument("ids",  help="question ids Ex: 1  \n  1,2,5  or 1-20  or all" )
    show_parser.add_argument('-s', '--solution_count', help='show top rated solution count')  
    # show_parser.add_argument('-d', '--detail', help='show quesiton detail')  
    show_parser.add_argument('-m', '--markdown', action='store_true', help='output solution markdown only effect when -s is specified')  
    show_parser.add_argument('-c', '--clean', help='clean mode, no garbage generated, easy to pipe the output')  
    show_parser.add_argument("-a","-all",default=False,  help="show all" )
#     show_parser.add_argument('-i', '--id',type=str,  help="question ids Ex: 1  or  1,2,5  or 1-20" )
    show_parser.add_argument('-f', '--filter',type=str,required=False, help='filter args', default="")  
    show_parser.add_argument("-l",'--language', type=str, default="python", required=False, help='language')

########################################################################
#   main commands
    parser.add_argument("-p",'--proxy', action='store_true',default=False,  help='auto proxy at 127.0.0.1:18888 for debug, and ignore SSL certificate verification')
    parser.add_argument("-r",'--refresh', action='store_true',default=False,  help='get request will refresh cache')
    parser.add_argument('-d', '--debug', help='debug mode. debug logger will output', default=False, action='store_true')   
    parser.add_argument('-j', '--json', help='pure json output', default=False, action='store_true')   

########################################################################
#   pull commands

#     pull_parser = pull_parser.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")

    pull_parser = subparsers.add_parser('pull', formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="", help='pull question related files to local disk by')
    pull_parser.set_defaults(func=pull)

    pull_parser.add_argument('id',  help="question id" )
    pull_parser.add_argument('-t', '--tempalte', help='generate code template',default=True, action='store_true')  
#     pull_parser.add_argument("-i",'--id', type=str, required=False, help='question id')
    pull_parser.add_argument('-m', '--markdown', help='generate markdown', action='store_true')  
    pull_parser.add_argument('-html', '--html', help='generate html', action='store_true')  
    pull_parser.add_argument('-o', '--output',type=str,required=False, help='where does template file generate to', default="./")  
    pull_parser.add_argument("-l",'--language', type=str, default="python", required=False, help='language')
     

     
########################################################################
#   push  commands 

    push_parser = subparsers.add_parser('push',formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="",  help='push file to server')
    push_parser.set_defaults(func=push)

    push_parser.add_argument('filepath',  help="if submit/test,lee will try to use the default generated file name by id.But if it fails,you need to specify the full name" )

#     push_parser.add_argument("-i",'--id', type=str,  required=False, help='question id')
    push_parser.add_argument('-t', '--test', help='test questions', default=False, action='store_true') 
#     push_parser.add_argument("-f",'--file', type=str, required=False, help='if submit/test,lee will try to use the default generated file name by id.But if it fails,you need to specify the full name')


########################################################################
#   log  commands 
    log_parser = subparsers.add_parser('log',formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="",  help='status of server')
    log_parser.set_defaults(func=log)
########################################################################
#   login  commands 
    login_parser = subparsers.add_parser('login',formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="",  help='login ')
    login_parser.set_defaults(func=login)
    return parser

# @Halo(text='...', spinner='dots', color="green", text_color="green")
# @Halo(text='Loading.', spinner='dots', color="green", text_color="green")
# @Halo(text='Loading..',stream=sys.stderr, spinner='dots', color="cyan", text_color="cyan")
def command_main():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)
    
    
if __name__ == "__main__":
    command_main()



    
