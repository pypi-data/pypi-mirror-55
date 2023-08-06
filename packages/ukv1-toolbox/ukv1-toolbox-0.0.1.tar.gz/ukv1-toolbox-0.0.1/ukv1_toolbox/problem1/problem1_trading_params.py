from backtester.trading_system import TradingSystem
from backtester.trading_system_parameters import TradingSystemParameters
from backtester.features.feature import Feature
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.version import updateCheck
from backtester.constants import *
from backtester.timeRule.us_time_rule import USTimeRule
from backtester.dataSource.csv_data_source import CsvDataSource
from backtester.logger import *
import pandas as pd

class MyTradingParams(TradingSystemParameters):
	'''
	initialize class
	place any global variables here
	'''
	def __init__(self, tradingFunctions):
		self.__tradingFunctions = tradingFunctions
		self.__dataSetId = 'qq16p1Data'
		self.__instrumentIds = self.__tradingFunctions.getInstrumentIds()
		self.__targetVariable = 'Revenue'
		self.__priceKey = 'Share Price'
		self.__additionalInstrumentFeatureConfigDicts = self.__tradingFunctions.getInstrumentFeatureConfigDicts()
		self.__additionalMarketFeatureConfigDicts = []
		self.__fees = {'brokerage': 0.00,'spread': 0.00}
		self.__startDate = '2009/09/30'
		self.__endDate = '2019/06/30'
		self.__lookbackSize = 20
		self.__dataParser = None
		self.__model = {}
		self.__params = self.__tradingFunctions.params
		self.updateFrequency = 1
		self.burnData = 60
		self.predictionLogFile = open('predictions.csv', 'a')
		self.headerNotSet = True
		super(MyTradingParams, self).__init__()

	'''
	Returns an instance of class DataParser. Source of data for instruments
	'''

	def getDataParser(self):
		
		downloadUrl = 'https://qq16-data.s3.us-east-2.amazonaws.com/qq16p1Data/'
		
		datasource = CsvDataSource(cachedFolderName='historicalData/',
							 dataSetId=self.__dataSetId,
							 instrumentIds=self.__instrumentIds,
							 downloadUrl = downloadUrl,
							 timeKey = 'time',
							 timeStringFormat = '%Y-%m-%d',
							 startDateStr=self.__startDate,
							 endDateStr=self.__endDate,
							 liveUpdates=True,
							 pad=True)
		return datasource


	def getTimeRuleForUpdates(self):
		return USTimeRule(startDate = self.__startDate,
						endDate = self.__endDate,
						frequency='BQ', sample='1')

	
	'''
	Return starting capital
	'''
	def getStartingCapital(self):
		return 10000
	
	'''
	This is a way to use any custom features you might have made.
	'''

	def getCustomFeatures(self):
		customFeatures = {'prediction': TrainingPredictionFeature}
		try:
			customFeatures.update(self.__tradingFunctions.getCustomFeatures())
			return customFeatures
		except AttributeError:
			return customFeatures

	def getInstrumentFeatureConfigDicts(self):

		predictionDict = {'featureKey': 'prediction',
								'featureId': 'prediction',
								'params': {'tsParams':self}}

		# ADD RELEVANT FEATURES HERE
		expma10dic = {'featureKey': 'expma10',
				 'featureId': 'exponential_moving_average',
				 'params': {'period': 4,
							  'featureName': 'Share Price'}}
		mom10dic = {'featureKey': 'mom10',
				 'featureId': 'difference',
				 'params': {'period': 4,
							  'featureName': 'Share Price'}}
		scoreDict = {'featureKey': 'score',
					 'featureId': 'score_fv',
					 'params': {'predictionKey': 'prediction',
								'price' : self.getTargetVariableKey()}}

		stockFeatureConfigs = self.__tradingFunctions.getInstrumentFeatureConfigDicts()
		return {INSTRUMENT_TYPE_STOCK: stockFeatureConfigs +
				self.__additionalInstrumentFeatureConfigDicts
										+ [predictionDict, scoreDict]}

	'''
	Returns an array of market feature config dictionaries
	'''

	def getMarketFeatureConfigDicts(self):
	# ADD RELEVANT FEATURES HERE
		scoreDict = {'featureKey': 'score',
					 'featureId': 'score_fv',
					 'params': {'featureName': self.getPriceFeatureKey(),
								'instrument_score_feature': 'score'}}
		return self.__additionalMarketFeatureConfigDicts + [scoreDict]


	'''
	A function that returns your predicted value based on your heuristics.
	'''

	def getPrediction(self, time, updateNum, instrumentManager):

		predictions = pd.Series(0.0, index = self.__instrumentIds)

		# holder for all the instrument features
		lbInstF = instrumentManager.getLookbackInstrumentFeatures()
		featureList = lbInstF.getAllFeatures()
		# print(featureList)
		if 'Revenue(Y)' in featureList:
			featureList.remove('Revenue(Y)')
		if 'Income(Y)' in featureList:
			featureList.remove('Income(Y)')

		if self.getTargetVariableKey()=='Revenue':
			predictions = self.__tradingFunctions.getRevenuePrediction(time, updateNum, lbInstF, 
						instrumentManager.getDataDf(), featureList, 
						lbInstF.getFeatureDf(self.getTargetVariableKey()), predictions)
		else:
			predictions = self.__tradingFunctions.getIncomePrediction(time, updateNum, lbInstF, 
						instrumentManager.getDataDf(), featureList, 
						lbInstF.getFeatureDf(self.getTargetVariableKey()), predictions)
		
		print('Predicted Value for %s: %.3f'%(self.getTargetVariableKey(), predictions))

		self.logPredictions(time, predictions)

		return predictions

	'''
	Here we convert prediction to intended positions for different instruments.
	'''

	def getExecutionSystem(self):
		return SimpleExecutionSystem(enter_threshold=1, exit_threshold=0.5, 
									longLimit=0, shortLimit=0, capitalUsageLimit=0.05, 
									enterlotSize=0, exitlotSize=0, 
									limitType='L', price=self.getPriceFeatureKey())

	'''
	For Backtesting, we use the BacktestingOrderPlacer, which places the order which we want, 
	and automatically confirms it too.
	'''

	def getOrderPlacer(self):
		return BacktestingOrderPlacer()

	'''
	Returns the amount of lookback data you want for your calculations.
	'''

	def getLookbackSize(self):
		return 90


	def getMetricsToLogRealtime(self):
		# Everything will be logged if left as is
		return {
			'market': None,
			'instruments': None
		}

	def getPriceFeatureKey(self):
		return self.__priceKey

	def setPriceFeatureKey(self, priceKey='Adj_Close'):
		self.__priceKey = priceKey

	def getDataSetId(self):
		return self.__dataSetId

	def setDataSetId(self, dataSetId):
		self.__dataSetId = dataSetId

	def getInstrumentsIds(self):
		return self.__instrumentIds

	def setInstrumentsIds(self, instrumentIds):
		self.__instrumentIds = instrumentIds

	def getDates(self):
		return {'startDate':self.__startDate,
				'endDate':self.__endDate}

	def setDates(self, dateDict):
		self.__startDate = dateDict['startDate']
		self.__endDate = dateDict['endDate']

	def getTargetVariableKey(self):
		return self.__targetVariable

	def setTargetVariableKey(self, targetVariable):
		self.__targetVariable = targetVariable

	def setFees(self, feeDict={'brokerage': 0.00,'spread': 0.00}):
		self.__fees = feeDict

	def setAdditionalInstrumentFeatureConfigDicts(self, dicts = []):
		self.__additionalInstrumentFeatureConfigDicts = dicts

	def setAdditionalMarketFeatureConfigDicts(self, dicts = []):
		self.__additionalMarketFeatureConfigDicts = dicts

	def getFeatureKeys(self):
		return self.__featureKeys

	def setFeatureKeys(self, featureList):
		self.__featureKeys = featureList

	def getBurn(self):
		return self.burnData

	def setBurn(self, burn=240):
		self.burnData = burn

	def setPredictionLogFile(self, logFileName):
		self.predictionLogFile = open(logFileName, 'a')

	def logPredictions(self, time, predictions):
		if (self.predictionLogFile != None):
			if (self.headerNotSet):
				header = 'datetime'
				for index in predictions.index:
					header = header + ',' + index
				self.predictionLogFile.write(header + '\n')
				self.headerNotSet = False

			lineData = str(time)

			for prediction in predictions.get_values():
				lineData = lineData + ',' + str(prediction)

			self.predictionLogFile.write(lineData + '\n')


class TrainingPredictionFeature(Feature):

	@classmethod
	def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
		t = featureParams['tsParams']
		return t.getPrediction(time, updateNum, instrumentManager)
