#/usr/bin/env python
#coding=utf-8
#---------------------------------------------------------------------------
# Name:        zshell.py
# Author:      cedar12
#
# Created:     1-Nov-2019
# License:     Mit License
#---------------------------------------------------------------------------

import sys,re,platform,difflib,os

__version__='1.1.4'
__auchor__='cedar12'
__author_email__='cedar12.zxd@qq.com'
__github__='https://github.com/cedar12/zshell.git'

class App():
    __defs__=list()
    __defs_args__=list()
    __cell_args__=list()
    __curr_args__=list()
    __curr_cmd__=None
    __app_exit__=False
    __space__='_&_'
    __dict_name__='kwargs'
    __tuple_name__ = 'args'
    __cutoff=0.0
    def __init__(self,prefix='zshell:>>',ignore_case=True,info_print=True,unknown_command_error='Unknown command',cutoff=0.0):
        self.system_name=platform.system()
        self.prefix=prefix
        self.ignore_case=ignore_case
        self.unknown_command_error=unknown_command_error
        self.__cutoff=cutoff
        self.__add_in()
        print_str = '''
                   *******    *******    *          *******    *          *         
                        *     *          *          *          *          *         
                      *       *******    *******    *******    *          *         
                    *               *    *     *    *          *          *         
                   *******    *******    *     *    *******    *******    *******   '''
        if info_print:
            if self.system_name=='Windows':
                print(print_str)
            else:
                print('\033[1;34;0m{0} \033[0m'.format(print_str))
        self.__diff_list = []
        for d in self.__defs__:
            self.__diff_list.append(d[0])
    def __add_in(self):
        self.__add(('help',('Offer to help',self.__help)),{'help':[('c',['-c','--command'])]})
        self.__add(('exit|quit',('Quit the application',self.__exit)),{'exit|quit':[]})
        self.__add(('clear', ('Clean console output', self.__clear)), {'clear': []})
    def __output(self,m):
        print(m)
    def error(self,m):
        if m==self.unknown_command_error:
            if self.__cutoff==0.0:
                print('\033[1;31;0m{0} \033[0m'.format(m))
            else:
                list = difflib.get_close_matches(self.__curr_cmd, self.__diff_list, 10, cutoff=self.__cutoff)
                for c in list:
                    print(c+'\t',end='')
                print()
                if len(list)==0:
                    self.__output(m)
        elif platform.system()=='Windows':
            self.__output(m)
        else:
            print('\033[1;31;0m{0} \033[0m'.format(m))
    def __help(self,c=None):
        self.__output('AVAILABLE COMMANDS')
        for d in  self.__defs__:
            self.__output('\t{0}\t{1}'.format(d[0],d[1][0]))
    def __exit(self):
        self.__app_exit__=True
        sys.exit()
    def __clear(self):
        if platform.system()=='Windows':
            os.system('cls')
        else:
            os.system('clear')
        print()
    def __add(self,d,a):
        self.__defs__.append(d)
        self.__defs_args__.append(a)
    def __check_defs(self,name):
        for i in range(0,len( self.__defs__)):
            if  self.__defs__[i][0]==name:
                return i
    def __add_defs(self,desc,name,fn,args):
        if name == None:
            name = fn.__name__
        elif type(name) == str:
            name = name.strip()
        i = self.__check_defs(name)
        if i == None:
            self.__add((name,(desc,fn)),{name:args})
        else:
            self.__defs__[i]=(self.__defs__[i][0],(desc,fn))
            self.__defs_args__[i][name]=args
        pass

    def __space_input(self, input):
        input_list = list(input)
        si = 0
        ei = 0
        for i in range(0, len(input_list)):
            t = input_list[i]
            if (t == '\'' or t == '"') and input_list[i - 1] == ' ':
                si = i
            if (t == '\'' or t == '"') and (i == len(input_list) - 1 or input_list[i + 1] == ' '):
                ei = i
            if ei > si and ei != 0:
                for j in range(si, ei):
                    if input_list[j] == ' ':
                        input_list[j] = self.__space__
                si = 0
                ei = 0
        input = ''.join(input_list)
        return input
    def __input(self):
        if self.system_name=='Windows':
            inp = input(self.prefix)
        else:
            inp = input('\033[1;33;0m{0} \033[0m'.format(self.prefix))
        self.__cell_args__ = list()
        self.__curr_args__ = list()
        i=inp.strip().find(' ')
        if i==-1:
            self.__curr_cmd = inp
        else:
            args_str=inp[i:].strip()
            args_str=self.__space_input(args_str)
            args=re.split(r'\s+',args_str)
            for j in range(0,len(args)):
                args[j]=args[j].replace(self.__space__,' ')
            self.__curr_cmd=inp[:i]
            self.__curr_args__=args
        return self.__curr_cmd
    def __cmd(self,input):
        for i in range(0,len(self.__defs__)):
            d=self.__defs__[i]
            t_cmd=self.__curr_cmd
            c_cmd=self.__defs__[i][0]
            if self.ignore_case:
                t_cmd=str(t_cmd).upper()
                c_cmd=str(c_cmd).upper()
            if '|' in d[0] or '*' in d[0]:
                ab=self.__defs__[i][0].split('|')
                for t in ab:
                    if self.ignore_case:
                        t = t.upper()
                    if t.strip()==t_cmd:
                        self.__call(i)
                        return
            elif c_cmd.strip()==t_cmd.strip():
                self.__call(i)
                return
        self.error(self.unknown_command_error)
    def __args(self,args):
        if len(args)==0:
            handle = self.__curr_cmd__[1][1]
            varnames = []
            vars = handle.__code__.co_varnames
            vars_count = handle.__code__.co_argcount
            if vars_count==0 and len(vars)>=1 and vars[0]==self.__dict_name__:
                for i in range(0, len(self.__curr_args__) - 1,2):
                    try:
                        self.__curr_args__[i + 1] = int(self.__curr_args__[i + 1])
                    except:
                        self.__curr_args__[i + 1] = '\'' + self.__curr_args__[i + 1].replace('\'', '').replace('"', '') + '\''
                    self.__cell_args__.append('{0}={1}'.format(str(self.__curr_args__[i]).replace('-','').replace('--',''), self.__curr_args__[i + 1]))
            elif vars_count==0 and len(vars)>=1 and vars[0]==self.__tuple_name__:
                for i in range(0, len(self.__curr_args__)):
                    try:
                        self.__curr_args__[i] = int(self.__curr_args__[i])
                    except:
                        self.__curr_args__[i] = '\'' + self.__curr_args__[i].replace('\'', '').replace('"','') + '\''
                    self.__cell_args__.append(str(self.__curr_args__[i]))
            else:
                for j in range(0, vars_count):
                    varnames.append(vars[j])
                min_len=vars_count
                if min_len>len(self.__curr_args__):
                    min_len=len(self.__curr_args__)
                for i in range(0,min_len):
                    try:
                        self.__curr_args__[i] = int(self.__curr_args__[i])
                    except:
                        self.__curr_args__[i] = '\'' + self.__curr_args__[i].replace('\'', '').replace('"', '') + '\''
                        pass
                    if not self.__curr_args__[i] in self.__cell_args__:
                        self.__cell_args__.append('{0}={1}'.format(varnames[i], self.__curr_args__[i]))
        for a in args:
            key = a[0]
            prefix = a[1]
            for p in prefix:
                for i in range(0,len(self.__curr_args__)-1):
                    if self.__curr_args__[i] == str(p).strip():
                        try:
                            self.__curr_args__[i+1] = int(self.__curr_args__[i+1])
                        except:
                            self.__curr_args__[i+1] = '\'' + args[i].replace('\'', '').replace('"', '') + '\''
                            pass
                        self.__cell_args__.append('{0}={1}'.format(key,self.__curr_args__[i+1]))
                        break
    def __call(self,i):
        d=self.__defs__[i]
        self.__curr_cmd__=d
        args = self.__defs_args__[i][d[0]]
        res=None
        try:
            self.__args(args)
            if len(self.__cell_args__)==0:
                res=d[1][1]()
            else:
                res=eval('d[1][1]({0})'.format(','.join(self.__cell_args__)))
            if res != None:
                self.__output(res)
        except:
            self.__parse_error(sys.exc_info()[1])

    def __parse_error(self,err):
        self.error(err)
    def __loop(self,is_run=True):
        while is_run:
            if self.__app_exit__:
                return
            cmd=str(self.__input()).strip()
            self.__cmd(cmd)

    def shell(self,desc='',name=None,args=[]):
        if type(desc)==str:
            def fun(fn):
                self.__add_defs(desc,name,fn,args)
            return fun
        else:
            self.__add_defs('',name,desc,args)
            pass
    def run(self):
        if len(sys.argv) > 1:
            args = sys.argv[2:]
            cmd = sys.argv[1:2][0]
            for i in range(0, len(args)):
                try:
                    args[i] = int(args[i])
                except:
                    pass
            self.__curr_cmd = cmd
            self.__curr_args__ = args
            self.__cmd(cmd)
        else:
            self.__app_exit__=False
            self.__loop()