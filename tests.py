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
		self.analyzer.reset()

	def tearDown(self):
		pass

	def test_word_count_not_unique(self):
		self.assertEqual(self.analyzer.wordCount(t1), 2)
		self.assertEqual(self.analyzer.wordCount(t2), 0)
		self.assertEqual(self.analyzer.wordCount(t3), 0)
		self.assertEqual(self.analyzer.wordCount(t4), 1)
		self.assertEqual(self.analyzer.wordCount(t5), 7)
		self.assertEqual(self.analyzer.wordCount(t6), 2)
		self.assertEqual(self.analyzer.wordCount(t7), 2)
		self.assertEqual(self.analyzer.wordCount(t8), 5)
		self.assertEqual(self.analyzer.wordCount(t9), 5)

	def test_word_count_unique():
		pass

	def test_mode_text_time():
		pass

	def test_relative_word_frequency():
		pass

	def test_average_word_per_text(self):
		self.assertEqual(self.analyzer.avgWordsPerText(TEXTS), 2.375)

	def test_unique_word_count():
		pass

	def test_avg_sent_without_response():
		pass

	def test_ratio_sent_received():
		pass

if __name__ == '__main__':
    unittest.main()


