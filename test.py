#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime
import time
import sys
import paramiko

def cisco_disable_paging(remote_conn):
	'''Disable paging on a Cisco router'''

	remote_conn.send("terminal length 0\n")
	time.sleep(1)

	# Clear the buffer on the screen
	output = remote_conn.recv(1000)

	return output

def h3c_disable_paging(remote_conn):
	remote_conn.send("screen-length 0\n")
	time.sleep(1)

	output = remote_conn.recv(1000)
	return output

def getInfo(log):
	st = True
	try:
		f = open("./password.txt", "r")  
		while st:  
			line = f.readline()  
			if line:  
				#pass # do something here 
				line=line.strip()
				#print "create %s"%line
				analyzeInfo(line, log)
			else:  
				break
		f.close()
	except:
		content = "password.txt文件不存在！\n"
		print content
		log.write(content)
	
def writeInfo(contain):
	file_object = open('thefile.txt', 'w')
	file_object.write(contain)
	file_object.close( )


def analyzeInfo(line, log):
	s = line
	ss = s.split(' ')
	if len(ss) == 6:
		if ss[2] == 'cisco':
			#print ss[0], ss[3], ss[4]
			do_cisco(ss[0],ss[3],ss[4],ss[5], log)
		elif ss[2] == 'h3c':
			do_h3c(ss[0],ss[3],ss[4], ss[5],log)
		else :
			content = ss[0] + "这个IP所包含的设备信息存在错误!\n"
			print content
			log.write(content)
	else:
		content = ss[0] + "这个IP所包含的参数数量存在错误!\n"
		print content
		log.write(content)
	
def do_telnet(Host, username, password):
	tn = telnetlib.Telnet(Host)
	tn.set_debuglevel(2)
 
	tn.read_until('Username:')
	tn.write(username + '\n')
 
	tn.read_until('Password:')
	tn.write(password + '\n')
 
	tn.write('en' + '\n')
	tn.read_until('Password:')
	tn.write(password +'\n')

	tn.write('show run' + '\n')
	#tn.write('exit' + '\n')
	#time.sleep(1)
	while (tn.read_until('--More--') == '--More--'):
		output = tn.read_very_eager()
		tn.write(' ')
	output = tn.read_very_eager()
	tn.write('exit' + '\n')
	tn.close()
	#print output
	#tn.close() # tn.write('exit\n')
	writeInfo(output)
 
def do_cisco(ip, username, password, newpassword, log):
	#newpassword = "zyhlw@27"
	# Create instance of SSHClient object
	remote_conn_pre = paramiko.SSHClient()

	# Automatically add untrusted hosts (make sure okay for security policy in your environment)
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		# initiate SSH connection
		remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
		#print "SSH connection established to %s" % ip

		# Use invoke_shell to establish an 'interactive session'
		remote_conn = remote_conn_pre.invoke_shell()
		#print "Interactive SSH session established"

		# Strip the initial router prompt
		#output = remote_conn.recv(1000)

		# See what we have
		#print output
		# Turn off paging
		#cisco_disable_paging(remote_conn)

		# Now let's try to send the router a command
		#remote_conn.send("\n")
		#remote_conn.send("show ip int brief\n")

		# Wait for the command to complete
    
		#output = remote_conn.recv(5000)
		#print output
    
		#disable_paging(remote_conn)
		remote_conn.send("\n")
		remote_conn.send("en\n")
		time.sleep(2)
		remote_conn.send(password + "\n")
		remote_conn.send("config terminal\n")
		remote_conn.send("enable secret "+newpassword+"\n")
		time.sleep(2)
		remote_conn.send("username " + username + " password "+ newpassword + "\n")
		#time.sleep(2)
		#output = remote_conn.recv(5000)
		content = ip + "这个IP所在的设备密码已经成功修改!\n"	
		print content
		log.write(content)

	except:
		content = ip+ "这个IP不存在或者用户名密码有错误!\n"
		print content
		log.write(content)

def do_h3c(ip, username, password, newpassword, log):
	# Create instance of SSHClient object
	remote_conn_pre = paramiko.SSHClient()

	# Automatically add untrusted hosts (make sure okay for security policy in your environment)
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		# initiate SSH connection
		remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
		#print "SSH connection established to %s" % ip

		# Use invoke_shell to establish an 'interactive session'
		remote_conn = remote_conn_pre.invoke_shell()
		#print "Interactive SSH session established"

		# Strip the initial router prompt
		#output = remote_conn.recv(1000)

		# See what we have
		#print output

		# Turn off paging
		#h3c_disable_paging(remote_conn)

		# Now let's try to send the router a command
		#remote_conn.send("\n")
		#remote_conn.send("display cur\n")

		# Wait for the command to complete
		#time.sleep(2)
    
		#output = remote_conn.recv(5000)
		#print output
    
		#disable_paging(remote_conn)

		remote_conn.send("\n")
		remote_conn.send("sys\n")
		remote_conn.send("local-user " + username + "\n")
		remote_conn.send("password simple "+newpassword+"\n")
		#time.sleep(2)
		#print output
		content = ip + "这个IP所在的设备密码已经被成功修改!\n"
		print content
		log.write(content)
	except:
		content = ip+ "这个IP不存在或者用户名密码有错误!\n"
		print content
		log.write(content)

def display():
	control = 0
	while control < 3:
		print "请输入以下选项并按回车键进行操作："
		print "R键：更新你所有列表中的设备密码"
		print "V键：查看版本信息及服务条款"
		print "Q键：退出本程序"
		v = raw_input("Input:")
		if v == "r" or v == "R":
			ti = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))	
			log = open(ti + '_log.txt', "w")
			control = 1
			getInfo(log)
			log.close()
		elif v == "v" or v == "V": 
			control = 2 
			view_info()
		elif v == "q" or v == "Q":
			control = 3 
		else:
			print "输入错误，请重新输入!!!"

def view_info():
	print "                      服务条款"
	print "    本程序为遵义中支科技科开发的批量修改网络设备密码工具（测试版V1.1）如您继续使用本工具，代表您同意以下条款：1、因本程序漏洞或bug所造成的一切损失与遵义中支科技科无关。2、如果您发现任何有关本程序的漏洞或bug,请及时联系遵义中支科技科，联系电话：0851-28220393。"

if __name__=='__main__':
	#Host = 'IP' 
	view_info()
	display()
	#analyzeInfo()
	#username = 'user'
	#password = 'password'
	#do_telnetiHost, username, password)


	# VARIABLES THAT NEED CHANGED


