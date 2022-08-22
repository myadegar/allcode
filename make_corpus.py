import os
from tqdm import tqdm
import re

from parsivar import Tokenizer
from normalizer import Normalizer

normalizer = Normalizer(hold_link=False, hold_mention=False, hold_emoji=False,
                                hold_currency_symbols=False, remove_end_text_hashtag=False,
                                remove_english_marker=True, change_hashtag_to_text=True)

exception_marker = '[?!.؟]'

tokenizer = Tokenizer()


source_directory = r'F:\persian_corpus\text'
destination_directory = r'F:\persian_corpus\corpus'

file_names = os.listdir(source_directory)
all_texts = set()
for file_name in file_names:
    path = os.path.join(source_directory, file_name)
    with open(path, mode='r', encoding='utf-8') as text_file:
        for line_text in tqdm(text_file):
            sents = tokenizer.tokenize_sentences(normalizer.normalize(line_text))
            for txt in sents:
                if len(txt.split()) > 3:
                    txt = re.sub(exception_marker, '', txt)
                    txt = txt.strip()
                    all_texts.add(txt)
###
max_count = 1000000
count = 0
file_ind = 0
for txt in tqdm(all_texts):
    if count == 0:
        new_file_name = 'persian_text'+'_'+str(file_ind)+'.txt'
        path_write = os.path.join(destination_directory, new_file_name)
        f_write = open(path_write, mode='w', encoding='utf-8')
    f_write.writelines(txt + '\n')
    count += 1
    if count >= max_count:
        count = 0
        file_ind += 1
        f_write.close()
f_write.close()

