#!/usr/bin/env python
# coding=gbk

import datetime
import time
import sys
import paramiko
import os
from openpyxl import Workbook
from openpyxl import load_workbook

global static1, static2 

def check_ip(ipaddr, device, username, old_password, new_password, log):
	global static1, static2

	addr=ipaddr.strip().split('.')  #切割IP地址为一个列表
	#print addr
	if len(addr) != 4:  #切割后列表必须有4个参数
		content = ipaddr + u"不符合ip规范!\n"
		static2 = static2 + 1
		print content
		log.write(content.encode("gbk"))
		return 0
	else:
		try:
			for i in range(4):
				addr[i]=int(addr[i])  #每个参数必须为数字，否则校验失败
		except:
			content = ipaddr + u"不符合ip规范!\n"
			static2 = static2 + 1
			print content
			log.write(content.encode("gbk"))
			return 0

		if addr[0] == 11 :
			if addr[1] == 76 or addr[1] == 77 :
				if addr[2] >= 0 and addr[2] <= 255:
					if addr[3] >=0 and addr[3] <=255:
						pass
					else:
						content = ipaddr + u"不符合ip规范!\n"
						static2 = static2 + 1
						print content
						log.write(content.encode("gbk"))
						return 0
				else:
					content = ipaddr + u"不符合ip规范!\n"
					static2 = static2 + 1
					print content
					log.write(content.encode("gbk"))
					return 0
			else:
				content = ipaddr + u"不符合ip规范!\n"
				static2 = static2 + 1
				print content
				log.write(content.encode("gbk"))
				return 0
		else:
			content = ipaddr + u"不符合ip规范!\n"
			static2 = static2 + 1
			print content
			log.write(content.encode("gbk"))
			return 0

	if device == None:
		content = ipaddr + u"不符合设备名称规范!\n"
		static2 = static2 + 1
		print content
		log.write(content.encode("gbk"))
		return 0
	if username == None:
		content = ipaddr + u"不符合用户名规范!\n"
		static2 = static2 + 1
		print content
		log.write(content.encode("gbk"))
		return 0
	if old_password == None:
		content = ipaddr + u"不符合旧密码规范!\n"
		static2 = static2 + 1
		print content
		log.write(content.encode("gbk"))
		return 0
	if new_password == None:
		content = ipaddr + u"不符合新密码规范!\n"
		static2 = static2 + 1
		print content
		log.write(content.encode("gbk"))
		return 0
	return 2

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


def do_cisco(ip, username, password, newpassword, log):
	global static1, static2
	remote_conn_pre = paramiko.SSHClient()

	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

		remote_conn = remote_conn_pre.invoke_shell()
    
		remote_conn.send("\n")
		remote_conn.send("en\n")
		time.sleep(1)
		remote_conn.send(password + "\n")
		remote_conn.send("config terminal\n")
		remote_conn.send("enable secret "+newpassword+"\n")
		time.sleep(1)
		remote_conn.send("username " + username + " password "+ newpassword + "\n")
		time.sleep(1)
		remote_conn.send("end\n")
		time.sleep(1)
		remote_conn.send("write\n")
		time.sleep(1)
		static1 = static1 + 1
		content = ip + u"这个IP所在的设备密码已经成功修改!\n"
		print content
		log.write(content.encode("gbk"))

	except:
		static2 = static2 + 1
		content = ip+ u"这个IP不存在或者用户名密码有错误!\n"
		print content
		log.write(content.encode("gbk"))

def do_h3c(ip, username, password, newpassword, log):
	global static1, static2
	remote_conn_pre = paramiko.SSHClient()

	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

		remote_conn = remote_conn_pre.invoke_shell()

		remote_conn.send("\n")
		remote_conn.send("sys\n")
		remote_conn.send("local-user " + username + "\n")
		remote_conn.send("password simple "+newpassword+"\n")
		time.sleep(1)
		remote_conn.send("quit\n")
		time.sleep(1)
		remote_conn.send("save\n")
		time.sleep(1)
		remote_conn.send("y\n")
		time.sleep(1)
		remote_conn.send("\n")
		time.sleep(1)
		remote_conn.send("y\n")
		time.sleep(1)
		static1 = static1 + 1
		content = ip + u"这个IP所在的设备密码已经被成功修改!\n"
		print content
		log.write(content.encode("gbk"))
	except:
		static2 = static2 + 1
		content = ip+ u"这个IP不存在或者用户名密码有错误!\n"
		print content
		log.write(content.encode("gbk"))

