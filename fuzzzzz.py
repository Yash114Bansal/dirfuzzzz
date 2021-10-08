import requests
from concurrent.futures import ThreadPoolExecutor
import sys
import argparse
import textwrap
class color:
    def red(self,name):
        print(f"\033[91m{name}\033[0m")
    def pink(self,name):
        print(f"\033[95m{name}\033[0m")
    def yellow(self,name):
        print(f"\033[93m{name}\033[0m")
    def bright(self,name):
        print(f"\033[1;32;40m{name}\033[0m")
    def blue(self,name):
        print(f"\033[1;32;34m{name}\033[0m")
    def cyan(self,name):
        print(f"\033[1;32;36m{name}\033[0m")
def fuzz(wordlist):
    global url,extension,extension_list,list_files,suburl
    
    r=requests.get(url+wordlist)
    if not "404" in str(r):
        print(wordlist," "*(30-len(wordlist)),r.status_code)
        list_dirs.append(wordlist)
        suburl.append(wordlist)
    if extension:
        for j in extension_list:
            file=wordlist+"."+j
            r=requests.get(url+file)
            if not "404" in str(r):
                print(file," "*(30-len(file)),r.status_code)
                list_files.append(file)

def fuzzsub(wordlist):
    global url_sub,extension,extension_list,list_files,suburl,url
    wordlist=url_sub+"/"+wordlist
    r=requests.get(url+wordlist)
    if not "404" in str(r):
        print(wordlist," "*(30-len(wordlist)),r.status_code)
        list_dirs.append(wordlist)
        suburl.append(wordlist)
    if extension:
        for j in extension_list:
            file=wordlist+"."+j
            r=requests.get(url+file)
            if not "404" in str(r):
                print(file," "*(30-len(file)),r.status_code)
                list_files.append(file)

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Simple Fast Directory fuzzer",formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent('''
                \033[1;32;36mExample:
                    python3 fuzzzz.py -u "http://example.com" -w wordlist 
                    python3 fuzzzz.py -u "http://example.com" -w wordlist -t 50
                    python3 fuzzzz.py -u "http://example.com" -w wordlist -t 80 -x php,html,sh
                    python3 fuzzzz.py -u "http://example.com" -w wordlist -t 50 -o result.txt
                                                
               \033[0m '''))
    parser.add_argument('-u', '--url',type=str, help='url')
    parser.add_argument('-w', '--wordlist',type=argparse.FileType('r'), help='wordlist')
    parser.add_argument('-t', '--threads',type=int,default=50,help='threads')
    parser.add_argument('-x', '--extension', type=str, help='extension(seperates by ",")')
    parser.add_argument('-o', '--output',type=str, help='output file')
    args = parser.parse_args()
    colour=color()
    if not args.url:
        colour.red("Please Specify Url")
        sys.exit()
    if not args.wordlist:
        colour.red("Please Specify Wordlist")
        sys.exit()

    wordlist=[]
    for i in args.wordlist.readlines():
        wordlist.append(i.rstrip("\n"))
    url = args.url
    try:
        requests.get(url)
    except requests.exceptions.MissingSchema:
        colour.red("Invalid url ")
        sys.exit()
    if '/' not in url[-1]:
        url=url+'/'
    list_dirs=[]
    list_files=[]
    suburl=[]
    extension=args.extension
    if extension:
        extension_list_temp=extension.split(",")
        extension_list=[]
        for i in extension_list_temp:
            extension_list.append(i.replace(".", ""))
    threads=args.threads
    colour.yellow("Attacking")
    print("\033[95m",end="")
    execute=ThreadPoolExecutor(max_workers=threads)
    execute.map(fuzz,wordlist)
    execute.shutdown(wait=True)
    if len(suburl)>0:
        colour.cyan("Attcking SubDirectories")
    print("\033[95m",end="")
    for i in suburl:
         url_sub=i
         execute=ThreadPoolExecutor(max_workers=threads)
         execute.map(fuzzsub,wordlist)
         execute.shutdown(wait=True)

    if args.output:
        f = open(args.output,"w+")
        for i in list_dirs:
            f.write(i)
            f.write("\n")
        for j in list_files:
            f.write(j)
            f.write("\n")
        f.close()
        print("\033[0m")
