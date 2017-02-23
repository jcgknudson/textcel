from textapp import TextAnalyzer
from datetime import datetime, timedelta
import unittest

#TODO:
#Come up with a better way to structure these tests rather than separating
#	test cases by static and instance methods. Additionally, find a better
#	way to test multiple conversations without having to create a new 
#	test class. This may need to be changed in TextAnalyzer	 

####UNITTEST FWK######
class TestTextAnalyzerMethods(unittest.TestCase):
	####Unique word count: ~27 (both), 14 (Jack), 16(Niki)
	####Average sent without response: 
	####Relative word frequency: Jack [0.33, 0.66] (you vs u), Niki [0.0, 1.0] (you vs u)

	CONVO_1 = "sample_conversations/sample1.csv"
	CONVERSATIONS = [ CONVO_1 ]

	def __init__(self, *args, **kwargs):
		super(TestTextAnalyzerMethods, self).__init__(*args, **kwargs)
		self.analyzer = TextAnalyzer(conversation_fname = self.CONVO_1, sender = "John Knudson")

	def setUp(self):
		self.analyzer.reset_conv_file()

	def tearDown(self):
		pass

	def test_word_count_unique(self):
		expected = 27
		self.assertEqual(self.analyzer.uniqueWordCount(None), expected)

	def test_word_count_by_participant(self):
		expected = {"John Knudson": 14, "Niki Waghani": 16}
		window = None
		self.assertEqual(self.analyzer.uniqueWordCountByParticipant(window), expected)

	def test_relative_word_frequency(self):
		expected = {"John Knudson":{"you": 1.0/3.0, "u": 2.0/3.0}, "Niki Waghani": {"you": 1.0, "u": 0.0}}
		window = None
		self.assertEqual(self.analyzer.relativeWordFrequency(["u", "you"], window), expected)

	def test_ratio_sent_received_no_window(self):
		expected = 3.0/6.0
		window = None
		self.assertEqual(self.analyzer.ratioSentReceived(window), expected)

	def test_ratio_sent_received(self):
		expected = 2.0/6.0
		begin_time = datetime(year=1994, month=8, day=17, hour=0, minute=0, second=0)
		end_time = datetime(year=1994, month=8, day=17, hour=1, minute=40, second=0) 
		window = (begin_time, end_time)
		self.assertEqual(self.analyzer.ratioSentReceived(window), expected)

class TestTextAnalyzerIndex(unittest.TestCase):
	DATES_1 = "sample_conversations/sample_dates1.csv"
	DATES = [DATES_1]

	def __init__(self, *args, **kwargs):
		super(TestTextAnalyzerIndex, self).__init__(*args, **kwargs)
		self.analyzer = TextAnalyzer(conversation_fname = self.DATES_1, sender = "A")

	def setUp(self):
		self.analyzer.reset_conv_file()

	#Supplied date is before first text
	def test_index_output_edge_before(self):
		expected = 0
		date = datetime(year=1998, month=11, day=17, hour=5, minute=0, second=0)
		self.assertEqual(self.analyzer.findDateIndex(date), expected)
	
	#Supplied date is after last text
	def test_index_output_edge_after(self):
		expected = -1
		date = datetime(year=2000, month=11, day=17, hour=5, minute=0, second=0)
		self.assertEqual(self.analyzer.findDateIndex(date), expected)

	def test_index_output(self):
		expected_1 = 5
		expected_2 = 13
		expected_3 = 22
		expected_4 = 24

		w1_begin = datetime.strptime("01/25/1999/23:30:54", TextAnalyzer.DEFAULT_DATE_FORMAT)
		w2_begin = datetime.strptime("02/17/1999/19:59:08", TextAnalyzer.DEFAULT_DATE_FORMAT)
		w3_begin = datetime.strptime("03/29/1999/17:41:16", TextAnalyzer.DEFAULT_DATE_FORMAT)
		w4_begin = datetime.strptime("04/05/1999/23:42:58", TextAnalyzer.DEFAULT_DATE_FORMAT)

		self.assertEqual(self.analyzer.findDateIndex(w1_begin), expected_1)
		self.assertEqual(self.analyzer.findDateIndex(w2_begin), expected_2)
		self.assertEqual(self.analyzer.findDateIndex(w3_begin), expected_3)
		self.assertEqual(self.analyzer.findDateIndex(w4_begin), expected_4)

class TestTextAnalyzerStaticMethods(unittest.TestCase):

	TEXT_1 = "hello world"
	TEXT_2 = " "
	TEXT_3 = ""
	TEXT_4 = "singleword"
	TEXT_5 = "hello this is niki, What's up? bye."
	TEXT_6  = "   spaces before"
	TEXT_7 = "spaces after     "
	TEXT_8 = " a a a %^ &a^ "
	TEXT_9 = "hello,goodbye,see,you,soon"
	TEXTS = [TEXT_1, TEXT_2, TEXT_3, TEXT_4, TEXT_5, TEXT_6, TEXT_7, TEXT_8, TEXT_9]

	def __init__(self, *args, **kwargs):
		super(TestTextAnalyzerStaticMethods, self).__init__(*args, **kwargs)
		self.analyzer = TextAnalyzer()

	def setUp(self):
		self.analyzer.reset_conv_file()

	def tearDown(self):
		pass

	def test_word_count_not_unique(self):
		self.assertEqual(self.analyzer.wordCount(self.TEXT_1), 2)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_2), 0)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_3), 0)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_4), 1)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_5), 7)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_6), 2)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_7), 2)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_8), 4)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_9), 5)

	def test_mode_text_time(self):
		pass

	def test_average_word_per_text(self):
		self.assertEqual(self.analyzer.avgWordsPerText(self.TEXTS), 23.0/9.0)

if __name__ == '__main__':
    unittest.main()


