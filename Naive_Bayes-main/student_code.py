import math
import re


class Bayes_Classifier:

    def __init__(self):
        self.stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                           "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
                           'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
                           'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
                           'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                           'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
                           'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                           'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                           'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                           'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                           'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                           'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',
                           'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
                           "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
                           "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
                           "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't",
                           'wouldn', "wouldn't"]
        self.vocab_count = {"5": 0, "1": 0}
        # self.review_1 = []
        # self.review_5 = []
        self.count_word_1 = dict()
        self.count_word_5 = dict()
        self.complete_vocab = set()

    def remove_punct(self, word):
        return (re.sub(r'[^\w \s]', '', word))

    def beautify(self, document):
        for line in document:
            review = line.split('|')
            words = review[2].split()
            expanded_review = list(map(lambda x: x.strip().lower(), words))
            if review[0] == '1':
                self.vocab_count['1'] += 1
                # words = review[2].split()
                # y = list(map(lambda x: x.strip().lower(), words))
                for i in expanded_review:
                    if i not in self.stop_words:
                        unpunct_word = self.remove_punct(i)
                        # self.review_1.append(unpunct_word)
                        if i not in self.count_word_1:
                            self.count_word_1[unpunct_word] = 1
                        else:
                            self.count_word_1[unpunct_word] += 1
            elif review[0] == '5':
                self.vocab_count['5'] += 1
                # words = review[2].split()
                # z = list(map(lambda x: x.strip().lower(), words))
                for i in expanded_review:
                    if i not in self.stop_words:
                        unpunct_word = self.remove_punct(i)
                        # self.review_5.append(unpunct_word)
                        if i not in self.count_word_5:
                            self.count_word_5[unpunct_word] = 1
                        else:
                            self.count_word_5[unpunct_word] += 1
            self.complete_vocab = set(list(self.count_word_5.keys()) + list(self.count_word_1.keys()))
            # print(self.complete_vocab)
            # print(self.count_word_1)
            # print(self.count_word_5)
        print('vocab count is', self.vocab_count)

    def calc_probability(self, words):
        positive_class_probab = (self.vocab_count['5'] / (self.vocab_count['5'] + self.vocab_count['1']))
        negative_class_probab = (self.vocab_count['1'] / (self.vocab_count['5'] + self.vocab_count['1']))
        # positive_set = set(self.review_5)
        # negative_set = set(self.review_1)
        # complete_vocab = positive_set.union(negative_set)
        for word in words:
            if word in self.count_word_5:
                # occurrence = self.review_5.count(word)
                probab_word = (self.count_word_5[word] + 1) / (len(self.count_word_5) + len(self.complete_vocab))
                positive_class_probab *= probab_word
            if word in self.count_word_1:
                # occurrence = self.review_1.count(word)
                probab_word = (self.count_word_1[word] + 1) / (len(self.count_word_1) + len(self.complete_vocab))
                negative_class_probab *= probab_word
            else:
                positive_class_probab *= 1
                negative_class_probab *= 1
        return (positive_class_probab, negative_class_probab)

    def train(self, lines):
        self.beautify(lines)

    def classify(self, lines):

        prediction_class = []

        for line in lines:
            # print(line)
            review = line.split('|')
            words = review[2]
            unpunct_word = self.remove_punct(words)
            y = list(map(lambda x: x.strip().lower(), unpunct_word.split()))
            positive_probaility, negative_probability = self.calc_probability(y)
            if positive_probaility > negative_probability:
                prediction_class.append('5')
            else:
                prediction_class.append('1')
            # print(positive_probaility, negative_probability)

        # print(prediction_class)
        return (prediction_class)