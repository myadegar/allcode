import os
import re
from tqdm import tqdm
from itertools import islice
from concurrent.futures import ProcessPoolExecutor
from normalizer import Normalizer

normalizer = Normalizer(hold_link=False, hold_mention=False, hold_emoji=False,
                             hold_currency_symbols=False, remove_end_text_hashtag=False,
                             remove_english_marker=True, change_hashtag_to_text=True)

##########################################
# source_directory = 'F:\Tweets_train'
source_directory = 'F:\persian_corpus\corpus'
destination_directory = 'F:\persian_corpus\multimeaning_phrase'
window_size = 2
n_split_phrase = 200
n_maximum_phrase = 20000

##########################################
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


def find_sentence(args):
    all_phrase = args[0]
    path = args[1]
    file_number = args[2]
    print(f'File number : {file_number}')
    with open(path, mode='r', encoding='utf-8') as f:
        texts = [line_text for line_text in f]
    all_selected_sentences = {}
    for main_phrase, other_form_phrases in all_phrase.items():
        selected_sentences = {}
        for phrase in other_form_phrases:
            window_sentence_dict = {}
            for line_text in texts:
                if (' ' + phrase + ' ') in line_text:
                    window_sentence = extract_window_sentence(phrase, line_text, window_size)
                    if window_sentence in window_sentence_dict.keys():
                        window_sentence_dict[window_sentence] += 1
                    else:
                        window_sentence_dict[window_sentence] = 1
            selected_sentences[phrase] = window_sentence_dict
        all_selected_sentences[main_phrase] = selected_sentences

    print(f'Processed: {path}')
    return all_selected_sentences

def main():
    path = os.path.join('source', 'convertable_multiple_formal_and_correct_form_words.txt')
    all_phrase = {}
    with open(path, mode='r', encoding='utf-8') as f:
        for line in f:
            phrases = [phrase.rstrip('\n').strip() for phrase in line.split('\t')]
            all_phrase[phrases[0]] = phrases[1:]
    it = iter(all_phrase)
    chunks = iter(lambda: tuple(islice(it, n_split_phrase)), ())
    ###
    file_list = os.listdir(source_directory)
    n_files = len(file_list)
    path_list = [os.path.join(source_directory, file_name) for file_name in file_list]
    ###
    for chunk in chunks:
        all_phrase_splitted = {}
        for phr in chunk:
            all_phrase_splitted[phr] = all_phrase[phr]

        with ProcessPoolExecutor(max_workers=os.cpu_count()-1) as executor:
            args = [(all_phrase_splitted, path, file_number) for path, file_number in zip(path_list, range(1, n_files+1))]
            output_generator = executor.map(find_sentence, args)
        ###
        aggregated_all_sentences = {}
        for main_phrase, other_forms_phrase in all_phrase_splitted.items():
            aggregated_all_sentences[main_phrase] = {phrase:{} for phrase in other_forms_phrase}
        for all_selected_sentences in tqdm(output_generator):
            for main_phrase, other_form_window_sentence_dict in all_selected_sentences.items():
                for phrase, window_sentence_dict in other_form_window_sentence_dict.items():
                    for window_sentence, count in window_sentence_dict.items():
                        if window_sentence in aggregated_all_sentences[main_phrase][phrase].keys():
                            aggregated_all_sentences[main_phrase][phrase][window_sentence] += count
                        else:
                            aggregated_all_sentences[main_phrase][phrase][window_sentence] = count

        ###
        for main_phrase, other_forms_phrase_dict in tqdm(aggregated_all_sentences.items()):
            for phrase, window_sentence_dict in other_forms_phrase_dict.items():
                sorted_window_sentence = sorted(window_sentence_dict.items(), key=lambda x:x[1], reverse=True)
                dir = os.path.join(destination_directory, main_phrase)
                os.makedirs(dir, exist_ok=True)
                path = os.path.join(dir, phrase+'.txt')
                with open(path, mode='w', encoding='utf-8') as f:
                    for line_text, _ in sorted_window_sentence[:n_maximum_phrase]:
                        f.writelines(line_text+'\n')


if __name__ == '__main__':
    main()