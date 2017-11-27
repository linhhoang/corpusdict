import base64
import math
import gzip

BASE_64_STRING = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


def encode_base_64(n):
    s = n
    result = ''
    while s > 0:
        r = s % 64
        s = math.floor(s / 64)
        result = BASE_64_STRING[r - 1] + result

    return result


def decode_base_64(s):
    l = len(s)
    p = 0
    total = 0
    for i in range(l):
        i = BASE_64_STRING.index(s[l-i-1]) + 1
        n = i*pow(64, p)
        total += n
        p += 1
    return total;


def main():
    print('Convert dictionary')
    corpusdic = {}
    dict_index_file = open('data/EV/anhviet109K.index', 'r', encoding="utf8")
    dict_file = gzip.open('data/EV/anhviet109K.dict.dz', 'rb')

    dic_indexes = dict_index_file.readlines()
    # for i in range(5):
    line_words = dic_indexes[0].replace('\n', '').split('\t')
    if len(line_words) >= 3:
        word_index = decode_base_64(line_words[1])
        word_len = decode_base_64(line_words[2])
        print('word:' + line_words[0] + ', index=' + str(word_index) + ', len=' + str(word_len));
        dict_file.seek(word_index + 2)
        content = dict_file.read(word_len)
        print(content.decode('utf8'))

    dict_index_file.close()
    dict_file.close()

main()


print(encode_base_64(872))