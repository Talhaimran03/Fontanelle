#!/usr/bin/env python
# File: csvmng
# Author: Carlo Tacchella
# Date: 21/06/2022
# Description: class to manage csv files

import pandas as pd

class CSVManager:
	df = None
	def __init__(self, fileName):
		print("Init CSVManager", fileName)		
		self.df = pd.read_csv(fileName)
	def getData(self):
		return self.df
	def getDataByProperty(self, attribute):
		return self.df[attribute]
	def getDataAsList(self):
		return self.df.values.tolist()
	def getDataByPropertyAsList(self, attribute):
		return self.df[attribute].tolist()

