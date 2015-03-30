#!/usr/bin/env python
# -*-coding: utf-8-*-     
#    File Name: mysql_test
#       Author: 黄金强
#        Email: ligelaige@gmail.com
# Created Time: 2015-03-26 13:58


import os
from ConfigParser import ConfigParser
import MySQLdb

class CaseSConfigParser(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)

    def optionxform(self, optionstr):
        return optionstr


xsh_data = {

    "SessionInfo":[
            "Version"
        ],

    "CONNECTION":[
            "Port",
            "Host",
            "Protocol"
        ],

    "CONNECTION:AUTHENTICATION":[
        "Password",
        "UserName",
        "UseInitScript",
        "ScriptPath"
    ]

}

def getxshdata(xshfile = "", debug = True):
    if not os.path.exists(xshfile):
        print "Not Find File..."
        exit(-1)

    xsh_lines = []

    cf = CaseSConfigParser()
    cf.read(xshfile)
    section_list = cf.sections()

    for section in xsh_data:
        if section in section_list:

            xsh_lines.append("")
            xsh_lines.append("[%s]" % section)
            if debug:
                print
                print "[%s]" % section

            option_list = cf.options(section)

            for option in xsh_data[section]:
                if option in option_list:
                    arguments = cf.get(section, option)

                    xsh_lines.append("%s=%s" % (option, arguments))

                    if debug:
                        print "%s=%s" % (option, arguments)

    return xsh_lines

def getxshfile_list(rootpath = ""):
    if not os.path.exists(rootpath):
        print "File Path is not Exists..."
        exit(-1)

    xshfile_list = []

    def getfile(path):
        if os.path.isfile(path) and path.split(".")[-1] == "xsh":
            xshfile_list.append(path)
            return

        if os.path.isdir(path):
            for filename in os.listdir(path):
                subpath = os.path.join(path, filename)
                getfile(subpath)

        return

    getfile(rootpath)

    return xshfile_list

def get_XshFile_dictlist(xshpath = r"D:\Documents\PythonScript\auto_xshell\xshell"):

    filelist = getxshfile_list(xshpath)

    filedict_list = []

    for filename in filelist:
        nodedict = {}
        host = os.path.basename(filename)[:-4]
        xshfile = "\r\n".join(getxshdata(filename, False))
        nodedict["Host"] = host
        nodedict["Description"] = host
        nodedict["XshFile"] = str(xshfile)

        filedict_list.append(nodedict)

    return filedict_list

def save_XshFiledict(mysql_host, mysql_user, mysql_pwd, mysql_db, mysql_cmd = ""):
        try:
            conn = MySQLdb.connect(host = mysql_host, user = mysql_user, passwd = mysql_pwd, db = mysql_db)
            cur = conn.cursor()
            cur.execute(mysql_cmd)

            # rows = cur.fetchall()

            cur.close()
            conn.close()
            print "success!"

            # if len(rows) > 0:
            #     for row in rows:
            #         #print row
            #         line = [' : '.join(item) for item in zip(self.mysql_cmdargs, map(lambda x: str(x), row))]
            #         self.mysql_result_list.append('\r\n'.join(line))
            #
            # else:
            #     #print "^_^ All GateServers are Normal! ^_^"
            #     self.mysql_result_list.append("^_^ All GateServers are Normal! ^_^")

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            # self.mail_subject += "[Mysql Error]"
            print "failure!"

def mysql_insert_main():

    mysql_host = "mysql_host"
    mysql_user = "mysql_user"
    mysql_pwd = "mysql_pwd"
    mysql_db = "auto_xshell"

    xshpath = r"D:\Documents\PythonScript\auto_xshell\xshell"
    filedict_list = get_XshFile_dictlist(xshpath)

    for xshnode in filedict_list:
        xshfile = xshnode["XshFile"]
        mysql_insert = r'''INSERT INTO xsh_table(Host, Description, XshFile) VALUES('%s','%s','%s')''' \
                   % (xshnode["Host"], xshnode["Description"], xshfile)

        save_XshFiledict(mysql_host, mysql_user, mysql_pwd, mysql_db, mysql_insert)


def get_XshFiledict(mysql_host, mysql_user, mysql_pwd, mysql_db, mysql_cmd = ""):

    filedict_list = []

    try:
        conn = MySQLdb.connect(host = mysql_host, user = mysql_user, passwd = mysql_pwd, db = mysql_db)
        cur = conn.cursor()
        cur.execute(mysql_cmd)

        rows = cur.fetchall()

        cur.close()
        conn.close()
        print "success!"

        if len(rows) > 0:
            for row in rows:
                # print row
                nodedict = {
                    "Host" : row[1],
                    "Description": row[2],
                    "XshFile": row[3]
                }
                filedict_list.append(nodedict)

        else:
            print "^_^ All GateServers are Normal! ^_^"

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        print "failure!"

    return filedict_list

def mysql_select_main():

    mysql_host = "mysql_host"
    mysql_user = "mysql_user"
    mysql_pwd = "mysql_pwd"
    mysql_db = "auto_xshell"

    mysql_select = r'''SELECT * FROM xsh_table;'''

    filedict_list = get_XshFiledict(mysql_host, mysql_user, mysql_pwd, mysql_db, mysql_select)

    return filedict_list

if __name__ == '__main__':

    mysql_insert_main()

    # filedict_list = mysql_select_main()
    #
    # for nodedict in filedict_list:
    #
    #     print nodedict["XshFile"]

