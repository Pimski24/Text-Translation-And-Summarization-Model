import os
from nltk import tokenize, word_tokenize
from nltk.corpus import stopwords

class Summarizer:
    """
    A class used to summarize texts.

    This class can summarize texts from strings, list of string or a file.
    It can use language specific stop word lists containg words to ignore during the 
    determination of the most important subjects of the text. The language and stop word lists
    can be set seperately or can be detected automatically from a text.

    Attributes
    ----------
    stop_words : set
        a set of stopwords. These are ignored when searching for the most used
        words in the text
    language : str
        the current selected language. The stop words set is language specific
    summary_length : int
        the default number of sentences to use for the summary.
    balance_length : bool
        determines if the sentence weight is weighted based on sentence length

    """
    
    stop_words:set = {}
    language:str = None
    summary_length:int = 0
    balance_length:bool = False
    
    def __init__(self, language:str='dutch', summary_length:int=3, balance_length=False):
        """
        :param str language: The language to use, defaults to 'dutch'
        :param int summary_length: The default length for the summary to generate, defaults to 3
        :param bool balance_length: Balance sentences on lebgth, default to False
        """
        self.set_language(language)
        self.set_summary_length(summary_length)
        self.set_balance_length(balance_length)
    
    def set_language(self, lang:str) -> None:
        """
        Sets the language to use and set the stop words to the default
        list provided by NLTK corpus for this language
        :param str lang: The language to use
        """
        try:
            self.stop_words = set(stopwords.words(lang))
            self.language = lang
        except:
            self.stop_words = {}
            self.language = None
        
    def set_stop_words(self, stop_words:set) -> None:
        """
        Sets the stop words to the provided list.
        :param set stop_words: The stop words to use
        """
        if stop_words:
            self.stop_words = set(stop_words)
        else:
            self.stop_words = {}
        
    def read_stopwords_from_file(self, language:str, filename:str) -> None:
        """
        Read the stop words from the specified file and set the language to
        the given language name
        :param strlanguage: The name of the language to set
        :param str filename: The name of the file containing the stop words
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                 text = " ".join(f.readlines())
            self.stop_words = set(text.split())  # prevent duplicate entries
            self.language = language
        except:
            self.stop_words = {}
            self.language = None
            
    def set_summary_length(self, summary_length:int) -> None:
        """
        Sets the default length for the summaries to be created
        :param int summary_length: The new default length
        """
        self.summary_length = summary_length

    def set_balance_length(self, balance_length:bool) -> None:
        """
        Sets the swith if the sentence weights need to weighted on
        sentence length. This might improve performance if the text
        contains a variety of short and long sentences.
        :param bool balance_length: new vale
        """
        self.balance_length = balance_length