#!/usr/bin/env python
# -*- coding:utf-8 -*-
import MySQLdb,logging,sys,paramiko

#定义日志级别、格式、输出位配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %Y-%m-%d %H:%M:%S',
                    filename='../logs/test.log',
                    filemode='a',
                    )
class ssh_host(object):
    def __init__(self,conn,cur):
        self.conn=conn
        self.cur=cur
        pass
    def single(self):
        '''
        对单台主机的操作
        :return:
        '''
        while True:
            host_ip=raw_input("输入要操作的主机ip:").strip()
            cmd=raw_input("输入要操作的cmd:").strip()
            logging.info("{}{}".format(host_ip,cmd))
            reCount = self.cur.execute("select * from host where host_ip='{}' ".format(host_ip))
            nRet = self.cur.fetchall()
            print nRet[0]

            if cmd=='put':
                transport = paramiko.Transport((nRet[0][0], nRet[0][4]))
                transport.connect(username=nRet[0][2], password=nRet[0][3])
                sftp = paramiko.SFTPClient.from_transport(transport)
                local_file=raw_input("请输入你要上传文件的绝对路径:").strip()
                server_file=raw_input("请输入上传到远程主机的绝对路径:").strip()
                sftp.put(local_file, server_file)
                transport.close()
                print ("put成功")
            if cmd=='get':
                transport = paramiko.Transport((nRet[0][0], nRet[0][4]))
                transport.connect(username=nRet[0][2], password=nRet[0][3])
                sftp = paramiko.SFTPClient.from_transport(transport)
                server_file = raw_input("请输入远程主机文件的绝对路径:").strip()
                local_file = raw_input("请输local的绝对路径:").strip()
                sftp.get(server_file, local_file)
                transport.close()
                print ("get成功")



            # 创建SSH对象
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname=nRet[0][0], port=nRet[0][4], username=nRet[0][2], password=nRet[0][3])

            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            result = stdout.read()
            print result



        # 关闭连接
        ssh.close()
    def group(self):
        '''
        对一组机器操作
        :return:
        '''

        group_name=raw_input("输入组名:").strip()
        cmd = raw_input("输入要操作的cmd:").strip()
        if cmd=='put':
            local_file = raw_input("请输入你要上传文件的绝对路径:").strip()
            server_file = raw_input("请输入上传到远程主机的绝对路径:").strip()
        if cmd=='get':
            server_file = raw_input("请输入远程主机文件的绝对路径:").strip()
            local_file = raw_input("请输local的绝对路径:").strip()
        logging.info("{}{}".format(group_name,cmd))
        reCount = self.cur.execute("select * from host where host_group='{}' ".format(group_name))
        nRet = self.cur.fetchall()
        #print nRet[0][0]
        for i in nRet:
            print i[0]
            reCount = self.cur.execute("select * from host where host_ip='{}' ".format(i[0]))
            jieguo= self.cur.fetchall()
            print jieguo[0]
            if cmd == 'put':
                transport = paramiko.Transport((jieguo[0][0], jieguo[0][4]))
                transport.connect(username=jieguo[0][2], password=jieguo[0][3])
                sftp = paramiko.SFTPClient.from_transport(transport)
                #local_file = raw_input("请输入你要上传文件的绝对路径:").strip()
                #server_file = raw_input("请输入上传到远程主机的绝对路径:").strip()
                sftp.put(local_file, server_file)
                transport.close()
                print ("put成功")
            if cmd == 'get':
                transport = paramiko.Transport((jieguo[0][0], jieguo[0][4]))
                transport.connect(username=jieguo[0][2], password=jieguo[0][3])
                sftp = paramiko.SFTPClient.from_transport(transport)
                #server_file = raw_input("请输入远程主机文件的绝对路径:").strip()
                #local_file = raw_input("请输local的绝对路径:").strip()
                sftp.get(server_file, local_file)
                transport.close()
                print ("get成功")

            # 创建SSH对象
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname=jieguo[0][0], port=jieguo[0][4], username=jieguo[0][2], password=jieguo[0][3])

            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            result = stdout.read()
            print result

        # 关闭连接
        ssh.close()

if __name__=="__main__":
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='day8', charset="utf8")
    cur = conn.cursor()
    user_enter=raw_input("1:对单台主机的操作\n2:对一组机器操作\n>>:").strip()
    operating=ssh_host(conn,cur)
    if user_enter=='1':
        operating.single()
    elif user_enter=='2':
        operating.group()

    cur.close()
    conn.close()