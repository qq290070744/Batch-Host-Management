#!/usr/bin/env python
# -*- coding:utf-8 -*-
import prettytable,pymysql,logging
conn = pymysql.connect(host='121.201.68.21', user='jiang', passwd='jiangwenhui',port=3307, db='Batch-Host-Management', charset="utf8")
cur = conn.cursor()
#定义日志级别、格式、输出位配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %Y-%m-%d %H:%M:%S',
                    filename='../logs/test.log',
                    filemode='a',
                    )
while True:
    x = prettytable.PrettyTable(["\033[32m编号\033[0m","\033[33m名称\033[0m"])
    x.add_row([1,'查看分组'])
    x.add_row([2,'增加分组'])
    x.add_row([3,'删除分组'])
    x.add_row([4,'查看服务器'])
    x.add_row([5,'增加服务器'])
    x.add_row([6,'删除服务器 '])
    x.add_row([7,'修改服务器信息'])
    x.add_row([8,'quit'])
    print (x)


    enter=input("enter number:").strip()
    if enter=='1':
        reCount = cur.execute('select * from host')
        nRet = cur.fetchall()
        y = prettytable.PrettyTable(["\033[32mhost_ip\033[0m", "\033[33m所在主机组\033[0m"])
        for i in nRet:
            #print i[0],i[1]
            y.add_row([i[0],i[1]])
        print (y)
    elif enter=='2':
        group_name=input("请输入想要新建的主机组名称:").strip()
        host_ip=input("请输入你要添加到这个组的 host IP:").strip()
        user=input("输入主机用户名:").strip()
        password=input("输入主机password:").strip()
        port=input("输入端口号:").strip()
        reCount = cur.execute('insert into host(host_ip,host_group,username,password,port) values(%s,%s,%s,%s,%s)', (host_ip, group_name,user,password,port))
        conn.commit()
        print ("添加主机组{}成功".format(group_name))
        logging.info("添加主机组{}".format(group_name))
    elif enter=='3':
        group_name=input("请输入想要del的主机组名称:").strip()
        reCount = cur.execute("delete from host where host_group='%s' "%group_name)

        conn.commit()
        print ("del主机组{}成功".format(group_name))
        logging.info("del主机组{}".format(group_name))
    elif enter=='4':
        host_ip=input("请输入要查看服务器的IP:").strip()
        reCount = cur.execute("select * from host where host_ip='%s'"%host_ip)
        nRet = cur.fetchall()
        y = prettytable.PrettyTable(["\033[32mhost_ip\033[0m", "\033[33m所在主机组\033[0m"])
        for i in nRet:
            # print i[0],i[1]
            y.add_row([i[0], i[1]])
        print (y)
    elif enter=='5':
        host_ip=input("输入IP:").strip()
        group_name=input("输入所属的组:").strip()
        user = input("输入主机用户名:").strip()
        password = input("输入主机password:").strip()
        port=input("输入端口号:").strip()
        reCount = cur.execute('insert into host(host_ip,host_group,username,password,port) values(%s,%s,%s,%s,%s)', (host_ip, group_name,user,password,port))
        conn.commit()
        print ("添加主机[{}]成功".format(host_ip))
        logging.info("添加主机[{}]".format(host_ip))
    elif enter=='6':
        #host_ip=raw_input("输入IP:").strip()
        host_ip = input("请输入想要del的主机ip:").strip()
        reCount = cur.execute("delete from host where host_ip='%s' " % host_ip)

        conn.commit()
        print ("del主机{}成功".format(host_ip))
        logging.info("del主机{}".format(host_ip))
    elif enter=='7':
        host_ip=input("输入host IP:").strip()
        group_name=input("输入修改后的组名:").strip()
        user=input("输入修改后的username:").strip()
        password=input("输入修改后的password:").strip()
        port=input("输入修改后的 port:").strip()
        reCount = cur.execute("update host set host_group='%s',username='%s',password='%s',port='%s' where host_ip='%s' "%(group_name,user,password,port,host_ip))
        conn.commit()
        print ("修改服务器信息 成功!")
        logging.info("修改服务器信息")
    elif enter=='8':
        break

cur.close()
conn.close()