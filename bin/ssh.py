#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql, logging, sys, paramiko
from multiprocessing import Process
import threading

# 定义日志级别、格式、输出位配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %Y-%m-%d %H:%M:%S',
                    filename='../logs/test.log',
                    filemode='a',
                    )


class ssh_host(object):
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        pass

    def single(self):
        '''
        对单台主机的操作
        :return:
        '''
        while True:
            host_ip = input("输入要操作的主机ip:").strip()
            cmd = input("输入要操作的cmd:").strip()
            logging.info("{}{}".format(host_ip, cmd))
            reCount = self.cur.execute("select * from host where host_ip='{}' ".format(host_ip))
            nRet = self.cur.fetchall()
            # print(nRet[0])

            if cmd == 'put':
                transport = paramiko.Transport((nRet[0][0], nRet[0][4]))
                transport.connect(username=nRet[0][2], password=nRet[0][3])
                sftp = paramiko.SFTPClient.from_transport(transport)
                local_file = input("请输入你要上传文件的绝对路径:").strip()
                server_file = input("请输入上传到远程主机的绝对路径:").strip()
                sftp.put(local_file, server_file)
                transport.close()
                print("put成功")
            if cmd == 'get':
                transport = paramiko.Transport((nRet[0][0], nRet[0][4]))
                transport.connect(username=nRet[0][2], password=nRet[0][3])
                sftp = paramiko.SFTPClient.from_transport(transport)
                server_file = input("请输入远程主机文件的绝对路径:").strip()
                local_file = input("请输local的绝对路径:").strip()
                sftp.get(server_file, local_file)
                transport.close()
                print("get成功")

            private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
            # 创建SSH对象
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname=nRet[0][0], port=nRet[0][4], username=nRet[0][2], key=private_key)

            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            result = stdout.read()
            print(result)



            # 关闭连接
            # ssh.close()

    def group(self):
        '''
        对一组机器操作
        :return:
        '''

        group_name = input("输入组名:").strip()
        cmd = input("输入要操作的cmd:").strip()
        if cmd == 'put':
            local_file = input("请输入你要上传文件的绝对路径:").strip()
            server_file = input("请输入上传到远程主机的绝对路径:").strip()
        if cmd == 'get':
            server_file = input("请输入远程主机文件的绝对路径:").strip()
            local_file = input("请输local的绝对路径:").strip()
        logging.info("{}{}".format(group_name, cmd))
        reCount = self.cur.execute("select * from host where host_group='{}'".format(group_name))
        nRet = self.cur.fetchall()

        # print (nRet)

        def exec(ip, user, password, prot, cmd):
            private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
            if cmd == 'put':
                transport = paramiko.Transport((ip, prot))
                transport.connect(username=user, pkey=private_key)
                sftp = paramiko.SFTPClient.from_transport(transport)
                # local_file = raw_input("请输入你要上传文件的绝对路径:").strip()
                # server_file = raw_input("请输入上传到远程主机的绝对路径:").strip()
                sftp.put(local_file, server_file)
                transport.close()
                print("put成功")
            if cmd == 'get':
                transport = paramiko.Transport((ip, prot))
                transport.connect(username=user, pkey=private_key)
                sftp = paramiko.SFTPClient.from_transport(transport)
                # server_file = raw_input("请输入远程主机文件的绝对路径:").strip()
                # local_file = raw_input("请输local的绝对路径:").strip()
                sftp.get(server_file, local_file)
                transport.close()
                print("get成功")


            # 创建SSH对象
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname=ip, port=prot, username=user, key=private_key)

            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            result = stdout.read()
            print("\033[32mhost:{} cmd:{}:执行结果\033[0m:\n {}".format(ip, cmd, str(result, 'utf8')))

            # 关闭连接
            ssh.close()

        for i in nRet:
            # print(i[0])
            reCount = self.cur.execute("select * from host where host_ip='{}' ".format(i[0]))
            jieguo = self.cur.fetchall()[0]
            # print(jieguo)
            ip = jieguo[0]
            user = jieguo[2]
            password = jieguo[3]
            port = jieguo[4]

            # print(ip,user,password,port)
            # exec(ip=jieguo[0],user=jieguo[2],password=jieguo[3],prot=jieguo[4],cmd=cmd)
            t = threading.Thread(target=exec, args=(ip, user, password, port, cmd))
            t.start()
            # p = Process(target=exec,args=(ip,user,password,port,cmd))
            # p.start()


if __name__ == "__main__":
    conn = pymysql.connect(host='121.201.68.21', user='jiang', passwd='jiangwenhui', port=3307,
                           db='Batch-Host-Management')
    cur = conn.cursor()
    user_enter = input("1:对单台主机的操作\n2:对一组机器操作\n>>:").strip()
    operating = ssh_host(conn, cur)
    if user_enter == '1':
        operating.single()
    elif user_enter == '2':
        operating.group()

    cur.close()
    conn.close()
