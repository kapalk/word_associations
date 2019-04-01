from collections import Counter
import nltk
import os
import pickle
import string
import sys

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

class WikimediaEvaluator:

    NOT_EXISTS = -1

    def __init__(self):
        
        self.article_folder = self._get_article_folder()
        self.cache = os.path.join(self.article_folder, '.cache')
        self.lemmatizer = nltk.WordNetLemmatizer()
        
    def simple_wikitravel_evaluate(self, country, similar, cached=True):
        return self.simple_evaluate(country, similar, src='wikitravel', cached=cached)
    
    def simple_wikipedia_evaluate(self, country, similar, cached=True):
        return self.simple_evaluate(country, similar, src='wikipedia', cached=cached)
    
    def simple_evaluate(self, country, similar, src='wikitravel', cached=True):
        
        if not similar:
            return 0

        bag_of_words = self._get_bag_of_words_model(country, src, cached=cached)

        word_count = 0
        for word in similar:
            needle = word.lower().strip()
            word_count += 1 if needle in bag_of_words else 0 
     
        return word_count / len(similar)
    
    def get_article_keywords(self, country, src='wikitravel', cached=True):

        cached_file = os.path.join(self.cache, 'tfdf', src, country.capitalize() + '.pkl')
        if cached and os.path.exists(cached_file):
            print('Return cached')
            with open(cached_file , 'rb') as cfp:
                return pickle.load(cfp)

        article_name = self._get_wiki_article(country, src)

        if article_name is None:
            return WikimediaEvaluator.NOT_EXISTS

        with open(article_name, 'r') as fp:
            raw_article = fp.read()

        article = self._preproces_artice(raw_article)

        token_dict = {}

        def tokenize(text):
            tokens = word_tokenize(text)
            return [self.lemmatizer.lemmatize(token) for token in tokens]

        for dirpath, dirs, files in os.walk(os.path.join(self.article_folder, src)):
            for f in files[:2]:
                fname = os.path.join(dirpath, f)
                with open(fname) as pearl:
                    text = pearl.read()
                    token_dict[f] = text
        vectorizer = TfidfVectorizer(smooth_idf=True,use_idf=True)
        vectorizer.fit(token_dict.values())

        keywords = vectorizer.transform([article])
        print(keywords)

        # feature_names = tfidf.get_feature_names()
        # for col in response.nonzero()[1]:
        #     print feature_names[col], ' - ', response[0, col]


        dirname, _ = os.path.split(cached_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(cached_file, 'wb') as cfp:
            pickle.dump(keywords, cfp)

        return keywords
        

    def _get_bag_of_words_model(self, country, src='wikitravel', cached=True):
        
        cached_file = os.path.join(self.cache, 'bof', src, country.capitalize() + '.pkl')
        if cached and os.path.exists(cached_file):
            print('Return cached')
            with open(cached_file , 'rb') as cfp:
                return pickle.load(cfp)
        
        article_name = self._get_wiki_article(country, src)

        if article_name is None:
            return WikimediaEvaluator.NOT_EXISTS

        with open(article_name, 'r') as fp:
            raw_article = fp.read()

        article = self._preproces_artice(raw_article)
        tokens = word_tokenize(article)
        filtered_tokens = self._filter_stopwords(tokens)
        
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
        bag_of_words = Counter(lemmatized_tokens)

        dirname, _ = os.path.split(cached_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(cached_file, 'wb') as cfp:
            pickle.dump(bag_of_words, cfp)

        return bag_of_words

    def _preproces_artice(self, article):
        return article.lower()

    def _filter_stopwords(self, tokens):

        remove = stopwords.words('english') + list(string.punctuation)
        ftokens = [token for token in tokens if token not in remove]
        return ftokens

    def _get_article_folder(self):
        path = os.path.join(os.path.dirname( __file__), '..', 'cleaned_data')
        return os.path.normpath(path)

    def _get_wiki_article(self, country, src):
        path = os.path.join(self.article_folder, src, country.capitalize() + '.txt')
        return path if os.path.exists(path) else None


def main():

    evaluator = WikimediaEvaluator()

    country = sys.argv[1]
    
    # wikitravel_model = evaluator._get_bag_of_words_model(country, src='wikitravel')
    # wikipedia_model = evaluator._get_bag_of_words_model(country, src='wikipedia')
    
    # print('wikitravel')
    # print(wikitravel_model.most_common(20))
    # print('wikipedia')
    # print(wikipedia_model.most_common(20))

    evaluator.get_article_keywords(country, 'wikitravel', cached=False)

if __name__ == '__main__':
    main()