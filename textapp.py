#TODO: 
#Come up with some sort of character escaping scheme for including commas in texts
#	Figure out first how conversations are exported
#
#Add support for PyUnit for automated testing
#	IN PROGRESS
#
#Remove any assumptions about the number of partiipants in each conversation
#	so that this can also work for group conversations
#
#Determine which methods should be static
#	We could have *every* method be static, and simply have a wrapper instance function that
#	passes (for example) a long list of times or texts to a static analysis function.
#	Or perhaps a hybrid of the two? Each function may be a static or instance function on a case-by-case basis
#	What are the pros and cons of each approach?

import csv
from statistics import mode
from collections import *

#timesMorning = ["0:30", "1:20", "2:00", "3:00", "0:45", "1:25", "2:37", "2:10"]
class TextConversationAnalyzer:

	####CONSTANTS#########
	CSV_TIMESTAMP = 0
	CSV_SENDER = 1
	CSV_RECEIVER = 2
	CSV_DIGEST = 3

	####SPECIAL FUNCTIONS#
	def __init__(self):
		self.conv_file = None
		self.reader = None

	def __init__(self, conversation_file_name):
		#This is probably bad juju, so fix it soon
		self.conv_file = open(conversation_file_name)
		self.reader = csv.reader(conv_file)
		#Add initialization stuff for generating texting thresholds for individual participants

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
			totalWords += wordCount(text)

		return float(totalWords)/len(texts)

	@staticmethod
	def wordCount(text):
		tokens = tokenizeStr(text)
		return len(tokens)

	@staticmethod
	def modeTextTime(times): #assumes times in military time for now, of form (string) mm/dd/yyyy/hh:mm:ss
		hours = []

		for csv_row in reader:
			if len(csv_row) < CSV_DIGEST + 1:
				continue
			hour = csv_row[CSV_TIMESTAMP][-8:-6] #TODO: remove magic numbers
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
		participants = countWordsByParticipant(word_list)
		result = {}
		
		#print(participants)
		for participant, participant_counter in participants.items():
			#Convert counter to dict for result
			print(participant)
			result[participant] = dict(participant_counter)
			total = sum(participant_counter.values())

			for result_word, result_count in result[participant].items():
				if total > 0.0:
					result[ participant ][ result_word ] = float(result_count)/float(total)

			for word in word_list:
				if word not in result[participant]:
					result[ participant ][ word ] = 0.0
		
		reset_conv_file()
		return result

	def countWordsByParticipant(self, word_list):
		participants = {}
		for csv_row in reader:
			if len(csv_row) < CSV_DIGEST + 1:
				continue
			tokens = tokenizeStr(csv_row[CSV_DIGEST])
			sender = csv_row[CSV_SENDER]
			for token in tokens:
				#a to_upper or to_lower will be needed here
				if token in word_list:
					if not participants.get( sender, False ):
						participants[ sender ] = Counter()
					participants[ sender ][ token ] += 1

		reset_conv_file()
		return participants

	def countWordsUnique(reader):
		pass

	####OTHER#############

	#Returns a list of strings that comprise string/list of words in the text
	#	basically our souped up version of str.split()
	@staticmethod
	def tokenizeStr(text):
		replacedCommas = replaceChar(',', ' ', text)
		return replacedCommas.split()

	#Replace this
	@staticmethod
	def replaceChar(ch_target, ch_replace, text):
		replaced = ""
		for ch in text:
			if ch == ch_target:
				replaced += ch_replace
			else:
				replaced += ch
		return replaced 
print("here")
#a = TextConversationAnalyzer()
print("here1")
a = TextConversationAnalyzer("sample_conversations/sample1.csv")
print("here2")

