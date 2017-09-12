#!usr/bin/python
import pymongo
from pymongo import MongoClient

import dropbox

from pprint import pprint
import os
import re

from threading import Thread
import time

class DataBaseConnexion():

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
		print("collection content")
		for document in documents:
			pprint(document)
		print("collection content")

	def insertDocument(self,collection,document,path):
		collection.update( {"path":path},document,upsert=True)
		print("a document has been updated")

	def deleteDocument(self,collection,document):
		collection.delete_one(document)
		print("a document has been deleted")


class DropboxConnexion(DataBaseConnexion):
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

	def synchronize(self,dropbox_client,folder_path,connexion_db,collection):
		while True:
			#update documents
			for fil in dropbox_client.metadata(folder_path)["contents"]:
				if fil["is_dir"]==False:

					path=fil["path"] 
					parent_folder,base=os.path.split(path)
					name,ext=os.path.splitext(base)
					content=self.readFile(dropbox_client,path)
					document={"parent_folder":parent_folder,"name":name,"path":path,"content":content}
					
					connexion_db.insertDocument(collection,document,path)
				else:
					self.synchronize(dropbox_client,fil["path"],connexion_db,collection)

			#delete documents
			for fil in collection.find():
				res=dropbox_client.search(fil["parent_folder"],fil["name"])

				if res==[]:
					connexion_db.deleteDocument(collection,fil)
			print("sleeping...")
			time.sleep(1)



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
	connexion_dp.synchronize(dropbox_client,path,connexion_db,collection)



