'''

	# nshort算法
	几个概念
		待分词的文本，可以是一句话，也可以是一段文字
		一元词频(大数据语料库训练出来的一元单词的频率)
		一元词网(待分词文本，计算后得到的词频信息)
		二元词频(大数据语料库训练出来的二元单词的频率)
		二元词网(待分词文本，计算后得到的二元词频信息)
		
		传参过程

'''
import math

#定义全局变量
MAX_FREQUENCY = 25146057
dTemp = 1 / MAX_FREQUENCY + 0.00001
dSmoothPara = 0.1

#判断一个字是否是中文
def is_chinese(uchar):
	"""判断一个unicode是否是汉字"""
	if uchar >= u'/u4e00' and uchar<=u'/u9fa5':
		return True
	else:
		return False

#判断某个词在预料库中的频率是多少
def getWordFreq2(word):
	fopen = open('sanguo.txt',encoding="UTF-8")
	#计算每个汉字的词频,计算每个词语的词频
	wordCount = 0
	dicLength = len(word)
	for line in fopen.readlines():
		i = 0
		lineLength = len(line)
		while i < lineLength:
			if is_chinese(line[i]):
				if i + dicLength - 1 < lineLength:
					#print('curWord-->'+line[i:i+dicLength])
					if line[i:i+dicLength] == word:
						if word not in wordDict:
							wordCount = 1
						else:
							wordCount += 1
						i += dicLength
					else:
						i += 1
				else:
					i += 1
			else:
				i += 1
	return wordCount

#加载一元词频字典
def loadOneGramDictionary(fileName):
	fopen = open(fileName,encoding="UTF-8")
	wordFreqDict = {}
	for line in fopen.readlines():
		wordList = line.strip().split()
		wordFreqDict[wordList[0]] = int(wordList[2])
	fopen.close()
	return wordFreqDict
	
#加载二元词频字典
def loadTwoGramDictionary(fileName):
	fopen = open(fileName,encoding="UTF-8")
	wordFreqDict = {}
	for line in fopen.readlines():
		wordList = line.strip().split()
		wordFreqDict[wordList[0]] = int(wordList[1])
	fopen.close()
	return wordFreqDict	
	
#计算 一元词网: 返回列表	
def calcOneGramWordNet(content,oneGramWordDict):
	wordNet = {}
	index = 0
	for i in range(len(content)):
		j = i+1
		while ''.join(content[i:j]) in oneGramWordDict and j<=len(content):
			if content[i] not in wordNet:
				wordNet[content[i]] = {'index':index,'list':[]}
				index += 1
			wordNet[content[i]]['list'].append(content[i:j])
			j += 1
	return sorted(wordNet.items(),key=lambda k:k[1]['index'])	
		
#计算权重
def calcWeight(fromWord,toWord,oneGramWordFreq,twoGramWordFreq):
	frequency = 1
	if fromWord in oneGramWordFreq:
		frequency = oneGramWordFreq[fromWord]
	if frequency == 0:
		frequency = 1
	nTwoWordFreq = 1
	if fromWord+"@"+toWord in twoGramWordFreq:
		nTwoWordFreq = twoGramWordFreq[fromWord+"@"+toWord]
	weight = math.log(dSmoothPara * frequency / (MAX_FREQUENCY) + (1-dSmoothPara) * ((1-dTemp) * nTwoWordFreq / frequency + dTemp))
	if weight < 0:
		weight = -weight
	return weight	
		
#计算 二元词网
def calcTwoGramWordNet(wordNet,oneGramWordFreq,twoGramWordFreq):
	cur = 0
	dictList = []
	wordList = []
	indexDict = {}
	index = 0
	originList = []
	for word in wordNet:
		wordList.append(word[1]['list'])
		for singleWord in word[1]['list']:
			originList.append(singleWord)
		indexDict[index]  = cur
		index += 1
		cur += len(word[1]['list'])
	index = 0
	for word in wordNet:
		for i in range(indexDict[index],indexDict[index]+len(wordList[index])):
			tmpI = i - indexDict[index] + 1
			if index + tmpI >= len(wordList):
				continue
			for j in range(indexDict[index + tmpI],indexDict[index + tmpI]+len(wordList[index + tmpI])):
				tmpJ = j - indexDict[index + tmpI]
				dic = {}
				fromWord = wordList[index][tmpI-1]
				toWord = wordList[index + tmpI][tmpJ-1]
				dic['from'] = i
				dic['to'] = j
				dic['weight'] = calcWeight(fromWord,toWord,oneGramWordFreq,twoGramWordFreq)
				dic['word'] = fromWord+"@"+toWord
				dictList.append(dic)
		index += 1
	return dictList,originList
	
