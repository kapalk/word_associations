import os
import sys

from collections import Counter

from nltk.tokenize import word_tokenize

class Word_Associations_Evaluator:

    NOT_EXISTS = -1

    def __init__(self):
        
        self.article_folder = self._get_article_folder()

    def simple_evaluate(self, country, similar):
        
        if not similar:
            print('0')
            return 0

        article_name = self._get_wikitravel_article(country)

        if article_name is None:
            return Word_Associations_Evaluator.NOT_EXISTS

        with open(article_name, 'r') as fp:
            raw_article = fp.read()

        article = self._preproces_artice(raw_article)
        tokens = word_tokenize(article)

        bag_of_words = Counter(tokens)

        word_count = 0
        for word in similar:
            needle = word.lower().strip()
            word_count += 1 if needle in bag_of_words.keys() else 0 

        print(word_count / len(similar))
        return word_count / len(similar)
    
    def _preproces_artice(self, article):
        return article.lower()

    def _get_article_folder(self):
        path = os.path.join(os.path.dirname( __file__), '..', 'cleaned_data')
        return os.path.normpath(path)

    def _get_wikitravel_article(self, country):

        for fname in os.listdir(self.article_folder):
            country_name, _ = os.path.splitext(fname)
            if country_name.lower() == country.lower():
                return os.path.join(self.article_folder, fname)
        return None


def main():

    evaluator = Word_Associations_Evaluator()

    country = sys.argv[1]
    related = sys.argv[2:]

    evaluator.simple_evaluate(country, related)

if __name__ == '__main__':
    main()