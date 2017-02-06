from textapp import TextConversationAnalyzer
import unittest

####UNITTEST FWK######
class TestTextConversationAnalyzerStaticMethods(unittest.TestCase):

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

	CONVO_1 = "sample_conversations/sample1.csv"
	CONVERSATIONS= [ CONVO_1 ]

	def __init__(self, *args, **kwargs):
		super(TestTextConversationAnalyzerStaticMethods, self).__init__(*args, **kwargs)
		self.analyzer = TextConversationAnalyzer()

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
		self.assertEqual(self.analyzer.wordCount(self.TEXT_8), 5)
		self.assertEqual(self.analyzer.wordCount(self.TEXT_9), 5)

	def test_word_count_unique(self):
		pass

	def test_mode_text_time(self):
		pass

	def test_relative_word_frequency(self):
		pass

	def test_average_word_per_text(self):
		self.assertEqual(self.analyzer.avgWordsPerText(self.TEXTS), 24.0/9.0)

	def test_unique_word_count(self):
		pass

	def test_avg_sent_without_response(self):
		pass

	def test_ratio_sent_received(self):
		pass

if __name__ == '__main__':
    unittest.main()


