import csv
import string
import bisect
import logging

from statistics import mean, mode
from collections import *
from datetime import datetime, timedelta

class TextAnalyzer(object):

	#Refactor the following into 'conversations'
	####TRANSLATION#######
	#Add unit testing for this
	date_fmt = "%m/%d/%Y/%H:%M:%S"
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
										self.date_fmt))

		self.sender = sender

	def __del__(self):
		pass
		
	####CLASS UTILITIES###
	def reset_conv_file(self):
		pass

	####SENTENCE##########

	####TEXT##############
	def avgTextTime(self, times):
		pass

	#Times 0 to 23 are blocked as follows:
	#1-5: booty caller, 6-10: early morning, 11-3: midday, 4-9: evening, 10-1: night owl
	
	def amToPm(self, times):
		pass

	def avgTextBlocks(self):
		pass

	def avgTextsPerHour(self):
		pass

	def textFirst(self):
		pass

	####CONVERSATION######
	#window is a tuple of two datetime objects, signifiying the beginning and end of 
	#the window
	#TODO: Change sender to argument
	def ratioSentReceived(self, window):
		
		if(self.sender is None):
			logging.warn("sender is none")
			return

		sent = 0
		received = 0
		(begin, end) = self.getWindowIndices(window)

		logging.debug("begin window: %u, end window: %u", begin, end)
		for csv_row in self.conv[begin:end+1]:
			if len(csv_row) < self.CSV_DIGEST + 1:
				continue
			timestamp = datetime.strptime(csv_row[TextAnalyzer.CSV_TIMESTAMP], self.date_fmt)
			
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
	def meanSentWithoutResponse(self, window):
		pass

	#MTTR
	#If Alice triple-texts Bob, the 3rd text from Alice is used when calculating
	#Bob's response time
	#IDEA: Could pre-sort messages into separate lists based on sender at cost of memory
	#Should return both stddev and average
	def meanTimeToRespond(self, participant, window):
		(begin, end) = self.getWindowIndices(window)
		deltas = []
		#Make sure the responded-to text is not outside the window
		responding = False
		for i, csv_row in enumerate(self.conv[begin:end+1]):
			#Find first message sent from someone other than participant
			if participant == csv_row[self.CSV_SENDER] and responding:
				deltas.append(self.getTimeBetweenTexts(i-1, i))
				responding = False
			elif participant != csv_row[self.CSV_SENDER]:
				responding = True
		logging.debug("deltas: " + deltas.__str__())
		#TODO: Cannot directly average these timedeltas, find another way
		return sum(deltas, timedelta()) / len(deltas)

	#TODO: implement these responsibly (safe, including exceptions, etc.) and
	#remove all raw self.conv[ind][field] - style accesses in code

	#def getTextTime(self, i):
	#def getTextMessage(self, i):
	#def getTextReceiver(self, i):
	#def getTextSender(self, i):

	def getTimeBetweenTexts(self, t1_ind, t2_ind):
		last_text_time = datetime.strptime(self.conv[t1_ind][self.CSV_TIMESTAMP], self.date_fmt)
		this_text_time = datetime.strptime(self.conv[t2_ind][self.CSV_TIMESTAMP], self.date_fmt)
		logging.debug(last_text_time)
		logging.debug(this_text_time)
		return this_text_time - last_text_time
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

		(begin, end) = self.getWindowIndices(window)
 		
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

	#Returns a map from participant to a list of at most top_n words sorted in order
	#of usage
	#TODO: add support for most common words, regardless of participant
	def mostCommonWords(self, top_n, participant_list, window):
		participants = self.wordUsageByParticipant(window)
		selected_participants = {}

		for participant in participant_list:
			selected_participants[participant] = participants[participant].most_common(top_n)
		
		return selected_participants

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

	def getWindowIndices(self, window):
		begin = self.findBeginWindow(window[0]) if window else self.findBeginWindow(None) 
		end = self.findEndWindow(window[1]) if window else self.findEndWindow(None)
		indices = (begin, end)
		logging.debug(indices)
		return (indices)
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
