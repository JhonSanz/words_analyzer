import re
import pandas as pd
import nltk
from unidecode import unidecode
from whatstk import WhatsAppChat
from nltk.tokenize import RegexpTokenizer
from ignored_words import IGNORED

nltk.download('stopwords')
from nltk.corpus import stopwords
sw_nltk = stopwords.words('spanish') + IGNORED
sw_nltk = list(map(lambda x: unidecode(x), sw_nltk))

IGNORED_REGEX = [
    r'^[jah]*$',  r'^[uy]*$',  r'^[je]*$',
    r'^[mm]*$',  r'^[uf]*$', r'^chimb[a]*$',
    r'^[oe]+$',  r'^a[g]+$',
]

class Solver:
    def __init__(self, df):
        self.df = df
        self.words_count = {}

    def ignored_regex(self, word):
        return any(map(
            lambda pattern: re.search(pattern, word),
            IGNORED_REGEX
        ))

    def check_word(self, word):
        if (
            len(word) < 2 or
            word in sw_nltk or
            not word.isalpha() or
            self.ignored_regex(word)
        ):
            return False
        return True

    def proccess_row(self, paragraph):
        tokenizer = RegexpTokenizer(r'\w+')
        paragraph = unidecode(paragraph.lower())
        paragraph = tokenizer.tokenize(paragraph)
        paragraph = [word for word in paragraph if self.check_word(word)]
        return paragraph

    def count_words(self, paragraph):
        for word in paragraph:
            try:
                self.words_count[word] += 1
            except KeyError:
                self.words_count[word] = 1
    
    def run(self):
        for (message,) in zip(self.df["message"]):
            paragraph = self.proccess_row(message)
            self.count_words(paragraph)
        return self.words_count
    
df = WhatsAppChat.from_source(filepath="chat.txt").df

result = Solver(df).run()

count = pd.DataFrame.from_dict(result, orient='index', columns=['count']).reset_index()
count.columns = ['word', 'count']
count = count.sort_values('word').reset_index(drop=True)
count.to_csv("result.csv")
