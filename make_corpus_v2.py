import os
from tqdm import tqdm
from normalizer import Normalizer
from lang_detection import load,detect

sess = load()
normalizer = Normalizer(hold_link=False, hold_mention=False, hold_emoji=False,
                 hold_currency_symbols=False, remove_end_text_hashtag=False,
                 remove_english_marker=True, change_hashtag_to_text=True)

###############################
source_directory = 'dataset'
result_directory = 'clean_texts'
source_file_names = os.listdir(source_directory)
batch_size = 10000

########################################
for source_file_name in source_file_names:
    print('started : {}'.format(source_file_name))
    text_list = []
    with open(os.path.join(source_directory, source_file_name), mode='r',encoding='utf-8',errors='ignore') as text_file:
        for line_text in text_file:
            text_list.append(line_text.rstrip('\n'))
    batch_counter = 0
    split_text_list = []
    language_list = []
    for text in tqdm(text_list):
        batch_counter += 1
        split_text_list.append(text)
        if (batch_counter % batch_size) == 0:
            split_language_list = detect(sess, split_text_list)
            for lang in split_language_list:
                language_list.append(lang)
                split_text_list = []
    if (batch_counter % batch_size) != 0:
        split_language_list = detect(sess, split_text_list)
        for lang in split_language_list:
            language_list.append(lang)
    clean_texts = {normalizer.normalize(text) for i,text in enumerate(text_list) if language_list[i]=='fa'}

    path = os.path.join(result_directory, source_file_name)
    with open(path, mode='w', encoding='utf-8') as f:
        for line_text in clean_texts:
            f.writelines(line_text + '\n')


