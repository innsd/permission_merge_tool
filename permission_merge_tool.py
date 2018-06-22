######################################################################################
#The tool which is used to merge permission of minecraft game plugin GroupManner     #
#author:insnd                                                                        #
#e-mail:innsd@qq.com                                                                 #
#The poor program haven't Exception handing,so,emmmmm......                          #
#Please use std data                                                                 #
######################################################################################
import yaml
import os
import json
from funclib import *
logger.warning('this is a logger warning message')
try:
    with open("config.json","r") as f:
        config_data=json.load(f)
#        print(config_data)
except FileNotFoundError:
    print("第一次使用本程序？请完成以下初始化设置：")
    file_init()
except PermissionError:
    print("文件权限错误，请联系系统管理员检查文件权限！")
    exit()
with open("permissions.json","r") as f_p:
    permissions_is_merged=json.load(f_p)
lock=True
while(lock):
    try:
        with open(config_data["path1"],"r") as f1:
            permission1=yaml.load(f1)
        with open(config_data["path2"],"r") as f2:
            permission2=yaml.load(f2)
        with open(config_data["path3"],"r") as f3:
            permission3=yaml.load(f3)
        lock=False
    except IOError:
        print("打开文件错误，请重新进行设置")
        file_init()
        with open("config.json","r") as f:
            config_data=json.load(f)
print(permission1)
#test = json.dumps(permission1, sort_keys=True, indent=4, separators=(',', ': '))
#print(test)
players_in_f1=set(permission1["users"].keys())
players_in_f2=set(permission2["users"].keys())
players_in_f3=set(permission3["users"].keys())
players=players_in_f1|players_in_f2|players_in_f3
#print(players)
for player in players:
    permissions_in_1=set()
    permissions_in_2=set()
    permissions_in_3=set()
    print(player)
    if player in players_in_f1:
        permissions_in_1=set(permission1["users"][player]["permissions"])
        #print(permission1["users"][player]['lastname'])
    if player in players_in_f2:
        permissions_in_2=set(permission2["users"][player]["permissions"])
        #print(permission2["users"][player]['lastname'])
    if player in players_in_f3:
        permissions_in_3=set(permission3["users"][player]["permissions"])
        #print(permission3["users"][player]['lastname'])
    print("====================================\n")
    print(permissions_in_1)
    print(permissions_in_2)
    print(permissions_in_3)
    different_permissions=(permissions_in_1|permissions_in_2|permissions_in_3)-(permissions_in_1&permissions_in_2&permissions_in_3)
    print("diff权限集：")
    print(different_permissions)
    for p in different_permissions:
        lock=False
        for ap in permissions_is_merged:
            if ap in p:
                lock=True
        if lock:
            print("玩家："+permission1["users"][player]['lastname']+"的权限:"+p+"符合要求，\n")
            logger.info("玩家："+permission1["users"][player]['lastname']+"的权限:"+p+"符合要求")
            permissions_in_1.add(p)
            permissions_in_2.add(p)
            permissions_in_3.add(p)
            permission1["users"][player]['permissions']=list(permissions_in_1)
            permission2["users"][player]['permissions']=list(permissions_in_2)
            permission3["users"][player]['permissions']=list(permissions_in_3)
print(permission1)
#print(permission2)
#print(permission3)
lock=True
while(lock):
    try:
        with open(config_data["path1"],"w+") as f1:
            yaml.dump(permission1,f1)
        with open(config_data["path2"],"w+") as f2:
            yaml.dump(permission2,f2)
        with open(config_data["path3"],"w+") as f3:
            yaml.dump(permission3,f3)
        lock=False
    except IOError:
        print("打开文件错误，请重新进行设置")
        file_init()
        with open("config.json","r") as f:
            config_data=json.load(f)