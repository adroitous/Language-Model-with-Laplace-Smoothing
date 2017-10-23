import decimal
import math
import random
import string
import nltk
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class NLP1:

	def __init__(self, n, text):
		self.n = n 
		self.text = text
		
		#belowed is used for solving problem 1
		#self.openfileProblem1(text)


		#belowed is used for solving problem 3
		#self.openfileProblem3(text)

		self.openfileProblem4(text)
		self.dictionary()

		#used for counting words
		#self.printCount()

		#used for counting probability, takes the amount to keep track of: so top 10 and top 20 probability
		#self.printProbability(10)
		#self.printProbability(20)

	#used for parsing line for number 1 no preprocessing	
	def openfile(self, filename):
		text = open(filename, "r")
		lines = text.readlines()
		tokenA = []
		for line in lines:
			tokenA = tokenA+line.split()
		self.tokenA = tokenA

	#used for parsing line for number 3 preprocessing includes lowercase
	def openfileProblem3(self, filename):
		text = open(filename, "r")
		lines = text.readlines()
		tokenA = []
		for line in lines:
			tokenA = tokenA+["<s>"]+line.lower().split()+["</s>"]
		self.tokenA = tokenA
		self.globalTotal = len(tokenA)
		#print self.globalTotal

	#used for parsing line for number 4 preprocessing includes lowercase also uses NLTK library
	def openfileProblem4(self, filename):
		text = open(filename, "r")
		lines = text.read()
		sentTokens = nltk.sent_tokenize(lines)
		Tokens = []
		for sentToken in sentTokens:
			Tokens = Tokens+["$"]+[sentToken]+["#"]
		Token = []
		#print "Token"
		#print Token
		for element in Tokens:
			Token = Token + nltk.word_tokenize(element.lower())
		#print Token
		self.tokenA = Token
		self.globalTotal = len(Token)

		#print Token

	#generate the dictionary and generate the string with probability
	def dictionary(self):
		UnigramDic = {}
		# unigram model
		# I added the unigram dictionary specifically to tally the number of unique words in the text.
		# the unigram dictionary is also used to give every possible in the Laplace Smoothing technique
		for tokenValue in self.tokenA:
			if tokenValue in UnigramDic:
				#will add one for Laplace Smoothing in the probabilityDic section
				UnigramDic.update({tokenValue: UnigramDic.get(tokenValue)+1})
			else: 
				UnigramDic.update({tokenValue: 1})
		self.UnigramDic =UnigramDic

		#print UnigramDic
		#n-1 model
		dic={}
		n1dic={}

		#generate the probability for words in the dictionary
		NgramCount = self.ngramdic(self.n, dic)	
		N1gramCount= self.ngramdic(self.n-1, n1dic)
		self.dic = dic
		self.n1dic = n1dic

		#keep track of top 10
		probabilityDic = {}
		self.probabilityDic = {}

		#number of unique words/word types used in the calculation of probability 
		N = float(len(UnigramDic))

		#generate the probability for the elements in the dictionary used for number 2 and 3
		for alltoken in dic:
			self.probability(alltoken, dic, n1dic, N)	

		#used to generate string for number 4 
		#starting with "$" 
		startingString = "$"
		print "Ngram is " +str(self.n)
		#repeat 5 times for 5 different sentences
		for x in xrange(5):
			adjustedString = " ".join(startingString.split(" ")[-(self.n-1):])
			#generate the the 10 words or when the "#" appears
			for _ in xrange(10):
				adjustedString = self.generation(adjustedString, dic, n1dic, N)
				# break the loop if the last word breaks with "#" 
				if adjustedString.split()[-1]== "#":
					break
			print adjustedString + ".\\"

	#print the sorted count of the data structure
	#print out the unigram and the bigram for Question number 1. 
	def printCount(self):
		#for unigram
		print sorted(self.UnigramDic.items(), key = lambda a:a[1])[::-1][:10]
		#for all  N grams use this line to print out 
		print sorted(self.dic.items(), key = lambda a:a[1])[::-1][:10]

	#generate the string by applying generating the probability given the starting adjusted string
	#this method makes it faster to repeat
	def generation(self, adjustedString, dic, n1dic, N):
		pd = self.generateProbability(adjustedString, dic, n1dic, N)	
		string = self.generateString(pd)
		return string

	#print the probability for questions 2 and 3
	def printProbability(self, int):
		print sorted(self.probabilityDic.items(), key = lambda a:a[1])[::-1][:int]

	#generate the ngram count and the ngram dictionary, which allows us to use the same method for n-1 gram
	def ngramdic(self, number, dic):
		#the NgramCount allows us to calculate the specifics token counts for probability calculation
		NgramCount = 0
		for i in range(0, len(self.tokenA)-number+1):
			tokenValue = self.tokenA[i:i+number]
			tokens = " ".join(tokenValue)
			if tokens in dic:
				dic.update({tokens: dic.get(tokens)+1})
				NgramCount+=1
			else: 
				dic.update({tokens: 1}) 
				NgramCount+=1
		return NgramCount

	#used to calculate the probability of a given sentence
	#return the probability and update the probability dictionary for given N grams
	def probability(self, completeText, NgramHistory, N1gramHistory, N):
		#split the complete text into given text, so the string with n-words and without the last word a
		giventext = completeText.split(' ', self.n-1)[self.n-2]
		if giventext in N1gramHistory:
			Historyminus = N1gramHistory.get(giventext)
		else:
			Historyminus = 0.0
		#special case for unigram
		if self.n ==1:
				Historyminus = self.globalTotal
		#find the completeText in dictionary and update the dictionary(HIstory) count
		if completeText in NgramHistory:
			History = NgramHistory.get(completeText)
		else:
			History = 0.0
		#calculate the probability
		self.probabilityDic.update({completeText: float((History+1)/(Historyminus+N))})
		#calculate the probability
		return float((History+1)/(Historyminus+N))

	def generateProbability(self, adjustedString, NgramHistory, N1gramHistory, N):
		probabilityD ={}
		for everyWord in self.UnigramDic:
			#combine the given strings with every possible word in the corpus as given by the unigram
			word = adjustedString+" "+everyWord
			History = 0.0
			Historyminus =0.0
			NgramHistory.get(word)
			#find the completeText in dictionary and update the dictionary(HIstory) count
			if word in NgramHistory:
				History = NgramHistory.get(word)
			if adjustedString in N1gramHistory:
				Historyminus = N1gramHistory.get(adjustedString)
			#special case for unigram
			if self.n ==1:
				Historyminus = self.globalTotal
			#calculate the probability
			prob = float((History+1)/(Historyminus+N))
			probabilityD.update({word:prob})

		return probabilityD

	#generate the string 
	def generateString(self, probabilityDictionary):
		total = sum(probabilityDictionary.itervalues())
		r = random.uniform(0, total)
		upto = 0
		#use the randomly generatedly number to map to a given probability range in the sum and 
		#and use that value to map to a specific string
		for value in probabilityDictionary.values():
			if upto + value >= r:
				w =  probabilityDictionary.popitem()
				return w[0]
			else: 
				upto += value
				probabilityDictionary.popitem() 


#run for specfic problmes
#problem1and2 = NLP1(1, "sam.txt")
#problem1and2 = NLP1(2,"sam.txt")
#problem3 = NLP1(2, "moviescript.txt")
#problem4 = NLP1(5, "bronte_jane_eyre.txt")
#problem4 = NLP1(4, "bronte_jane_eyre.txt")
#problem4 = NLP1(3, "bronte_jane_eyre.txt")
#problem4 = NLP1(2, "bronte_jane_eyre.txt")
#problem4 = NLP1(1, "bronte_jane_eyre.txt")
