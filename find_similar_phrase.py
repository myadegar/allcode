from normalizer import Normalizer
from gensim.models.word2vec import Word2Vec
import numpy as np
from numpy.linalg import norm
import os
import re
import time

normalizer = Normalizer(hold_link=False, hold_mention=False, hold_emoji=False,
                             hold_currency_symbols=False, remove_end_text_hashtag=False,
                             remove_english_marker=True, change_hashtag_to_text=True)

model_cbow = Word2Vec.load("model/cbow_w2v.mod")
vocab = model_cbow.wv.vocab
vector_size = model_cbow.vector_size

#########################################################

window_size = 2
window_len = 2 * window_size
primary_weights = [2,7,7,2]
topn = 10
n_selected_phrase = 5000

main_phrase = 'بیس'
main_sentence = 'مامان من دارم با دوستم میرم بیس بال بازی کنم'

#ToDO delete all marker after normalizer
#ToDO kasre ezafe FOR ALL
#ToDO same degree
#ToDO ignore number 2

main_sentence = normalizer.normalize(main_sentence)
tokens_list = main_sentence.split()
len_tokens = len(tokens_list)
index = [i for i, e in enumerate(tokens_list) if e == main_phrase]
main_index = index[0]

window_index = []
for i in range(main_index - window_size, main_index):
    if i >= 0:
        window_index.append(i)
    else:
        window_index.append(-1)
for i in range(main_index + 1, main_index + window_size + 1):
    if i <= len_tokens - 1:
        window_index.append(i)
    else:
        window_index.append(-1)

weights = [0] * len(window_index)
for i, ind in enumerate(window_index):
    if ind != -1:
        weights[i] = primary_weights[i]
weights = [w / sum(weights) for w in weights]

main_sentence_vector = []
position_index_in_window = []
for i, index in enumerate(window_index):
    word = tokens_list[index]
    if (index != -1) and word in vocab:
        vector = model_cbow.wv.word_vec(word)
        main_sentence_vector.append(vector)
        position_index_in_window.append(i)

#########################################################
def extract_window_sentence(main_phrase, line_text, window_size):
    main_phrase_sticky = re.sub('[\s \ufffe \uffff \u200c \u200e _]', '', main_phrase)
    text = line_text.replace(main_phrase, main_phrase_sticky)
    tokens_list = text.split()
    len_tokens = len(tokens_list)
    index = [i for i, e in enumerate(tokens_list) if e == main_phrase_sticky]
    if len(index) == 0:
        return ['']*(2*window_size)
    ind = index[0]

    window_sentence = []
    for i in range(ind - window_size, ind):
        if i >= 0:
            word = tokens_list[i]
            window_sentence.append(word)
        else:
            window_sentence.append('')
    for i in range(ind + 1, ind + window_size + 1):
        if i <= len_tokens - 1:
            word = tokens_list[i]
            window_sentence.append(word)
        else:
            window_sentence.append('')

    return window_sentence

###############
source_directory= r'F:\persian_corpus\multimeaning_phrase'

file_list = os.listdir(source_directory)
all_texts = {}
text_count = {}
for file_name in file_list:
    path = os.path.join(source_directory, file_name)
    phrase = file_name.split('.')[0]
    with open(path, mode='r', encoding='utf-8') as f:
        texts = [line.rstrip('\n') for line in f]
    all_texts[phrase] = texts[:n_selected_phrase]

########## for initial load
all_texts_vector = {}
for phrase, texts in all_texts.items():
    vector_matrix = np.zeros((len(texts),window_len,vector_size), dtype='float32')
    for i, text in enumerate(texts):
        window_sentence = extract_window_sentence(phrase, text, window_size)
        for j, word in enumerate(window_sentence):
            if word != '' and word in vocab:
                vector = model_cbow.wv.word_vec(word)
                vector_matrix[i,j] = vector
    all_texts_vector[phrase] = vector_matrix

#########################################################
# for process, sim calc
t0 = time.time()
sum_sim_value = -1
for phrase, vector_matrix in all_texts_vector.items():
    samples_similarity = np.zeros(vector_matrix.shape[0], dtype='float32')
    for i, ind in enumerate(position_index_in_window):
        samples_vector = vector_matrix[:,ind]
        main_vector = main_sentence_vector[i]
        sim = np.dot(samples_vector, main_vector) * weights[ind]
        samples_similarity += sim
    top_n_idx = np.argsort(samples_similarity)[-topn:][::-1]
    top_n_sum_values = sum([samples_similarity[i] for i in top_n_idx])
    if top_n_sum_values > sum_sim_value:
        selected_phrase = phrase
        sum_sim_value = top_n_sum_values

    top_n_values = [samples_similarity[i] for i in top_n_idx]
    for idx, sim in zip(top_n_idx, top_n_values):
        print(phrase, sim, all_texts[phrase][idx])
    print(phrase, sum(top_n_values))
    print('*'*20)


print(selected_phrase)


    # for idx, sim in zip(top_n_idx, top_n_values):
    #     print(phrase, sim, all_texts[phrase][idx])
    # print(phrase, sum(top_n_values))
    # print('*'*20)

print(f'time: {time.time()-t0}')