from requests import *
from subprocess import *
from zipfile import *
from threading import Thread
from sys import platform
from config import config
from bases import web
import json
import io

os=platform

class beeManager(Thread):
	
	def checkUpdates():#return true if an update is available, false if there isn't or the pc is offline
		if(web.isonline==True):
			latestjson = get('https://api.github.com/repos/BEEmod/BEE2.4/releases/latest').json()
			onlineVersion=latestjson['tag_name']
			currentVersion = config.load('beeVersion')
			if(currentVersion>=onlineVersion):#check if online is present a newer version
				return False
			elif(latestjson["draft"]=="true"):
				return False
			elif(latestjson["prerelease"]=="true" and config.load("enablePrereleases")=="true"):
				return True
			else:
				return True
		else:
			return False

	def start(os, state):
		if(state==1):
			install()
			print('installed BEE v.'+config.load('beeVersion'))
			return
		elif(state==2):
			update()
			print('updated BEE to v.'+config.load('beeVersion'))
		else:
			unistall()
			print('unistalled BEE2.\nPress return key to exit.')
			input('')
			exit()
			