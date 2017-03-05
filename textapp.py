import csv
import string
import bisect
import logging

from statistics import mode
from collections import *
from datetime import datetime, timedelta

#TODO: 
#Come up with some sort of character escaping scheme for including commas in texts
#	Figure out first how conversations are exported
#	Could simply reconstruct the message with commas inserted]
#
#Determine which methods should be static
#	We could have *every* method be static, and simply have a wrapper instance function that
#	passes (for example) a long list of times or texts to a static analysis function.
#	Or perhaps a hybrid of the two? Each function may be a static or instance function on a case-by-case basis
#	What are the pros and cons of each approach?
#
#Come up with a cohesive naming scheme for static/util/instance methods 
#
#Come up with a more intuitive way of organizing functions rather than conversation/etc.
#
#Refactor the below class into a "Conversation" object; enable an "Analyzer" class to process
#	multiple conversation objects
#
#Add decent input verification
#
#Add some way to responsibly raise and handle errors (i.e. window errors)

class TextAnalyzer(object):

	#Refactor the following into 'conversations'
	####TRANSLATION#######
	DEFAULT_DATE_FORMAT = "%m/%d/%Y/%H:%M:%S"
	#This is begging for refactoring
	IN_PUNC  = ",<.>/?;:\"{[}]|\\!@#$%^&*()-_=+"
	OUT_PUNC = "                             "
	_translator = str.maketrans(IN_PUNC, OUT_PUNC)
	####CONSTANTS#########
	CSV_TIMESTAMP = 0
	CSV_SENDER = 1
	CSV_RECEIVER = 2
	CSV_DIGEST = 3

	####SPECIAL FUNCTIONS#
	def __init__(self, *args, **kwargs):
		conv_fname = kwargs.get("conversation_fname", None)
		sender = kwargs.get("sender", None)
		
		self.conv = []
		self._index = []
		if(conv_fname):
			with open(conv_fname) as conv_file:
				reader = csv.reader(conv_file)
				for csv_row in reader:
					self.conv.append(csv_row)
					self._index.append(datetime.strptime(csv_row[self.CSV_TIMESTAMP], 
										self.DEFAULT_DATE_FORMAT))

		self.sender = sender

	def __del__(self):
		pass
		#if(self.conv_file is not None):
		#	self.conv_file.close()

	####CLASS UTILITIES###
	def reset_conv_file(self):
		pass
		#if(self.conv_file is not None):
		#	self.conv_file.seek(0)
	####SENTENCE##########

	####TEXT##############
	def avgTextTime(times):
		pass

	#Times 0 to 23 are blocked as follows:
	#1-5: booty caller, 6-10: early morning, 11-3: midday, 4-9: evening, 10-1: night owl
	
	def amToPm(times):
		pass

	def avgTextBlocks():
		pass

	def avgTextsPerHour():
		pass

	def textFirst():
		pass

	####CONVERSATION######
	#window is a tuple of two datetime objects, signifiying the beginning and end of 
	#the window
	def ratioSentReceived(self, window):
		
		if(self.sender is None):
			logging.warn("sender is none")
			return

		sent = 0
		received = 0
		begin = self.findBeginWindow(window[0]) if window else self.findBeginWindow(None) 
		end = self.findEndWindow(window[1]) if window else self.findEndWindow(None)

		logging.debug("begin window: %u, end window: %u", begin, end)
		for csv_row in self.conv[begin:end+1]:
			if len(csv_row) < self.CSV_DIGEST + 1:
				continue
			timestamp = datetime.strptime(csv_row[TextAnalyzer.CSV_TIMESTAMP], self.DEFAULT_DATE_FORMAT)
			
			if(self.dateInWindow(timestamp, window)):
				if(self.sender == csv_row[TextAnalyzer.CSV_SENDER]):
					sent += 1
				else:
					received += 1
		logging.debug("sent: %u received: %u", sent, received)
		return  sent/received if received > 0.0 else 0.0
		
	#	  This could get pretty fancy. Right now our criteria for 'response' is literally just that a text
	#	was sent from Alice to Bob after Bob sent one to Alice. This isn't quite accurate though. For example,
	#	we may not wish to consider a text sent from Alice to Bob 3 months after Bob initially texted as a 
	#	'response.' So, there should be some sort of time period within which a sent text would be considered
	# 	a 'response'. But this window won't be the same for all texters... some people are simply slower to
	#	respond than others. Down the line, we may wish to calculate the average response time for both
	#	participants and individually calculate a window within which a text sent would be considered a
	#	response (e.g. within 2 std devs of the average response time)
	#
	#     I agree it's a good thought. I would go further to say that the pace of texting varies within different conversations between
	#   the same people. This means we could separate the entire digest into conversations based off of obviously longer breaks between
	#   subsequent conversations. Then we could apply your method to each conversation block.
	def avgSentWithoutResponse(self):
		pass

	def avgSentWithoutResponseWindow(self, window):
		pass

	#Accepts a list of words to calculate relative percentages
	#Returns a list of percentages
	#e.g. input ["u", "you"] returns [0.4, 0.6] for someone who uses 'u' %40 of the time
	#when compared with you

	#Returns a dictionary of participants of the form
	#{{"name1":{"word1":<percentage1>, "word2":<percentage2>,...}, "name2": {...}, ...}
	def relativeWordFrequency(self, word_list, window):
		participants = self.wordUsageByParticipant(window)
		result = {}
		
		#print(participants)
		for participant, participant_counter in participants.items():
			result[participant] = {} 
			#Only add words from the word list to the result dict
			total = 0
			for word in word_list:
				if participant_counter.get(word, False):
					count = participant_counter[word]
					result[participant][word] = count
					total += count
				else:
					result[participant][word] = 0
			

			for result_word, result_count in result[participant].items():
				if total > 0.0:
					result[participant][result_word] = float(result_count)/float(total)

		return result


	def wordUsageByParticipant(self, window):
		participants = {}

		begin = self.findBeginWindow(window[0]) if window else self.findBeginWindow(None) 
		end = self.findEndWindow(window[1]) if window else self.findEndWindow(None)

		for csv_row in self.conv[begin:end+1]:
			if len(csv_row) < self.CSV_DIGEST + 1:
				continue
			tokens = self.tokenizeStr(csv_row[self.CSV_DIGEST])
			sender = csv_row[self.CSV_SENDER]
			for token in tokens:
				#a to_upper or to_lower will be needed here
				if not participants.get( sender, False ):
					participants[ sender ] = Counter()
				participants[ sender ][ token ] += 1

		return participants

	#TODO
	def mostCommonWords(self, num, participants, window):
		participants = self.wordUsageByParticipant(window)
		pass

	#Returns a dictionary of {participant : word count}
	def uniqueWordCountByParticipant(self, window):
		participants = self.wordUsageByParticipant(window)
		participant_word_count = {}

		for participant, participant_counter in participants.items():
			participant_word_count[participant] = len(participant_counter.keys())

		return participant_word_count

	#Returns the count of unique words used in the conversation
	def uniqueWordCount(self, window):
		participant_word_count = self.wordUsageByParticipant(window)
		word_set = set()

		for participant, participant_counters in participant_word_count.items():
			word_set = word_set | set(participant_counters.keys())

		return len(word_set)

	#Returns the index with smallest date ocurring after or on the argument
	#geq
	def findBeginWindow(self, date):
		if date is None:
			return 0
		i = bisect.bisect_left(self._index, date)
		if(i != len(self._index)):
			return i
		return -1

	#Returns the index with largest date ocurring before or on the argument 
	#leq
	def findEndWindow(self, date):
		if date is None:
			return len(self.conv)-1
		i = bisect.bisect_right(self._index, date)
		if(i):
			return i-1
		return -1  

	####OTHER#############
	#Returns a list of strings that comprise string/list of words in the text
	#	basically our souped up version of str.split()
	@staticmethod
	def tokenizeStr(text):
		replaced = text.translate(TextAnalyzer._translator)
		return replaced.split()

	@staticmethod
	def avgWordsPerText(texts):
		totalWords = 0
		for text in texts:
			totalWords += TextAnalyzer.wordCount(text)
		return float(totalWords)/len(texts)

	@staticmethod
	def wordCount(text):
		tokens = TextAnalyzer.tokenizeStr(text)
		return len(tokens)

	@staticmethod
	def modeTextTime(times): #assumes times in military time for now, of form (string) mm/dd/yyyy/hh:mm:ss
		hours = []

		for csv_row in self.conv:
			if len(csv_row) < self.CSV_DIGEST + 1:
				continue
			hour = csv_row[self.CSV_TIMESTAMP][-8:-6] #TODO: remove magic numbers
			hours.append(hour)
		return "You normally text during: " + mode(hours)    #Need to make mode function work!! Ties?
															 #Don't return a string
	@staticmethod
	def dateInWindow(date, window):
		if(window is None):
			return True
		(begin_window, end_window) = window
		return (date >= begin_window) & (date <= end_window)