from collections import Counter
import re
import numpy as np


class AutoCorrectWords(object):

    def __init__(self, corpus_file_path):
        with open(corpus_file_path, "r") as file:
            lines = file.readlines()
            words = []
            for line in lines:
                words += re.findall(r'\w+', line.lower())

        self.vocabs=set(words)
        self.word_counts = Counter(words)
        total_words = float(sum(self.word_counts.values()))
        self.probs = {word: self.word_counts[word] / total_words for word in self.vocabs}

    def get_corrections(self,word):
        word=word.lower()
        if word in self.vocabs:
            return [word]
        suggestions = list((word in self.vocabs) or list(self.edit_one_letter(word).intersection(self.vocabs)) or list(
            self.edit_two_letters(word).intersection(self.vocabs)) )
        return suggestions


    def edit_one_letter(self,word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        split_l = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        insert_l = [a + l + b for a, b in split_l for l in letters]
        replace_l = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in letters if a+l+b!=word]
        switch_l = [L + R[1] + R[0] + R[2:] for L, R in split_l if len(R) >= 2]
        delete_l = [L + R[1:] for L, R in split_l]
        return set(insert_l+replace_l+switch_l+delete_l)

    def edit_two_letters(self,word):
        return set(e2 for e1 in self.edit_one_letter(word) for e2 in self.edit_one_letter(e1))


    def min_edit_distance(self,source, target, ins_cost=1, del_cost=1, rep_cost=2):
        m = len(source)
        n = len(target)
        D = np.zeros((m + 1, n + 1), dtype=int)
        for row in range(1, m + 1):
            D[row, 0] = D[row - 1, 0] + del_cost
        for col in range(1, n + 1):
            D[0, col] = D[0, col - 1] + ins_cost
        for row in range(1, m + 1):
            for col in range(1, n + 1):
                r_cost = rep_cost
                if source[row - 1] == target[col - 1]:
                    r_cost = 0
                D[row, col] = min(
                    [D[row - 1, col] + del_cost, D[row, col - 1] + ins_cost, D[row - 1, col - 1] + r_cost])
        med = D[m, n]
        return med

    def get_correct_word(self, word):
        dic={}
        for targ in self.get_corrections(word):
            dic[targ]=self.min_edit_distance(word,targ)
        if bool(dic):
            min_key = min(dic, key=lambda k: dic[k])
        else:
            min_key=word
        return min_key

corps = AutoCorrectWords("data/shakespeare")

word='BOOOK'
print(corps.get_corrections(word))
print(corps.get_correct_word(word))












