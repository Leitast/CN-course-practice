# -*- coding: utf_8 -*-
from Server import *
import Queue


port=3344
output=Output()# global 
Server(output).run(port)
output.run()
# 设计思路：
#1、线程：6个
#   主线程：在Output的run函数里运行。(IO并非总是很快，单独给它一个线程)(因为如果主线程休眠了，IO好像没反应(未实际验证))
#   子线程：
#           1、Server：在loop函数里接收并处理事件，包括clients manager的loop线程投递的事件
#           2、ClientsManager:
#               1、在listen函数里监听新的连接并交给loop处理(基本上处于休眠状态)
#               2、在loop函数里接收并处理事件
#           3、Client：
#               1、在send函数里发送封包(有必要？可能吧,没有它，只能交给client manager 的loop处理)
#               2、在recv函数里接收封包并交给clients manager的loop线程处理(基本上处于休眠状态)
#2、封包的处理：
#   package->Client->(msgtype,payload)->ClientsManager->(msgtype,name,...)->Server
#                  如果需要totalLength，修改代码



