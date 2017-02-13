import csv
import string
from statistics import mode
from collections import *


#TODO: 
#Come up with some sort of character escaping scheme for including commas in texts
#	Figure out first how conversations are exported
#
#
#Remove any assumptions about the number of partiipants in each conversation
#	so that this can also work for group conversations
#
#Determine which methods should be static
#	We could have *every* method be static, and simply have a wrapper instance function that
#	passes (for example) a long list of times or texts to a static analysis function.
#	Or perhaps a hybrid of the two? Each function may be a static or instance function on a case-by-case basis
#	What are the pros and cons of each approach?
#
#Come up with a cohesive naming scheme for static/util/instance methods
#
#Find a better object representation for Analyzer class. It might not make sense to have
#	only one conversation be analyzed per instance of the class. 

#timesMorning = ["0:30", "1:20", "2:00", "3:00", "0:45", "1:25", "2:37", "2:10"]
class TextConversationAnalyzer(object):

	####TRANSLATION#######
	IN_PUNC  = ",<.>/?;:\"{[}]|\\!@#$%^&*()-_=+"
	OUT_PUNC = "                             "
	TRANSLATOR = str.maketrans(IN_PUNC, OUT_PUNC)
	####CONSTANTS#########
	CSV_TIMESTAMP = 0
	CSV_SENDER = 1
	CSV_RECEIVER = 2
	CSV_DIGEST = 3

	####SPECIAL FUNCTIONS#
	def __init__(self, *args, **kwargs):
		conv_fname = kwargs.get("conversation_fname", None)

		if(conv_fname):
			self.conv_file = open(conv_fname)
			self.reader = csv.reader(self.conv_file)
		else:
			self.conv_file = None
			self.reader = None

	def __del__(self):
		if(self.conv_file is not None):
			self.conv_file.close()

	####CLASS UTILITIES###
	def reset_conv_file(self):
		if(self.conv_file is not None):
			self.conv_file.seek(0)
	####SENTENCE##########

	####TEXT##############
	@staticmethod
	def avgWordsPerText(texts):
		totalWords = 0
		for text in texts:
			totalWords += TextConversationAnalyzer.wordCount(text)

		return float(totalWords)/len(texts)

	@staticmethod
	def wordCount(text):
		tokens = TextConversationAnalyzer.tokenizeStr(text)
		return len(tokens)

	@staticmethod
	def modeTextTime(times): #assumes times in military time for now, of form (string) mm/dd/yyyy/hh:mm:ss
		hours = []

		for csv_row in self.reader:
			if len(csv_row) < self.CSV_DIGEST + 1:
				continue
			hour = csv_row[self.CSV_TIMESTAMP][-8:-6] #TODO: remove magic numbers
			hours.append(hour)
		return "You normally text during: " + mode(hours)    #Need to make mode function work!! Ties?

	def avgTextTime(times):
		pass

	#Times 0 to 23 are blocked as follows:
	#1-5: booty caller, 6-10: early morning, 11-3: midday, 4-9: evening, 10-1: night owl
	#TODO: Change this fn name
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
	def ratioSentReceived():
		pass

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
	def avgSentWithoutResponse():
		pass

	def avgSentWithoutResponseWindow(window):
		pass

	def uniqueWordCount():
		pass

	#Accepts a list of words to calculate relative percentages
	#Returns a list of percentages
	#e.g. input ["u", "you"] returns [0.4, 0.6] for someone who uses 'u' %40 of the time
	#when compared with you

	#Returns a dictionary of participants of the form
	#{{"name1":{"word1":<percentage1>, "word2":<percentage2>,...}, "name2": {...}, ...}
	def relativeWordFrequency(self, word_list):
		participants = countWordsByParticipant()
		result = {}
		
		#print(participants)
		for participant, participant_counter in participants.items():
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

		self.reset_conv_file()
		return result

	def countWordsByParticipant(self):
		participants = {}
		for csv_row in self.reader:
			if len(csv_row) < self.CSV_DIGEST + 1:
				continue
			tokens = self.tokenizeStr(csv_row[self.CSV_DIGEST])
			sender = csv_row[self.CSV_SENDER]
			for token in tokens:
				#a to_upper or to_lower will be needed here
				if not participants.get( sender, False ):
					participants[ sender ] = Counter()
				participants[ sender ][ token ] += 1

		self.reset_conv_file()
		return participants

	#Returns a dictionary of {participant : word count}
	def countWordsUniqueByParticipant(self):
		participants = self.countWordsByParticipant()
		participant_word_count = {}

		for participant, participant_counter in participants.items():
			participant_word_count[participant] = len(participant_counter.keys())

		return participant_word_count

	#Returns the count of unique words used in the conversation
	def countWordsUnique(self):
		participant_word_count = self.countWordsByParticipant()
		word_set = set()

		for participant, participant_counters in participant_word_count.items():
			word_set = word_set | set(participant_counters.keys())

		return len(word_set)

	####OTHER#############

	#Returns a list of strings that comprise string/list of words in the text
	#	basically our souped up version of str.split()
	@staticmethod
	def tokenizeStr(text):
		replacedCommas = text.translate(TextConversationAnalyzer.TRANSLATOR)
		return replacedCommas.split()