#返回要分词的内容，只返回一行
def getContent():
	return "石国祥会见乔布斯说苹果是世界上最好用的手机。"
	
#找到路径
def findPath(dic,fromNum,toNum):
	#print(fromNum,toNum)
	path = []
	if fromNum==toNum:
		return fromNum
	if fromNum==toNum-1:
		return toNum
		
	
	middleNum = dic[str(fromNum)+"@"+str(toNum)]
	left = findPath(dic,fromNum,middleNum)
	if type(left).__name__ == 'list':
		path = path + left
	else:
		path.append(left)
	path.append(toNum)
	return path
	
#根据二元词网计算最短路径
def finalCalc(twoGramWordNet):
	# 1 找出所有的点
	# 2 用floyd算法计算最短路径
	pointSet = set()
	MAX_TO = 0
	
	for dic in twoGramWordNet:
		pointSet.add(dic['from'])
		pointSet.add(dic['to'])
		if dic['to'] > MAX_TO:
			MAX_TO = dic['to']
	
	#print(twoGramWordNet)
	
	minValueDict = {}
	pathDict = {}
	
	for point1 in sorted(pointSet):
		for point2 in sorted(pointSet):
			minValueDict[str(point1)+"@"+str(point2)] = 9999
			pathDict[str(point1)+"@"+str(point2)] = -1
	
	for point1 in sorted(pointSet):
		for point2 in sorted(pointSet):
			if point1 != point2 and point2 > point1:
				for dic in twoGramWordNet:
					if dic['from'] == point1 and dic['to'] == point2:
						minValueDict[str(point1)+"@"+str(point2)] = dic['weight']
						pathDict[str(point1)+"@"+str(point2)] = -1
						
				
	
	for pointTmp in sorted(pointSet):
		for point1 in sorted(pointSet):
			for point2 in sorted(pointSet):
				if point1 != point2 and point2 > point1:
					pointStr = str(point1)+"@"+str(point2)
					point1ToTmp = str(point1)+"@"+str(pointTmp)
					pointTmpTo2 = str(pointTmp)+"@"+str(point2)
					if minValueDict[pointStr] > (minValueDict[point1ToTmp] + minValueDict[pointTmpTo2]):
						minValueDict[pointStr] = (minValueDict[point1ToTmp] + minValueDict[pointTmpTo2])
						pathDict[pointStr] = pointTmp
	
	
	#处理字典
	tmpDict = pathDict.copy()
	#for key in tmpDict:
	#	if pathDict[key] == -1:
	#		del pathDict[key]
			
	return findPath(pathDict,0,MAX_TO)
	'''
		0@24 = 22
		left = calc(0,22)
		right = calc(22,24)
		
	'''
	
#过滤二元词网
def filterTwoGramWordNet(twoGramWordNet):
	toSet = set()
	for dic in twoGramWordNet:
		toSet.add(dic['to'])
	
	weightDic = {}
	for to in toSet:
		weightDic[to] = 9999
		
	newTwoGramWordNet = []
	
	for to in toSet:
		for dic in twoGramWordNet:
			if dic['to'] == to and dic['weight'] < weightDic[to]:
				weightDic[to] = dic['weight']
	
	for to in toSet:
		for dic in twoGramWordNet:
			if dic['to']==to and dic['weight'] == weightDic[to]:
				newTwoGramWordNet.append(dic)
	
	return newTwoGramWordNet
	
#最新的算权重的办法
def calcPath(twoGramWordNet):
	return None
	
#nshort算法	
def nshort():
	
	'''
		一元词频
		二元词频
		一元词网
		二元词网
	'''
	oneGramWordDict = loadOneGramDictionary('CoreNatureDictionary.txt');
	print('一元词频------')
	print(oneGramWordDict)
	twoGramWordDict = loadTwoGramDictionary('CoreNatureDictionary.ngram.txt');
	#print('二元词频------')
	#print(twoGramWordDict)
	
	oneGramWordNet = calcOneGramWordNet(getContent(),oneGramWordDict)
	#print('一元词网------')
	#print(oneGramWordNet)
	
	twoGramWordNet,originList = calcTwoGramWordNet(oneGramWordNet,oneGramWordDict,twoGramWordDict)
	#twoGramWordNet = filterTwoGramWordNet(twoGramWordNet)
	#for dic in twoGramWordNet:
	#	print(dic['from'],dic['to'])
	path = finalCalc(twoGramWordNet)
	#path = calcPath(twoGramWordNet)
	print(originList[0],end=" ")
	for index in path:
		print(originList[index],end=" ")
	print("")
	#return path
	
	
	