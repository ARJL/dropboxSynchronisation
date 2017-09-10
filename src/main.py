#!usr/bin/python
import pymongo
from pymongo import MongoClient

from pprint import pprint

class DataBaseConnexion(object):
	"""docstring for DataBaseConnexion"""

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


if __name__ == '__main__':
	
	connexion=DataBaseConnexion('localhost',27017)
	mongo_client=connexion.connect()
	data_base=connexion.getDataBase(mongo_client,'Files')
	collection=connexion.getCollection(data_base,'file')
	connexion.showCollectionContent(collection)

