# -*- coding:utf-8 -*-

import logging
from gensim.models.word2vec import Word2Vec
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.utils import to_unicode
import itertools
import json
from normalizer import Normalizer
from time import time


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
normalizer = Normalizer(hold_link=False, hold_mention=False, hold_emoji=False,
                             hold_currency_symbols=False, remove_end_text_hashtag=False,
                             remove_english_marker=True, change_hashtag_to_text=False)

MAX_WORDS_IN_BATCH = 10000
class LineSentences(object):
    """Iterate over a list that contains sentences: one line = one sentence.
    Words must be already preprocessed and separated by whitespace.
    """
    def __init__(self, source, max_sentence_length=MAX_WORDS_IN_BATCH, limit=None):

        self.source = source
        self.max_sentence_length = max_sentence_length
        self.limit = limit

    def __iter__(self):
        """Iterate through the lines in the source."""
        for line in itertools.islice(self.source, self.limit):
            line = to_unicode(line).split()
            i = 0
            while i < len(line):
                yield line[i: i + self.max_sentence_length]
                i += self.max_sentence_length


def check_vocab(model):
    vocab = model.wv.vocab
    onegram = []
    bigram = []
    trigram = []
    for word in vocab.keys():
        if word.count('_') == 0:
            onegram.append(word)
        elif word.count('_') == 1:
            bigram.append(word)
        elif word.count('_') >= 2:
            trigram.append(word)

    with open('onegram.txt', mode='w', encoding='utf-8') as f:
        for word in onegram:
            f.writelines(word + '\n')

    with open('bigram.txt', mode='w', encoding='utf-8') as f:
        for word in bigram:
            f.writelines(word + '\n')

    with open('trigram.txt', mode='w', encoding='utf-8') as f:
        for word in trigram:
            f.writelines(word + '\n')


def main(file_name):
    dimension_size = 300
    window = 7
    min_count = 3
    threshold_bigram = 2 #3
    threshold_trigram = 2 #3
    epoch = 30
    ##
    # with open(file_name, mode='r', encoding='utf-8') as f:
    #     texts = json.load(f)
    # texts = [text.get('Text_Status') for text in texts]

    texts = []
    with open(file_name, mode='r', encoding='utf-8') as f:
        for line in f:
            text = line.split('\t')[2]
            texts.append(text)


    texts = {normalizer.normalize(text) for text in texts}
    texts = {text.replace('s0x23 ', '#') for text in texts}


    t0 = time()
    sentences = LineSentences(texts)

    phrases = Phrases(sentences=sentences, min_count=min_count, threshold=threshold_bigram)
    bigram = Phraser(phrases)
    sentences = bigram[sentences]

    phrases = Phrases(sentences=sentences, min_count=min_count, threshold=threshold_trigram)
    trigram = Phraser(phrases)
    sentences = trigram[sentences]

    ###############
    model_cbow = Word2Vec(size=dimension_size, window=window, min_count=min_count, #alpha=0.3, min_alpha=0.0007,
                     workers=7, sg=0, #iter=100, #sample=6e-5, negative=20,
                          )
    model_cbow.build_vocab(sentences=sentences, progress_per=10000)
    check_vocab(model_cbow)
    model_cbow.train(sentences, total_examples=model_cbow.corpus_count, epochs=epoch, report_delay=1)
    model_cbow.init_sims(replace=True)
    model_cbow.save("model/semantic_model.mod")
    t1 = time()
    print(f'Train time : {t1-t0}')
    ###############
    model_cbow = Word2Vec.load("model/semantic_model.mod")
    top_n = 200
    positive_query = ['جورج فلوید']
    negative_query = ['']

    positive_query = [normalizer.normalize(query).replace(' ', '_').replace('s0x23_', '#') for query in positive_query]
    negative_query = [normalizer.normalize(query).replace(' ', '_').replace('s0x23_', '#') for query in negative_query]
    all_query = positive_query + negative_query

    if positive_query[0] == '':
        positive_query = None
    if negative_query[0] == '':
        negative_query = None

    vocab = model_cbow.wv.vocab
    for word in all_query:
        if word not in vocab.keys() and word != '':
            raise Exception(f'{word} not in vaocabulary')


    sim_cbow = model_cbow.wv.most_similar(positive=positive_query, negative=negative_query, topn=top_n)
    phrase_similarity = []
    for phrase, degree in sim_cbow:
        if '#' in phrase:
            sub_phrase = phrase.split('#')
            sub_phrase[0] = sub_phrase[0].replace('_', ' ')
            new_sub_phrase  = sub_phrase[:1] + ['#'] + sub_phrase[1:]
            phrase = ''.join(new_sub_phrase)
        else:
            phrase = phrase.replace('_', ' ')
        phrase_similarity.append((phrase, degree))

    print('\n')
    for s in phrase_similarity:
        print(s)
    print('\n')


if __name__ == "__main__":
    file_name = r'source/BulkFile.json'
    file_name = r'source/2020-06-15.tsv'
    main(file_name)