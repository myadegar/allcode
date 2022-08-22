import os
import re
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from normalizer import Normalizer

normalizer = Normalizer(hold_link=False, hold_mention=False, hold_emoji=False,
                             hold_currency_symbols=False, remove_end_text_hashtag=False,
                             remove_english_marker=True, change_hashtag_to_text=True)

source_directory = 'F:\Tweets_train'
# source_directory = 'F:\persian_corpus\corpus'
window_size = 2

def extract_window_sentence(main_phrase, line_text, window_size):
    main_phrase_sticky = re.sub('[\s \ufffe \uffff \u200c \u200e _]', '', main_phrase)
    text = line_text.replace(main_phrase, main_phrase_sticky)
    tokens_list = text.split()
    len_tokens = len(tokens_list)
    index = [i for i, e in enumerate(tokens_list) if e == main_phrase_sticky]
    all_window_sentence = []
    for ind in index:
        window_sentence = []
        for i in range(ind - window_size, ind):
            if i >= 0:
                word = tokens_list[i]
                window_sentence.append(word)
        window_sentence.append(main_phrase)
        for i in range(ind + 1, ind + window_size + 1):
            if i <= len_tokens - 1:
                word = tokens_list[i]
                window_sentence.append(word)
        all_window_sentence.append(window_sentence)
    if len(all_window_sentence) != 0:
        final_window_sentence = max(all_window_sentence)
    else:
        final_window_sentence = []
    window_sentence = ' '.join(final_window_sentence)
    return window_sentence

def find_sentence(args) :
    main_phrase = args[0]
    path = args[1]
    selected_sentences = []
    with open(path, mode='r',encoding='utf-8') as f :
        for line_text in f :
            # line_text = normalizer.normalize(line_text)
            if ' '+ main_phrase + ' ' in line_text:
                window_sentence = extract_window_sentence(main_phrase, line_text, window_size)
                selected_sentences.append(window_sentence)
    return main_phrase, selected_sentences

def main():
    path = os.path.join('source', 'selected_phrase.txt')
    with open(path, mode='r', encoding='utf-8') as f:
        phrases = [phrase.rstrip('\n').strip() for phrase in f]
    all_sentences = {phrase:[] for phrase in phrases}

    file_list = os.listdir(source_directory)
    for file_name in tqdm(file_list):
        path = os.path.join(source_directory, file_name)
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            args = [(p, path) for p in phrases]
            output_generator = executor.map(find_sentence, args)

        for main_phrase, selected_sentences in tqdm(output_generator):
            all_sentences[main_phrase].extend(selected_sentences)

    for phrase, sentences in all_sentences.items():
        sentences = set(sentences)
        path = os.path.join('result', phrase+'.txt')
        with open(path, mode='w', encoding='utf-8') as f:
            for line in sentences:
                f.writelines(line+'\n')


if __name__ == '__main__':
    main()