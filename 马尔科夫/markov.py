'''
	马尔科夫进行分词
	给定一篇文档
		
		
	
'''
from numpy import *
import json
#加载词典文件
def loadDictionary(fileName):
	fopen = open(fileName,'r',encoding="UTF-8")
	dataArr = []
	for line in fopen.readlines():
		dataArr.append(line.strip().split())
	return dataArr
		

def fenci():
	fopen =  open('testSet.txt','r',encoding="UTF-8")
	wordSet = set()
	wordList = []
	for line in fopen:
		for word in line:
			wordSet.add(word)
			wordList.append(word)
	#执行力对
	wordSet.remove(" ")
	print(len(wordSet))
	listLength = len(wordList)
	'''
	wordDict = {}
	for word in wordSet:
		for i in range(listLength):
			if wordList[i]==word and i!=listLength-1:
				key = word+":"+wordList[i+1]
				if key not in wordDict:
					wordDict[key] = 1
				else:
					wordDict[key] += 1
				
	str = json.dumps(wordDict,ensure_ascii=False)			
	out = open('fre.txt','w',encoding="UTF-8")
	out.write(str)
	out.close()
	'''
	dictArr = loadDictionary('CoreNatureDictionary.txt');
	
	fopen2 = open('CoreNatureDictionary.txt','r',encoding="UTF-8")
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
	print(set1)
	output = "";
	for i in range(listLength):
		output += wordList[i]
		for index in set1:
			if index == i:
				output += "/"
	fopen2.close()
	fopen3 = open('output.txt','w',encoding="UTF-8")
	fopen3.write(output)
	fopen3.close()
	
		
	
	
	