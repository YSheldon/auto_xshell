#!/usr/bin/env python
# -*-coding: utf-8-*-     
#    File Name: auto_xshell
#       Author: 黄金强
#        Email: ligelaige@gmail.com
# Created Time: 2015-03-26 17:21

import MySQLdb
import os

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
            print 

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        print "failure!"

    return filedict_list


def mysql_select_main(host):

    mysql_host = "mysql_host"
    mysql_user = "mysql_user"
    mysql_pwd = "mysql_pwd"
    mysql_db = "auto_xshell"

    mysql_select = r'''SELECT * FROM xsh_table where Host='%s';''' % host

    filedict_list = get_XshFiledict(mysql_host, mysql_user, mysql_pwd, mysql_db, mysql_select)

    return filedict_list


def xshelltab(filepath, cmdpath = r"C:\Program Files (x86)\NetSarang\Xshell 5\Xshell.exe"):

    os.chdir(os.path.dirname(cmdpath))
    os.system("%s %s" % (os.path.basename(cmdpath), filepath))

def main(host = "192.168.0.199", cmdpath = r"C:\Program Files (x86)\NetSarang\Xshell 5\Xshell.exe", xshfilepath = os.path.dirname(__file__)):

    filedict_list = mysql_select_main(host)

    if len(filedict_list) > 0:
        nodedict = filedict_list[0]

        filepath = "%s-temp.xsh" % nodedict["Host"]
        print filepath
        filepath = os.path.join(xshfilepath, filepath)

        xsh_text_lines = nodedict["XshFile"].split("\r\n")

        xsh_text_lines = filter(lambda x: x.strip() != "", xsh_text_lines)

        fhandle = open(filepath, "w")
        for line in xsh_text_lines:
            fhandle.write(line + "\n")
            # print line
        fhandle.close()

        print xsh_text_lines

        xshelltab(filepath, cmdpath=cmdpath)
        # os.remove(filepath)

    else:
        print "  No found Host!"
        return
