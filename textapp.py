#TODO: 
#Come up with some sort of character escaping scheme for including commas in texts
#	Figure out first how conversations are exported
#
#Add support for PyUnit for automated testing
#
#Remove any assumptions about the number of partiipants in each conversation
#	so that this can also work for group conversations

import csv

t1 = "hello world"
t2 = " "
t3 = ""
t4 = "singleword"
t5 = "hello this is niki, What's up? bye."
t6  = "   spaces before"
t7 = "spaces after     "
t8 = " a a a %^ &a^ "
t9 = "hello,goodbye,see,you,soon"
texts = [t1, t2, t3, t4, t5, t6, t7, t8]

f1 = "sample1.csv"
#timesMorning = [0:30, 1:20, 2:00, 3:00, 0:45, 1:25, 2:37]

####CONSTANTS#########
CSV_TIMESTAMP = 0
CSV_SENDER = 1
CSV_RECEIVER = 2
CSV_DIGEST = 3

####SENTENCE##########

####TEXT##############
def avgWordsPerText(texts):
	totalWords = 0
	for text in texts:
		totalWords += wordCount(text)

	return float(totalWords)/len(texts)

def wordCount(text):
	tokens = tokenizeStr(text)
	return len(tokens)

def modeTextTime(times): #assumes times in military time for now, of form hour:minutes
	pass

def avgTextTime(times):
	pass

#Times 0 to 23 are blocked as follows:
#1-5: booty caller, 6-10: early morning, 11-3: midday, 4-9: evening, 10-1: night owl
def textAnalysis(times):
	pass

def amToPm(times):
	pass

def avgTextBlocks():
	pass

def avgTextsPerHour():
	pass

def textFirst():
	pass

####CONVERSATION######
def ratioSentReceived(reader):
	pass

#This could get pretty fancy. Right now our criteria for 'response' is literally just that a text
#	was sent from Alice to Bob after Bob sent one to Alice. This isn't quite accurate though. For example,
#	we may not wish to consider a text sent from Alice to Bob 3 months after Bob initially texted as a 
#	'response.' So, there should be some sort of time period within which a sent text would be considered
# 	a 'response'. But this window won't be the same for all texters... some people are simply slower to
#	respond than others. Down the line, we may wish to calculate the average response time for both
#	participants and individually calculate a window within which a text sent would be considered a
#	response (e.g. within 2 std devs of the average response time)
def avgSentWithoutResponse(reader):
	pass

def avgSentWithoutResponseWindow(reader, window):
	pass

def uniqueWordCount(reader):
	pass

#Accepts a list of words to calculate relative percentages
#Returns a list of percentages
#e.g. input ["u", "you"] returns [0.4, 0.6] for someone who uses 'u' %40 of the time
#when compared with you

#Returns a dictionary of participants of the form
#{{"name1":{"word1":<percentage1>, "word2":<percentage2>,...}, "name2": {...}, ...}
def relativeWordFrequency(reader, word_list):
	participants = {}
	result = {}
	for row in reader:
		tokens = tokenizeStr(row[CSV_DIGEST])
		for token in tokens:
			if token in word_list:
				participants[ row[CSV_SENDER] ][ token ] += 1
	
	for particpant in participants:
		total = 0
		for word in particpant:
			total += word.value
			result[ participant.key ][ word.key ] = float(word.value)
		for result_word in result[particpant.key]:
			if total > 0.0:
				result_word.value = result_word.value/float(total)
			else:
				result_word.value = 0.0

	return result
####OTHER#############

#Replace this with some regexp
def replaceChar(ch_target, ch_replace, string):
	replaced = ""
	for ch in text:
		if ch == ch_target:
			replaced += ch_replace
		else:
			replaced += ch
	return replaced 

#Returns a list of strings that comprise string/list of words in the text
#	basically our souped up version of str.split()
def tokenizeStr(string):
	replacedCommas = replaceChar(',', ' ', text)
	return string.split()

def myAssert(a, b):
	if a == b:
		print "Correct!"
	else:
		print "expected: " + str(b) + ", result: " + str(a)

####TESTS#############
def testWrapper(fname):
	with open(fname) as csvfile:
		reader = csv.reader(csvfile)
		testCSV(reader)
		testRelativeWordFrequency(reader)
		testUniqueWordCount(reader)
		testAvgSentWithoutResponse(reader)
		testRatioSentReceived(reader)

def testRelativeWordFrequency(reader):
	print(relativeWordFrequency(reader, ["u", "you"]))

def testUniqueWordCount(reader):
	pass

def testAvgSentWithoutResponse(reader):
	pass

def testRatioSentReceived(reader):
	pass

def testCSV(reader):
	for row in reader:
		print(row)
	

#myAssert(wordCount(t1), 2)
#myAssert(wordCount(t2), 0)
#myAssert(wordCount(t3), 0)
#myAssert(wordCount(t4), 1)
#myAssert(wordCount(t5), 7)
#myAssert(wordCount(t6), 2)
#myAssert(wordCount(t7), 2)
#myAssert(wordCount(t8), 5)
#myAssert(wordCount(t9), 5)
#myAssert(avgWordsPerText(texts), 2.375)

testWrapper(f1)

