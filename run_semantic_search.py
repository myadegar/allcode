from gensim.models.word2vec import Word2Vec
from normalizer import Normalizer
import streamlit as st
import pandas as pd
import numpy as np
import re
from collections import OrderedDict
from gensim import matutils
from numpy import array
from numpy import float32 as REAL
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
import openpyxl
import base64
from io import BytesIO

#################################################
def load_normalizer():
    normalizer = Normalizer(hold_link=False, hold_mention=False, hold_emoji=False,
                                 hold_currency_symbols=False, remove_end_text_hashtag=False,
                                 remove_english_marker=True, change_hashtag_to_text=True)
    return normalizer


@st.cache(hash_funcs={Word2Vec: id})
def load_model():
    model_path = r"D:\TextMining\SemanticSearch\word2vector\model\cbow_model.mod"
    model = Word2Vec.load(model_path)
    return model

def tsnescatterplot(model, positive_query, negative_query, list_semantics, dimension=200, max_display_words=30):
    """ Plot in seaborn the results from the t-SNE dimensionality reduction algorithm of the vectors of a query word,
    its list of most similar words, and a list of words.
    """

    arrays = np.empty((0, dimension), dtype='f')

    query_word = make_query_name(positive_query, negative_query)

    word_labels = [get_display(arabic_reshaper.reshape(query_word))]
    color_list = ['green']

    # adds the vector of the query word
    query_vector = []
    for wrd in positive_query:
        vector = model.wv.__getitem__([wrd])
        vector = vector / np.linalg.norm(vector)
        query_vector.append(vector)
    for wrd in negative_query:
        vector = model.wv.__getitem__([wrd])
        vector = vector / np.linalg.norm(vector)
        query_vector.append(-vector)

    query_vector = matutils.unitvec(array(query_vector).mean(axis=0)).astype(REAL)

    arrays = np.append(arrays, query_vector, axis=0)
    # arrays = np.append(arrays, model.wv.__getitem__([positive_query[0]]), axis=0)

    # adds the vector for each of the words from list_semantics to the array
    for wrd in list_semantics[:max_display_words+1]:
        wrd_vector = model.wv.__getitem__([wrd])
        wrd = wrd.replace('_', ' ')
        word_labels.append(get_display(arabic_reshaper.reshape(wrd)))
        color_list.append('blue')
        arrays = np.append(arrays, wrd_vector, axis=0)

    # Reduces the dimensionality from 300 to 50 dimensions with PCA
    n_reduced = min(20, max_display_words)
    reduc = PCA(n_components=n_reduced).fit_transform(arrays)

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

    plt.title('Visualization for {}'.format(get_display(arabic_reshaper.reshape(query_word.title()))))
    st.pyplot(plt)


def make_query_name(positive_query, negative_query):
    query_word = positive_query[0]
    for wrd in positive_query[1:]:
        query_word += '+' + wrd
    for wrd in negative_query:
        query_word += '-' + wrd
    query_word = query_word.replace('_', ' ')
    return query_word

def get_table_download_link(df, query_word):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    buf = BytesIO()
    df.to_excel(buf, index=False)
    b64 = base64.b64encode(buf.getvalue()).decode()  # some strings <-> bytes conversions necessary here
    name = query_word + '.xlsx'
    href = f'<a href="data:file/excel;base64,{b64}" download="{name}">Download Excel file</a>'

    # for cdv format
    # csv = df.to_csv(index=False)
    # b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a> (right-click and save as &lt;some_name&gt;.csv)'

    return href

def main():
    st.title("Semantic Search Demo")
    st.write("")
    positive_query = st.text_input("Positive Query:")
    positive_query = re.split(",|،", positive_query)

    negative_query = st.text_input("Negative Query:")
    negative_query = re.split(",|،", negative_query)


    count = st.slider("Result max count:", min_value=1, max_value=200, value=50)

    if st.button("Search!"):
        normalizer = load_normalizer()
        model = load_model()

        positive_query = [normalizer.normalize(query).replace(' ', '_').replace('s0x23_', '#') for query in positive_query]
        negative_query = [normalizer.normalize(query).replace(' ', '_').replace('s0x23_', '#') for query in negative_query]
        all_query = positive_query + negative_query

        if positive_query[0] == '':
            positive_query = None
        if negative_query[0] == '':
            negative_query = None

        vocab = model.wv.vocab
        for word in all_query:
            if word not in vocab.keys() and word != '':
                st.error(f'{word} not in vaocabulary')

        # sim = model.wv.most_similar(positive=positive_query, negative=negative_query, topn=count)
        # list_semantics = [t[0] for t in sim]
        # sim = [(word.replace('_', ' '), degree) for word, degree in sim]

        sim_cbow = model.wv.most_similar(positive=positive_query, negative=negative_query, topn=count)
        list_semantics = [t[0] for t in sim_cbow]
        sim = []
        for phrase, degree in sim_cbow:
            if '#' in phrase:
                sub_phrase = phrase.split('#')
                sub_phrase[0] = sub_phrase[0].replace('_', ' ')
                new_sub_phrase = sub_phrase[:1] + ['#'] + sub_phrase[1:]
                phrase = ''.join(new_sub_phrase)
            else:
                phrase = phrase.replace('_', ' ')
            sim.append((phrase, round(degree, 3)))


        df = pd.DataFrame(sim, columns=["Semantics", "Similarity"])
        df.index += 1
        st.table(df)

        if positive_query is None:
            positive_query = []
        if negative_query is None:
            negative_query = []

        query_word = make_query_name(positive_query, negative_query)
        df.to_excel(query_word + '.xlsx', encoding='utf-8')

        st.markdown(get_table_download_link(df, query_word), unsafe_allow_html=True)

        dimension = 300
        max_display_words = count
        tsnescatterplot(model, positive_query, negative_query, list_semantics, dimension, max_display_words)


if __name__ == "__main__":
    main()
    # streamlit run run_semantic_search.py --server.port 8501