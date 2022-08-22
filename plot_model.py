import numpy as np
import matplotlib.pyplot as plt


import seaborn as sns
import pandas as pd
from gensim import matutils
from numpy import array
from numpy import float32 as REAL

sns.set_style("darkgrid")

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from gensim.models.word2vec import Word2Vec
import arabic_reshaper
from bidi.algorithm import get_display



def tsnescatterplot(model, word, list_names, dimension=200):
    """ Plot in seaborn the results from the t-SNE dimensionality reduction algorithm of the vectors of a query word,
    its list of most similar words, and a list of words.
    """
    arrays = np.empty((0, dimension), dtype='f')

    query_word = word[0]
    for wrd in word[1:]:
        query_word += '+' + wrd
    query_word = query_word.replace('_', ' ')

    word_labels = [get_display(arabic_reshaper.reshape(query_word))]


    color_list = ['red']

    # adds the vector of the query word
    query_vector = []
    for wrd in word:
        vector = model.wv.__getitem__([wrd])
        vector = vector / np.linalg.norm(vector)
        query_vector.append(vector)

    query_vector = matutils.unitvec(array(query_vector).mean(axis=0)).astype(REAL)



    arrays = np.append(arrays, query_vector, axis=0)

    # arrays = np.append(arrays, model.wv.__getitem__(word), axis=0)

    # gets list of most similar words
    close_words = model.wv.most_similar(word)

    # adds the vector for each of the closest words to the array
    for wrd_score in close_words:
        wrd_vector = model.wv.__getitem__([wrd_score[0]])
        word_labels.append(get_display(arabic_reshaper.reshape(wrd_score[0])))
        color_list.append('blue')
        arrays = np.append(arrays, wrd_vector, axis=0)

    # adds the vector for each of the words from list_names to the array
    for wrd in list_names:
        wrd_vector = model.wv.__getitem__([wrd])
        word_labels.append(get_display(arabic_reshaper.reshape(wrd)))
        color_list.append('green')
        arrays = np.append(arrays, wrd_vector, axis=0)

    # Reduces the dimensionality from 300 to 50 dimensions with PCA
    reduc = PCA(n_components=20).fit_transform(arrays)

    # Finds t-SNE coordinates for 2 dimensions
    np.set_printoptions(suppress=True)

    Y = TSNE(n_components=2, random_state=0, perplexity=15).fit_transform(reduc)

    # Sets everything up to plot
    df = pd.DataFrame({'x': [x for x in Y[:, 0]],
                       'y': [y for y in Y[:, 1]],
                       'words': word_labels,
                       'color': color_list})

    fig, _ = plt.subplots()
    fig.set_size_inches(9, 9)

    # Basic plot
    p1 = sns.regplot(data=df,
                     x="x",
                     y="y",
                     fit_reg=False,
                     marker="o",
                     scatter_kws={'s': 40,
                                  'facecolors': df['color']
                                  }
                     )

    # Adds annotations one by one with a loop
    for line in range(0, df.shape[0]):
        p1.text(df["x"][line],
                df['y'][line],
                '  ' + df["words"][line].title(),
                horizontalalignment='left',
                verticalalignment='bottom', size='medium',
                color=df['color'][line],
                weight='normal'
                ).set_size(15)

    plt.xlim(Y[:, 0].min() - 50, Y[:, 0].max() + 50)
    plt.ylim(Y[:, 1].min() - 50, Y[:, 1].max() + 50)

    word_title = get_display(arabic_reshaper.reshape(query_word))
    plt.title('t-SNE visualization for {}'.format(word_title.title()))
    plt.show()


model_path = "model/cbow_w2v.mod"
model_loaded = Word2Vec.load(model_path)
query_word = ['کشتار','آبان']
list_names = [t[0] for t in model_loaded.wv.most_similar(positive=[query_word[0]], topn=20)][10:]
dimension=300

tsnescatterplot(model_loaded, query_word, list_names, dimension)