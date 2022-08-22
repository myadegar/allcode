# Import required libraries
import os
import gensim
import numpy as np
from random import shuffle
from scipy.spatial.distance import cdist
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

source_directory= r'D:\TextMining\SemanticSearch\word2vector\result'

file_list = os.listdir(source_directory)
texts = []
text_count = {}

for file_name in file_list:
    path = os.path.join(source_directory, file_name)
    with open(path, mode='r', encoding='utf-8') as f:
        count = 0
        for line in f:
            count += 1
            texts.append(line.split())
    phrase = file_name.split('.')[0]
    text_count[phrase] = count

# shuffle(texts)

tagged_data = [TaggedDocument(doc, [i]) for i, doc in enumerate(texts)]

def main(do_train):
    if do_train:
        model = Doc2Vec(vector_size=100, window=2, min_count=2, workers=4, dm=0, dbow_words = 1, epochs=30)
        model.build_vocab(tagged_data)
        # train model
        model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
        # save
        model.save('my_doc2vec_model')

    model = Doc2Vec.load('my_doc2vec_model')
    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    test_data = "یکی بیاد کمکم این جزوه".split()
    new_vector = model.infer_vector(test_data)
    #print("V1_infer", new_vector)


    docvectors = model.docvecs.vectors_docs
    similarities = (1 - cdist(new_vector.reshape((1, new_vector.shape[0])), docvectors, metric='cosine')).reshape(-1)

    # phrase_similarity = {}
    # i = 0
    # for phrase, count in text_count.items():
    #     phrase_similarity[phrase] = np.mean(similarities[i:i+count])
    #     i = count
    #     print(phrase,phrase_similarity[phrase])



    similar_doc = model.docvecs.most_similar(positive=[new_vector],topn=10)
    # model.docvecs.similarity_unseen_docs()

    phrase_similarity = {phrase:[] for phrase,_ in text_count.items()}
    for id, sim in similar_doc:
        i = 0
        for phrase, count in text_count.items():
            if i <= id < i+count :
                phrase_similarity[phrase].append(sim)
            i = count
    phrase_similarity = {phrase: sum(sims) for phrase, sims in phrase_similarity.items()}
    print(phrase_similarity)




    for i in range(0,len(similar_doc)):
        print(tagged_data[int(similar_doc[i][0])],similar_doc[i][1])

if __name__ == "__main__":
    do_train = False
    main(do_train)