def display():
	global static1, static2

	control = 0
	while control < 3:
		print "请输入以下选项并按回车键进行操作："
		print "R键：更新你所有列表中的设备密码"
		print "V键：查看版本信息及服务条款"
		print "G键：生成一个导入文件模板"
		print "Q键：退出本程序"
		v = raw_input("Input:")
		if v == "r" or v == "R":
			ti = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))	
			log = open(ti + '_log.txt', "w")
			content = time.strftime('%Y年%m月%d日%H时%M分%S秒', time.localtime(time.time())) + "\n"	
			log.write(content)
			static1 = 0
			static2 = 0
			control = 1
			do_getInfo(log)
			static = static1 + static2
			content = u"本次修改共涉及设备"+str(static)+u"台,其中成功修改"+str(static1)+u"台，修改失败"+str(static2)+u"台。"
			print content
			log.write(content.encode("gbk"))
			log.close()
		elif v == "v" or v == "V": 
			control = 2 
			view_info()
		elif v == "q" or v == "Q":
			control = 3 
		elif v == "g" or v == "G":
			do_saveinfo()
		else:
			print "输入错误，请重新输入!!!"

def view_info():
	print "                          <服务条款>"
	print "    本程序为遵义中支科技科开发的批量修改网络设备密码工具（正式版V1.2）如您继续使用本工具，代表您同意以下条款："
	print "    1、因本程序漏洞或bug所造成的一切损失与遵义中支科技科无关。"
	print "    2、如果您发现任何有关本程序的漏洞或bug,请及时联系遵义中支科技科，联系电话：0851-28220393。"

def do_getInfo(log):
	global static1, static2 
	
	i=1
	st =True
	try:
		wb = load_workbook(filename = 'Password.xlsx')
		sheet_ranges = wb['Sheet']
		while st:
			i= i + 1
			ip = sheet_ranges['A' + str(i)].value
			if ip == None:
				break
			else:
				ip = ip.strip()
				device = sheet_ranges['C' + str(i)].value
				username = sheet_ranges['D' + str(i)].value
				old_password = sheet_ranges['E' + str(i)].value
				new_password = sheet_ranges['F' + str(i)].value
				if check_ip(ip, device, username, old_password, new_password, log) == 2:
					device = device.strip()
					username = username.strip()
					old_password = old_password.strip()
					new_password = new_password.strip()
					if device == 'cisco' or device == 'Cisco' or device == 'CISCO': 
						do_cisco(ip, username, old_password, new_password, log)
					elif device == 'h3c' or device == 'H3C':
						do_h3c(ip, username, old_password, new_password, log)
					elif device == 'mp' or device == 'MP' or device == 'Mp':
						do_cisco(ip, username, old_password, new_password, log)
					else :
						content = ip + u"这个IP所包含的设备信息存在错误!\n"
						static2 = static2 + 1
						print content
						log.write(content.encode("gbk"))
					
	except:
		content = "Password文件不存在！\n"
		print content

def do_saveinfo():
	try:
		wb = load_workbook(filename = 'Password.xlsx')
		print "Password文件已经存在!!"
	except:
		wb = Workbook()

	# grab the active worksheet
		ws = wb.active

	# Data can be assigned directly to cells
	#ws['A1'] = 'IP Adress'

	# Rows can also be appended
		ws.append([u'IP地址', u"连接方式", u"设备类型", u"用户名", u"旧密码", u"新密码"])

	# Python types will automatically be converted
	#ws['A2'] = datetime.datetime.now()

	# Save the file
		wb.save("Password.xlsx")

if __name__ == '__main__':
	view_info()
	#do_getinfo()
	display()

