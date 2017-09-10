#!usr/bin/python
import pymongo
from pymongo import MongoClient

import dropbox

from pprint import pprint

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

	def listFolders(self,dropbox_client,folder_path):
		folders=dropbox_client.metadata(folder_path)
		print('hello')
		print(folders["contents"])
		return folders["contents"]


		


if __name__ == '__main__':
	
	connexion_db=DataBaseConnexion('localhost',27017)
	mongo_client=connexion_db.connect()
	data_base=connexion_db.getDataBase(mongo_client,'Files')
	collection=connexion_db.getCollection(data_base,'file')
	connexion_db.showCollectionContent(collection)

	connexion_dp=DropboxConnexion('a677i_26wXAAAAAAAAAAOQNC1q-qgwWwG-9WvGvhbsAbxRvSRdE-OgStsTN4oFQQ')
	dropbox_client=connexion_dp.connect()
	connexion_dp.listFolders(dropbox_client,'/Docs')




