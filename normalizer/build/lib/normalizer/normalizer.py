import re

from normalizer.constants import allowed_halfspace_chars
from normalizer.constants import allowed_pass_chars
from normalizer.constants import allowed_persian_chars
from normalizer.constants import currency_symbols
from normalizer.constants import emoji_dict
from normalizer.constants import english_alphabet
from normalizer.constants import english_marker
from normalizer.constants import link_specifiers
from normalizer.constants import rain_symbols
from normalizer.constants import reformation_alphabet_dict
from normalizer.constants import regex_duplicate
from normalizer.constants import selected_emojies
from normalizer.constants import set_english_marker
from normalizer.constants import sign_dict
from normalizer.constants import upper2lower


class Normalizer(object):
    def __init__(self, hold_link=True, hold_mention=True, hold_emoji=True,
                 hold_currency_symbols=True, remove_end_text_hashtag=False,
                 remove_english_marker=False, change_hashtag_to_text=False):
        self.hold_link = hold_link
        self.hold_mention = hold_mention
        self.hold_emoji = hold_emoji
        self.hold_currency_symbols = hold_currency_symbols
        self.remove_endText_hashtag = remove_end_text_hashtag
        self.remove_english_marker = remove_english_marker
        self.change_hashtag_toText = change_hashtag_to_text
        self.ordinary_clean_condition = (self.hold_link and
                                         self.hold_mention and
                                         not self.remove_endText_hashtag and
                                         not self.remove_english_marker and
                                         not self.change_hashtag_toText)
        self.allowed_english_chars = english_alphabet + english_marker
        self.allowed_hashtag_chars = (allowed_persian_chars +
                                      english_alphabet +
                                      '_')
        self.allowed_standalone_chars = ''
        if self.hold_currency_symbols:
            self.allowed_standalone_chars += currency_symbols
        if self.hold_emoji:
            self.allowed_standalone_chars += selected_emojies
        if self.hold_emoji:
            self.reformation_dict = dict(
                reformation_alphabet_dict,
                **emoji_dict,
                **sign_dict)
        else:
            self.reformation_dict = dict(reformation_alphabet_dict, **sign_dict)
        self.reformation_dict_keys = set(self.reformation_dict.keys())
        self.upper2lower_dict_keys = set(upper2lower.keys())
        self.other_char_state = 0
        self.persian_word_state = 1
        self.english_word_state = 2
        self.pass_chars_state = 3
        self.hashtag_state = 4
        self.symbol_word_state = 5
        self.mention_state = 6
        self.link_state = 7

    def _change_upper2lower(self, word):
        for specifier in link_specifiers:
            if specifier in word:
                return word, self.link_state

        if '@' in word:
            new_word = word.replace('@', 's' + hex(ord('@')) + ' ')
            return new_word, self.mention_state

        new_word = ''
        for char in word:
            if len(set(char).intersection(self.upper2lower_dict_keys)) != 0:
                char = upper2lower[char]
            new_word += char
        return new_word, self.english_word_state

    def _change_hashtag(self, hashtag):
        hashtag += ' '
        word_list = []
        word = ''
        previous_state = 0
        for char in hashtag:
            if char in self.allowed_hashtag_chars:
                state = 1
            elif char in allowed_halfspace_chars:
                state = 2
            elif char in allowed_pass_chars:
                state = 3
            else:
                state = 0

            if state == 1:
                if previous_state == 1:
                    word += char
                else:
                    word = char
            elif state == 2:
                if previous_state == 1:
                    word_list.append(word)
                    word = ''
            elif state == 3:
                state = previous_state
            else:
                if previous_state == 1:
                    word_list.append(word)
                if self.change_hashtag_toText is False:
                    word_list.append('s' + hex(ord(char)))
                word = ''
            previous_state = state
        if self.change_hashtag_toText:
            new_hashtag = ' '.join(word_list)
            new_hashtag = new_hashtag.replace('_', ' ').strip()
        else:
            new_hashtag = ' '.join(word_list[:-1])
        return new_hashtag

    def normalize(self, text: str) -> str:
        if not text:
            return ''

        if self.hold_emoji:
            for rain_symbol in rain_symbols:
                if rain_symbol in text:
                    text = text.replace(rain_symbol, '🌈')
        temp = ''
        for char in text:
            if len(set(char).intersection(self.reformation_dict_keys)) != 0:
                char = self.reformation_dict[char]
            temp += char
        text = temp + ' '
        word_list = []
        state_list = []
        word = ''
        previous_state = self.other_char_state
        hashtag_flag = False
        for char in text:
            if char in allowed_persian_chars:
                state = self.persian_word_state
            elif char in self.allowed_english_chars:
                state = self.english_word_state
            elif char in allowed_pass_chars:
                state = self.pass_chars_state
            elif char == '#':
                state = self.hashtag_state
            elif char in self.allowed_standalone_chars:
                state = self.symbol_word_state
            else:
                state = self.other_char_state
            ###
            if hashtag_flag:
                if char == ' ':
                    word = self._change_hashtag(word)
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(self.hashtag_state)
                    word = char
                    hashtag_flag = False
                elif char == '#':
                    word = self._change_hashtag(word)
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(self.hashtag_state)
                    word = char
                    hashtag_flag = True
                else:
                    word += char
            elif state == self.persian_word_state:
                if previous_state == self.persian_word_state:
                    if char == u'\u0622':
                        char = u'ا'
                    word += char
                elif previous_state == self.english_word_state:
                    word, word_state = self._change_upper2lower(word)
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(word_state)
                    word = char
                elif previous_state == self.symbol_word_state:
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(self.symbol_word_state)
                    word = char
                else:
                    word = char
            elif state == self.english_word_state:
                if previous_state == self.english_word_state:
                    word += char
                elif previous_state == self.persian_word_state:
                    word = re.sub(regex_duplicate, r'\1', word)
                    word_list.append(word)
                    state_list.append(self.persian_word_state)
                    word = char
                elif previous_state == self.symbol_word_state:
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(self.symbol_word_state)
                    word = char
                else:
                    word = char
            elif state == self.pass_chars_state:
                state = previous_state
            elif state == self.hashtag_state:
                hashtag_flag = True
                if previous_state == self.persian_word_state:
                    word = re.sub(regex_duplicate, r'\1', word)
                    word_list.append(word)
                    state_list.append(self.persian_word_state)
                    word = char
                elif previous_state == self.english_word_state:
                    word, word_state = self._change_upper2lower(word)
                    if word_state == self.link_state:
                        word += char
                        hashtag_flag = False
                        state = self.english_word_state
                    else:
                        word_list.append(word)
                        for i in range(len(word.split())):
                            state_list.append(self.english_word_state)
                        word = char
                elif previous_state == self.symbol_word_state:
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(self.symbol_word_state)
                    word = char
                else:
                    word = char
            elif state == self.symbol_word_state:
                char = 's' + hex(ord(char))
                if previous_state == self.symbol_word_state:
                    word += (' ' + char)
                elif previous_state in (
                        self.persian_word_state, self.english_word_state):
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(previous_state)
                    word = char
                else:
                    word = char
            else:
                if previous_state == self.persian_word_state:
                    word = re.sub(regex_duplicate, r'\1', word)
                    word_list.append(word)
                    state_list.append(self.persian_word_state)
                elif previous_state == self.english_word_state:
                    word, word_state = self._change_upper2lower(word)
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(word_state)
                elif previous_state == self.symbol_word_state:
                    word_list.append(word)
                    for i in range(len(word.split())):
                        state_list.append(self.symbol_word_state)
            previous_state = state
        if self.ordinary_clean_condition:
            new_text = ' '.join(word_list)
        else:
            new_word_list = []
            for word in word_list:
                new_word_list.extend(word.split())
            selected_index = list(range(len(new_word_list)))
            #
            if self.remove_endText_hashtag:
                end_index = len(new_word_list)
                for state in state_list[::-1]:
                    if state != self.hashtag_state:
                        break
                    else:
                        end_index -= 1
                selected_index = list(range(end_index))
            if self.hold_mention is False:
                selected_index = [i for i in selected_index if
                                  state_list[i] != self.mention_state]
            if self.hold_link is False:
                selected_index = [i for i in selected_index if
                                  state_list[i] != self.link_state]
            if self.remove_english_marker:
                index_list = []
                for i in selected_index:
                    if state_list[i] == self.english_word_state:
                        set_word = set(new_word_list[i])
                        len_intersect = len(
                            set_word.intersection(set_english_marker))
                        if len_intersect != len(set_word):
                            index_list.append(i)
                    else:
                        index_list.append(i)
                selected_index = index_list
            new_word_list = [new_word_list[i] for i in selected_index]
            new_text = ' '.join(new_word_list)

        return new_text
