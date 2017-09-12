#!usr/bin/python
import pymongo
from pymongo import MongoClient

import dropbox

from pprint import pprint
import os
import re

class DataBaseConnexion(object):

	def __init__(self, server,port):
		self.server=server
		self.port=port

	def connect(self):
		try:
			mongo_client=MongoClient(self.server,self.port)
			#print(mongo_client.server_info())
		except pymongo.errors as err:
			print(err)
		return mongo_client

	def getDataBase(self,mongo_client,data_base_name):
		data_base=mongo_client[data_base_name]
		return data_base

	def getCollection(self,data_base,collection_name):
		collection=data_base[collection_name]
		#print(collection.count())
		return collection

	def showCollectionContent(self,collection):
		documents=collection.find()
		for document in documents:
			print(document)

	def insertDocument(self):
		pass

	def deleteDocument(self):
		pass


class DropboxConnexion():
	def __init__(self, key):
		self.key = key

	def connect(self):
		dropbox_client=dropbox.client.DropboxClient(self.key)
		#print(dropbox_client.account_infos())
		return dropbox_client

	def readFile(self,dropbox_client,file_path):
		fil=dropbox_client.get_file(file_path)
		"""print("file content")
		print(fil.read())"""
		return (fil.read())

	def listFolders(self,dropbox_client,folder_path):
		files=[]
		for fil in dropbox_client.metadata(folder_path)["contents"]:
			if fil["is_dir"]==False:
				#files.append(fil)
				path=fil["path"]
				base=os.path.basename(path)
				name,ext=os.path.splitext(base)
				content=self.readFile(dropbox_client,path)
				document={"name":name,"path":path,"content":content}
				pprint(document)
			else:
				self.listFolders(dropbox_client,fil["path"])

	


if __name__ == '__main__':

	config_file=open('../.config','r')
	lines=config_file.readlines()
	configs=[]
	for line in lines:
		config=re.findall(r':+.*',line)
		config=config[0][1:]
		configs.append(config)
	server=configs[0]
	port=int(configs[1])
	key=configs[2]
	db=configs[3]
	col=configs[4]
	path=configs[5]
	
	connexion_db=DataBaseConnexion(server,port)
	mongo_client=connexion_db.connect()
	data_base=connexion_db.getDataBase(mongo_client,db)
	collection=connexion_db.getCollection(data_base,col)
	connexion_db.showCollectionContent(collection)

	connexion_dp=DropboxConnexion(key)
	dropbox_client=connexion_dp.connect()
	files=connexion_dp.listFolders(dropbox_client,path)



