import collections
import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()


def is_begin_match(token):
    return '({' == token


def is_end_match(token):
    return '})' == token


def get_pos(ptag):
    if ptag is not None and 'VB'.__eq__(ptag[1][:1]):
        return 'v'
    return 'n'


def add_headlist_item(token, matched_tokens, ptag, dicts):
    if ptag is not None and len(ptag[1]) > 1 and not 'CD'.__eq__(ptag[1]) and not 'NNP'.__eq__(ptag[1]):
        lemma_token = wordnet_lemmatizer.lemmatize(token, get_pos(ptag))
        dicts[lemma_token] = matched_tokens


def has_item(items):
    for k, v in items:
        for k1, v1 in v.items():
            if v1 > 1:
                return True
    return False


def get_group_target_item(token, i, source_token_list, target_token_list):
    count = 0
    t = token
    last_num = int(t) - 1
    group_target_item = ''
    while t.isdigit() and last_num == (int(t) -1):
        i += 1
        last_num = int(t)
        t = source_token_list[i]
        group_target_item += target_token_list[last_num - 1] + ' '
        count += 1

    return group_target_item, count


def main():
    corpusdic = {}
    with open('../data/vn_en.align.A3.final', 'r') as align_result:
        count = 0
        source_tokens = []
        target_tokens = []
        en_corpus_lines = open('../data/source.tok', 'r').readlines()
        corpus_line_number = 0
        for line in align_result:
            if line[0] == '#':
                count = 2
                continue
            elif count == 2:
                target_tokens = line.split()
                count -= 1
                continue
            elif count == 1:
                source_tokens = line.split()
                count -= 1
                corpus_line_number += 1

            if count == 0:
                end_matched_group_flag = True
                matched_token_list = {}

                previous_token = ''
                en_corpus_line_tokens = en_corpus_lines[corpus_line_number - 1].split()
                pos_tag_source_token_list = nltk.pos_tag(en_corpus_line_tokens)
                word_token_index = 0
                ptag = None

                source_tokens_size = len(source_tokens)
                i = 0
                while i < source_tokens_size:
                    token = source_tokens[i]
                    token_count = 1

                    if end_matched_group_flag:
                        if is_begin_match(token):
                            end_matched_group_flag = False
                            lemma_token = wordnet_lemmatizer.lemmatize(previous_token, get_pos(ptag))
                            if corpusdic.get(lemma_token) is None:
                                matched_token_list = {}
                            else:
                                matched_token_list = corpusdic[lemma_token]
                        else:
                            if token != 'NULL':
                                word_token_index += 1
                                ptag = pos_tag_source_token_list[word_token_index - 1]

                            previous_token = token
                    else:
                        if is_end_match(token):
                            end_matched_group_flag = True
                            add_headlist_item(previous_token, matched_token_list, ptag, corpusdic)
                        else:
                            if ptag is not None:
                                target_item, token_count = get_group_target_item(token, i, source_tokens,
                                                                                 target_tokens)
                                if matched_token_list.get(ptag[1]) is None:
                                    matched_token_list[ptag[1]] = {}
                                if target_item in matched_token_list[ptag[1]].keys():
                                    matched_token_list[ptag[1]][target_item] += 1
                                else:
                                    matched_token_list[ptag[1]][target_item] = 1

                    i += token_count

    odcorpus = collections.OrderedDict(sorted(corpusdic.items()))

    for key, value in odcorpus.items():
        if has_item(value.items()):
            print(key + ' : ')
            for ik, iv in value.items():
                if iv > 1:
                    print(ik + '(' + str(iv) + ')', end=',')
            print('\r\n')

main()



