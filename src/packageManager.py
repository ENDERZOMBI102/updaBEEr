from pathlib import Path
from typing import Dict

import requests

import beeManager
import config
import utilities
from packages import BPackage, PackageLargeView
from srctools.logger import get_logger

logger = get_logger()


def installBeeFromUrl(url: str):
	"""
	install a BEE package from url
	:param url: direct download link to the package/application zip
	"""
	path = Path( config.load('beePath') )
	if not path.exists():
		logger.error(f"BEE install path doesn't exist!")
		path.mkdir()
		logger.info('the folder has been created, please install BEE')
		return
	# tempFolder = config.temp


class PackageManager:

	database: Dict[str, BPackage]
	apiUrl: str
	databaseUrl = config.load('onlineDatabaseUrl')
	packagesWindows: Dict[str, PackageLargeView]

	def __init__(self):
		logger.info(f'checking package database.. ({self.databasePath})')
		if not utilities.isonline():
			pass
		else:
			pass

	def getPackage(self, identifier: str) -> BPackage:
		return self.database[identifier]

	def getPackageLargeView(self, identifier: str) -> PackageLargeView:
		return self.database[identifier].getLargeView()


def getDatabase():
	pass


def installBeePackage(identifier: str, url: str, service: str, filename: str):
	"""
	install a BEE package
	:param identifier: package identifier
	:param url: file direct download url
	:param service: file's service (github, gdrive, dropbox)
	:param filename: downloaded file name
	"""
	packagesPath: str = beeManager.packageFolder()
	filebytes: bytes  # the file content in bytes
	fileurl: str  # the file download url
	filename: str  # the file name
	filepath: str  # file path in the disk
	logger.info(f'installing package {identifier}')
	logger.debug('getting file url and name')
	if service == 'github':
		data = requests.get(url).json()  # get the release data
		fileurl = data['assets'][0]['browser_download_url']  # take the file url
		filename = data['assets'][0]['name']  # take the file name
	elif service == 'gdrive':
		fileurl = url  # take the file url
		filename = filename  # take the file name
	else:
		logger.warning(f'unexpected service found, expected "gdrive" or "github" got "{service}", aborting')
		return  # unsupported service
	logger.debug(f'file name: {filename}, file url: {fileurl}')
	# the filepath is generated by combining the packages folder path + filename
	filepath = packagesPath.join(filename)
	logger.debug('downloading file...')
	try:
		# get the file
		filebytes = requests.get(fileurl).content
	except Exception as e:
		logger.error(f'FAILED TO DOWNLOAD FILE! error: {e}')
		return
	logger.debug('success!')
	logger.debug('writing file to disk..')
	try:
		# write file to disk
		with open(filepath, 'x+b') as file:
			file.write(filebytes)
	except Exception as e:
		logger.error(f'FAILED TO SAVE FILE! error: {e}')
		return
	logger.info(f'successfully installed package {identifier}!')
