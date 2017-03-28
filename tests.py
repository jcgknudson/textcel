import unittest
import logging

from textapp import TextAnalyzer
from utils import create_window
from datetime import datetime, timedelta

#TODO:
#Come up with a better way to structure these tests rather than separating
#   test cases by static and instance methods. Additionally, find a better
#   way to test multiple conversations without having to create a new 
#   test class. This may need to be changed in TextAnalyzer  
#Add more conversations


#Base class that tests the majority of the functionality of the analyzer. To add more
#conversations to test, a new class that inherits from TestTextAnalyzerMethods should be
#created. The inputs and outputs for each conversation should be added as a class field
#in the initialization of the sublcass (see below in TestTextAnalyzerMethods_Conv1 for 
#an example)
class TestTextAnalyzerMethods(unittest.TestCase):
    ####Unique word count: ~27 (both), 14 (Jack), 16(Niki)
    ####Average sent without response: 
    ####Relative word frequency: Jack [0.33, 0.66] (you vs u), Niki [0.0, 1.0] (you vs u)
    def __init__(self, *args, **kwargs):
        super(TestTextAnalyzerMethods, self).__init__(*args, **kwargs)
        conversation = kwargs.get("conversation")
        sender = kwargs.get("sender")
        self.in_dict = None
        self.out_dict = None
        self.analyzer = TextAnalyzer(conversation_fname = conversation, sender = sender)
        
    def setUp(self):
        logging.info(self.id())
        self.analyzer.reset_conv_file()

    def tearDown(self):
        pass

    def test_word_count_unique(self):
        expected = self.out_dict.get("test_word_count_unique_out", None)
        inputs = self.in_dict.get("test_word_count_unique_in", None)
        self.assertEqual(self.analyzer.uniqueWordCount(inputs), expected)

    def test_word_count_unique_end_window_none(self):
        expected = self.out_dict.get("test_word_count_unique_end_window_none_out", None)
        inputs = self.in_dict.get("test_word_count_unique_end_window_none_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.uniqueWordCount(window), expected)

    def test_word_count_unique_begin_window_none(self):
        expected = self.out_dict.get("test_word_count_unique_begin_window_none_out", None)
        inputs = self.in_dict.get("test_word_count_unique_begin_window_none_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.uniqueWordCount(window), expected)
        
    def test_word_count_unique_window(self):
        expected = self.out_dict.get("test_word_count_unique_window_out", None)
        inputs = self.in_dict.get("test_word_count_unique_window_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.uniqueWordCount(window), expected)

    def test_word_count_by_participant(self):
        expected = self.out_dict.get("test_word_count_by_participant_out", None)
        inputs = self.in_dict.get("test_word_count_by_participant_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.uniqueWordCountByParticipant(window), expected)

    #TODO: ugh all of these, maybe wrap up in *subtests* (<- read docs!!!!) w/varying windows
    def test_word_usage_by_participant(self):
        pass

    #TODO: write another version using a window
    #TODO: rewrite other tests using this template (strict use of variables for parameter naming)
    def test_most_common_words(self):
        expected = self.out_dict.get("test_most_common_words_out", None)
        inputs = self.in_dict.get("test_most_common_words_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.mostCommonWords(
            inputs.get("top_n", 1), 
            inputs.get("participant_list", [""]),
            window), 
        expected)

    #TODO: write another version using a window
    def test_mean_time_to_respond(self):
        expected = self.out_dict.get("test_mean_time_to_respond_out", None)
        inputs = self.in_dict.get("test_mean_time_to_respond_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.meanTimeToRespond(
            inputs.get("sender", ""),
            window),
        expected)

    def test_relative_word_frequency(self):
        expected = self.out_dict.get("test_relative_word_frequency_out", None)
        inputs = self.in_dict.get("test_relative_word_frequency_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.relativeWordFrequency(
            inputs.get("word_list", []),
            window), 
        expected)

    def test_ratio_sent_received_no_window(self):
        expected = self.out_dict.get("test_ratio_sent_received_no_window_out", None)
        inputs = self.in_dict.get("test_ratio_sent_received_no_window_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.ratioSentReceived(window), expected)

    def test_ratio_sent_received(self):
        expected = self.out_dict.get("test_ratio_sent_received_out", None)
        inputs = self.in_dict.get("test_ratio_sent_received_in", None)
        window = create_window(inputs.get("window", None), self.analyzer.date_fmt)
        self.assertEqual(self.analyzer.ratioSentReceived(window), expected)

class TestTextAnalyzerMethods_Conv1(TestTextAnalyzerMethods):
    conversation = "sample_conversations/sample1.csv"
    sender = "John Knudson"
    def __init__(self):
        super(TestTextAnalyzer_Conv1, self).__init__(
            conversation = self.conversation,
            sender = self. sender)
        self.in_dict = {
            "test_word_count_unique_in": None,
            "test_word_count_unique_end_window_none_in": {"window": ("08/17/1994/00:00:30", None)},
            "test_word_count_unique_begin_window_none_in": {"window": (None, "08/17/1994/01:40:00")},
            "test_word_count_unique_window_in": {"window": ("08/17/1994/00:00:30", "08/17/1994/01:59:00")},
            "test_word_count_by_participant_in": {"window":None},
            "test_most_common_words_in": {"window":None, "top_n" :1, "participant_list": ["John Knudson"]},
            "test_mean_time_to_respond_in": {"window": None, "sender": "John Knudson"},
            "test_relative_word_frequency_in": {"window":None, "word_list" : ["u", "you"]},
            "test_ratio_sent_received_no_window_in": {"window":None},
            "test_ratio_sent_received_in": {"window":("08/17/1994/00:00:00", "08/17/1994/01:40:00")},
        }
        self.out_dict = {
            "test_word_count_unique_out": 27,
            "test_word_count_unique_end_window_none_out": 25,
            "test_word_count_unique_begin_window_none_out": 23,
            "test_word_count_unique_window_out": 21,
            "test_word_count_by_participant_out": {"John Knudson": 14, "Niki Waghani": 16},
            "test_most_common_words_out": {"John Knudson" : [("u", 2)] },
            "test_mean_time_to_respond_out": timedelta(minutes=((1.0+1.0+43.0)/3.0)),
            "test_relative_word_frequency_out": {"John Knudson":{"you": 1.0/3.0, "u": 2.0/3.0}, "Niki Waghani": {"you": 1.0, "u": 0.0}},
            "test_ratio_sent_received_no_window_out": 3.0/6.0,
            "test_ratio_sent_received_out": 2.0/6.0,
        }
"""
CONVO_1
test_word_count_unique_out = 27
test_word_count_unique_in = (None)

test_word_count_unique_end_window_none_out = 25
test_word_count_unique_end_window_none_in = {"window": ("08/17/1994/00:00:30", None)}

test_word_count_unique_begin_window_none_out = 23
test_word_count_unique_begin_window_none_in = {"window": (None, "08/17/1994/01:40:00")}

test_word_count_unique_window_out = 21
test_word_count_unique_window_in = {"window": ("08/17/1994/00:00:30", "08/17/1994/01:59:00")}

test_word_count_by_participant_out = {"John Knudson": 14, "Niki Waghani": 16}
test_word_count_by_participant_in = {"window":None}

test_most_common_words_out = {"John Knudson" : [("u", 2)] }
test_most_common_words_in = {"window":None, "top_n" :1, "participant_list": ["John Knudson"]}

test_mean_time_to_respond_out = timedelta(minutes=((1.0+1.0+43.0)/3.0))
test_mean_time_to_respond_in = {"window": None, "sender": "John Knudson"}

test_relative_word_frequency_out = {"John Knudson":{"you": 1.0/3.0, "u": 2.0/3.0}, "Niki Waghani": {"you": 1.0, "u": 0.0}}
test_relative_word_frequency_in = {"window":None, "word_list" : ["u", "you"]}

test_ratio_sent_received_no_window_out = 3.0/6.0
test_ratio_sent_received_no_window_in = {"window":None}

test_ratio_sent_received_out = 2.0/6.0
test_ratio_sent_received_in = {"window":("08/17/1994/00:00:00", "08/17/1994/01:40:00")}
"""


#TODO: add end window tests
class TestTextAnalyzerIndex(unittest.TestCase):
    DATES_1 = "sample_conversations/sample_dates1.csv"
    DATES = [DATES_1]

    def __init__(self, *args, **kwargs):
        super(TestTextAnalyzerIndex, self).__init__(*args, **kwargs)
        self.analyzer = TextAnalyzer(conversation_fname = self.DATES_1, sender = "A")

    def setUp(self):
        logging.info(self.id())
        self.analyzer.reset_conv_file()

    #Supplied date is before first text
    def test_begin_window_edge_before(self):
        expected = 0
        date = datetime(year=1998, month=11, day=17, hour=5, minute=0, second=0)
        self.assertEqual(self.analyzer.findBeginWindow(date), expected)
    
    #Supplied date is after last text
    def test_begin_window_edge_after(self):
        expected = -1
        date = datetime(year=2000, month=11, day=17, hour=5, minute=0, second=0)
        self.assertEqual(self.analyzer.findBeginWindow(date), expected)

    def test_begin_window(self):
        expected_1 = 5
        expected_2 = 13
        expected_3 = 22
        expected_4 = 24

        w1_begin = datetime.strptime("01/25/1999/23:30:54", self.analyzer.date_fmt)
        w2_begin = datetime.strptime("02/17/1999/19:59:08", self.analyzer.date_fmt)
        w3_begin = datetime.strptime("03/29/1999/17:41:16", self.analyzer.date_fmt)
        w4_begin = datetime.strptime("04/05/1999/23:42:58", self.analyzer.date_fmt)

        self.assertEqual(self.analyzer.findBeginWindow(w1_begin), expected_1)
        self.assertEqual(self.analyzer.findBeginWindow(w2_begin), expected_2)
        self.assertEqual(self.analyzer.findBeginWindow(w3_begin), expected_3)
        self.assertEqual(self.analyzer.findBeginWindow(w4_begin), expected_4)

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
        logging.info(self.id())
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

def main():
    logging.basicConfig(filename="textcel.log", 
                        format='%(funcName)s:%(message)s', 
                        level=logging.DEBUG,
                        filemode='w')
    logging.info("starting logging")
    unittest.main()
    
if __name__ == '__main__':
    main()

