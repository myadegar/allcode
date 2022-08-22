# -*- coding:utf-8 -*-

import logging
from gensim.models.word2vec import Word2Vec, PathLineSentences
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.models import FastText
from normalizer import Normalizer
from  time import time


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
normalizer = Normalizer(hold_link=False, hold_mention=False, hold_emoji=False,
                             hold_currency_symbols=False, remove_end_text_hashtag=False,
                             remove_english_marker=True, change_hashtag_to_text=True)


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


def main(do_train, dataset_directory, update_directory):
    top_n = 50
    dimension_size = 300
    window = 7 #10
    min_count = 10 #3
    threshold_bigram = 1 #3
    threshold_trigram = 1 #3
    epoch = 30 #30
    if do_train:
        t0 = time()
        sentences= PathLineSentences(dataset_directory)

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
        model_cbow.save(r"model/cbow_model.mod")
        t1 = time()
        print(f'Train time : {t1-t0}')
        ###############
        # model_skip_gram = Word2Vec(size=dimension_size, window=window, min_count=min_count, #alpha=0.3, min_alpha=0.0007,
        #                  worker5fgis=7, sg=1, #iter=100, #sample=6e-5, negative=20,
        #                       )
        # model_skip_gram.build_vocab(sentences=sentences, progress_per=10000)
        # model_skip_gram.train(sentences, total_examples=model_skip_gram.corpus_count, epochs=epoch, report_delay=1)
        # model_skip_gram.init_sims(replace=True)
        # model_skip_gram.save("model/skip_gram_w2v.mod")

        ###############
        # model_fast_text = FastText(size=dimension_size, window=window, min_count=min_count, #alpha=0.3, min_alpha=0.0007,
        #                  workers=7, sg=0, #iter=100, #sample=6e-5, negative=20,
        #                      )
        # model_fast_text.build_vocab(sentences=sentences, progress_per=10000)
        # model_fast_text.train(sentences, total_examples=model_fast_text.corpus_count, epochs=epoch, report_delay=1)
        # model_fast_text.init_sims(replace=True)
        # model_fast_text.save("model/fast_text_w2v.mod")

    if do_update:
        min_count = 5
        sentences = PathLineSentences(update_directory)

        phrases = Phrases(sentences=sentences, min_count=min_count, threshold=threshold_bigram)
        bigram = Phraser(phrases)
        sentences = bigram[sentences]

        phrases = Phrases(sentences=sentences, min_count=min_count, threshold=threshold_trigram)
        trigram = Phraser(phrases)
        sentences = trigram[sentences]

        model_cbow = Word2Vec.load("model/cbow_w2v.mod")
        model_cbow.build_vocab(sentences=sentences, update=True)
        check_vocab(model_cbow)
        model_cbow.train(sentences, total_examples=model_cbow.corpus_count, epochs=epoch, report_delay=1)
        model_cbow.init_sims(replace=True)
        model_cbow.save("model/update_cbow_w2v.mod")



    model_cbow = Word2Vec.load("model/cbow_model.mod")
    # model_skip_gram = Word2Vec.load("model/skip_gram_w2v.mod")
    # model_fast_text = Word2Vec.load("model/fast_text_w2v.mod")

    # positive_query = ['سلیمانی', 'سوریه']
    # negative_query = ['قتل']
    positive_query = ['نماینده چابهار']
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
    sim_cbow = [(word.replace('_', ' '), degree) for word, degree in sim_cbow]

    # sim_skip_gram = model_skip_gram.wv.most_similar(positive=positive_query, negative=negative_query, topn=top_n)
    # sim_skip_gram = [(word.replace('_', ' '), degree) for word, degree in sim_skip_gram]
    #
    # sim_fast_text = model_fast_text.wv.most_similar(positive=positive_query, negative=negative_query, topn=top_n)
    # sim_fast_text = [(word.replace('_', ' '), degree) for word, degree in sim_fast_text]


    print('\n')
    print('cbow: ')
    for s in sim_cbow:
        print(s)
    print('\n')

    # print('skip_gram: ')
    # for s in sim_skip_gram:
    #     print(s)
    # print('\n')
    #
    # print('fast_text: ')
    # for s in sim_fast_text:
    #     print(s)

if __name__ == "__main__":
    do_train = True
    do_update = False
    # dataset_directory = r"F:\Tweets_train"
    # dataset_directory = r"F:\Tweets_split_clean"
    # dataset_directory = r"F:\persian_corpus\twitter_paragraph_corpus"
    dataset_directory = r"F:\persian_corpus\Tweets_cluster\17000000"
    update_directory = r"F:\Tweets_split_clean"
    main(do_train, dataset_directory, update_directory)