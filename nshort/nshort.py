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
#定义全局变量
MAX_FREQUENCY = 25146057

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
					print('curWord-->'+line[i:i+dicLength])
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
def loadDictionary(fileName):
	fopen = open(fileName,encoding="UTF-8")
	wordFreqDict = {}
	for line in fopen.readlines():
		wordList = line.strip().split()
		wordFreqDict[wordList[0]] = int(wordList[2])
	fopen.close()
	return wordFreqDict
	
	
#计算 一元词频 内部算法  
#暂时不用自己计算词频 词频直接从字典文件加载
def getWordFreq():
	
	dictArr = loadDictionary('CoreNatureDictionary.txt');
	'''
	wordDict = {}
	i = 0
	tagSet = set()
	while i < listLength:
		temp = i
		for dic in dictArr:
			print(wordList[i],dic[0][0])
			if wordList[i] == dic[0][0]:
				print('=======')
				dicLength = len(dic[0])
				print(dicLength)
				if i + dicLength - 1 < listLength:
					print(wordList[i:i+dicLength])
					if ''.join(wordList[i:i+dicLength]) == dic[0]:
						if dic[0] not in wordDict:
							wordDict[dic[0]] = getWordFreq2(dic[0])
						tagSet.add(i+dicLength-1)
						i += dicLength
						break
					else:
						i += 1
				else:
					i += 1
		if temp == i:
			i += 1
	set1 = sorted(tagSet)
	'''
	return dictArr
	
#计算 一元词频
def prepareFrequency():
	'''
	fopen = open('sanguo.txt',encoding="UTF-8")
	#计算每个汉字的词频,计算每个词语的词频
	wordDict = {}
	wordDict2 = {}
	wordArr = []
	for line in fopen.readlines():
		wordArr.append(line)
		for i in range(len(line)):
			if is_chinese(line[i]):
				
				if line[i] not in wordDict:
					wordDict[line[i]] = 1
				else:
					wordDict[line[i]] += 1
	'''			
			
	
	wordDict2 = getWordFreq() 
	return wordDict2
	
	
	#一元词网
	'''
		循环某个句子
		while line[i] 有匹配:
			dict[line[i]].链表.append()
			一元词网
			
			重新分配顺序的时候  记住自己的下家是谁  乔下面有两个 所以有两个下家
			还没算概率
			
			关键是二元词频怎么计算,直接拿来用？
			一元词组@后面的东西有多少
			
			
			
			
	'''
	#二元词网
	'''
		
		会见@#人名#的概率
		
		对一元词网的每一个
		
		重新分配之后的链条 结合二元词网 进行计算
		
		endList[]
		for to in toList:
			for from in fromList:
				dict = {}
				dict['to'] = to
				dict['from'] = from
				dict['weight'] = weight(to,from)
				
		计算最优路径
		
		
		
	'''
	
#计算 一元词网: 返回字典	
def calcOneGramWordNet(content,oneGramWordDict):
	wordNet = {}
	for i in range(len(content)):
		j = i+1
		while ''.join(content[i:j]) in oneGramWordDict and j<=len(content):
			print('content->'+content[i:j])
			if content[i] not in wordNet:
				wordNet[content[i]] = []
			wordNet[content[i]].append(content[i:j])
			j += 1
	return wordNet	
		
#计算 二元词频权重
def calcWeight(fromWord,toWord):
	return 1.0		
		
#计算 二元词网
def calcTwoGramWordNet(wordNet):
	cur = 0
	dictList = []
	wordList = []
	indexDict = {}
	index = 0
	for word in wordNet:
		print(wordNet[word])
		wordList.append(wordNet[word])
		indexDict[index]  = cur
		index += 1
		cur += len(wordNet[word])
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
				dic['weight'] = calcWeight(fromWord,toWord)
				dic['word'] = fromWord+"@"+toWord
				dictList.append(dic)
		index += 1
	return dictList
	
#返回要分词的内容，只返回一行
def getContent():
	return "石国祥会见乔布斯说苹果是世界上最好的手机"
	
#根据二元词网计算最短路径
def finalCalc(twoGramWordNet):
	# 1 找出所有的点
	# 2 用floyd算法计算最短路径
	pointSet = set()
	print(twoGramWordNet)
	for dic in twoGramWordNet:
		pointSet.add(dic['from'])
		pointSet.add(dic['to'])
	
	minValueDict = {}
	pathDict = {}
	for point1 in pointSet:
		for point2 in pointSet:
			if point1 != point2:
				for dic in twoGramWordNet:
					if dic['from'] == point1 and dic['to'] == point2:
						minValueDict[str(point1)+"@"+str(point2)] = dic['weight']
						pathDict[str(point1)+"@"+str(point2)] = -1
				if str(point1)+"@"+str(point2) not in minValueDict:
					minValueDict[str(point1)+"@"+str(point2)] = 9999
					pathDict[str(point1)+"@"+str(point2)] = -1
				
	
	for pointTmp in pointSet:
		for point1 in pointSet:
			for point2 in pointSet:
				if point1 != point2 and point1 != pointTmp and point2 != pointTmp:
					pointStr = str(point1)+"@"+str(point2)
					point1ToTmp = str(point1)+"@"+str(pointTmp)
					pointTmpTo2 = str(pointTmp)+"@"+str(point2)
					if minValueDict[pointStr] > (minValueDict[point1ToTmp] + minValueDict[pointTmpTo2]):
						minValueDict[pointStr] = (minValueDict[point1ToTmp] + minValueDict[pointTmpTo2])
						pathDict[pointStr] = pointTmp
	
	
	#处理字典
	
	
	return pathDict
	
#nshort算法	
def nshort():
	
	'''
		一元词频
		#二元词频
		一元词网
		二元词网
	'''
	oneGramWordDict = prepareFrequency()
	#print('一元词频------')
	#print(oneGramWordDict)
	oneGramWordNet = calcOneGramWordNet(getContent(),oneGramWordDict)
	#print('一元词网------')
	#print(oneGramWordNet)
	twoGramWordNet = calcTwoGramWordNet(oneGramWordNet)
	path = finalCalc(twoGramWordNet)
	return path
	
	
	