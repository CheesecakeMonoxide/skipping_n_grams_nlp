import nltk, random, os

#bigram to 5-gram models:
#process given corpus and produce 2,3,4,5-grams lists
def n_gram(tokens, n):
    
    main_list = []
    sub_list = []
    if n == 2:
        for i in range(len(tokens)-1):
            sub_list = []
            sub_list.append(tokens[i])
            sub_list.append(tokens[i+1])
            sub_list = tuple(sub_list)
            main_list.append(sub_list)
    elif n == 3:
        for i in range(len(tokens)-2):
            sub_list = []
            sub_list.append(tokens[i])
            sub_list.append(tokens[i+1])
            sub_list.append(tokens[i+2])
            sub_list = tuple(sub_list)
            main_list.append(sub_list)
    elif n == 4:
        for i in range(len(tokens)-3):
            sub_list = []
            sub_list.append(tokens[i])
            sub_list.append(tokens[i+1])
            sub_list.append(tokens[i+2])
            sub_list.append(tokens[i+3])
            sub_list = tuple(sub_list)
            main_list.append(sub_list)
    elif n == 5:
        for i in range(len(tokens)-4):
            sub_list = []
            sub_list.append(tokens[i])
            sub_list.append(tokens[i+1])
            sub_list.append(tokens[i+2])
            sub_list.append(tokens[i+3])
            sub_list.append(tokens[i+4])
            sub_list = tuple(sub_list)
            main_list.append(sub_list)

    return main_list


#markov chain: predict the next word given a word/sequence of words
#produce a dictionary - {('word', 'sequence'):['possible', 'next', 'word']}
class Markov_Gen:
    
    def __init__(self, n_gram_list):       
        self.n_gram_list = n_gram_list
        self.unique_n_grams = set(self.n_gram_list)
        self.sentence_list = []

    def n_gram_counter(self):
        main_dict = {}
        for i in range(len(self.n_gram_list)):
            if self.n_gram_list[i] in main_dict.keys():
                main_dict[self.n_gram_list[i]] += 1
            else:
                main_dict[self.n_gram_list[i]] = 1
        self.main_dict = main_dict
        return self.main_dict

    def dict_Gen(self):
        markov_dict = {}
        for ab in self.unique_n_grams:
            a = ab[:-1]
            a = tuple(a)
            b = ab[-1]
##            self.p_of_b_given_a = self.n_gram_counter()[ab] / self.token_list.count(a)
##            print(a + " " + b + " / " + a + " = " + str(self.p_of_b_given_a))
##            if self.p_of_b_given_a >= 0.05:
            if a in markov_dict.keys():
                markov_dict[a].append(b)
            else:
                markov_dict[a] = []
                markov_dict[a].append(b)
##            else:
##                markov_dict[a] = []
        self.markov_dict = markov_dict
        return self.markov_dict

    def next_Word(self, previous_tup, markov_Dict):
        if previous_tup in markov_Dict.keys():
            val_list = markov_Dict[previous_tup]
            next_word = [random.choice(val_list)]
        else:
            dummy_tup = [previous_tup[-2], previous_tup[-1]]
            dummy_tup = tuple(dummy_tup)
            if dummy_tup in markov_Dict.keys():
                val_list = markov_Dict[dummy_tup]
                next_word = [random.choice(val_list)] #placeholder for now, but should be replaced by a POS_tag()
            else:
                dummy_tup2 = [dummy_tup[-1]]
                dummy_tup2 = tuple(dummy_tup2)
                val_list = markov_Dict[dummy_tup2]
                next_word = [random.choice(val_list)] #placeholder for now, but should be replaced by a POS_tag()
        self.next_word = tuple(next_word)
        return self.next_word

    def write_Sentence(self, previous_tup, markov_Dict):
        for i in range(len(previous_tup)):
            self.sentence_list.append(previous_tup[i])
        if self.sentence_list[-1] == '.' or  self.sentence_list[-1] == '?' or self.sentence_list[-1] == '!':
            self.autogen_sentence = self.sentence_list
        else:
##            if len(self.sentence_list) % 4 == 0:
##                prev_tup = [self.sentence_list[-3], self.sentence_list[-2], self.sentence_list[-1]]
            if len(self.sentence_list) % 2 == 0:
                prev_tup = [self.sentence_list[-2], self.sentence_list[-1]]
##            elif len(self.sentence_list) % 3 == 0:
##                prev_tup = [self.sentence_list[-3], self.sentence_list[-2], self.sentence_list[-1]]
            elif len(self.sentence_list) % 5 == 0:
                prev_tup = [self.sentence_list[-3], self.sentence_list[-2], self.sentence_list[-1]]
            elif len(self.sentence_list) % 2 == 1:
                prev_tup = [self.sentence_list[-1]]
            prev_tup = tuple(prev_tup)
            next_word = self.next_Word(prev_tup, markov_Dict)
            self.autogen_sentence = self.write_Sentence(next_word, markov_Dict)
        return self.autogen_sentence            

def find_word(gram_list):
    start_list = []
    for item in gram_list:
        if item[0][0].isupper():
            start_list.append(item)
    start_word = random.choice(start_list)
    return start_word

#sentence parsers and phrase structure rules for editing: parse generated sentence, and edit to the nearest acceptable PS rule
#templates


##sample = "My college roommate was working at my retail electronics store in the early 2000s. My college roommate was developing a program in college. My highschool friend was working at the department store during her college years. Her friend did not call her immediately. A friend in need is a friend indeed."
##tokens = nltk.word_tokenize(sample)


sample = open('C:\\Users\\Monica Aguilar\\Desktop\\consp.txt')
tokens = nltk.word_tokenize(sample.read())

bi_grams = n_gram(tokens, 2)
tri_grams = n_gram(tokens, 3)
four_grams = n_gram(tokens, 4)

n_grams = bi_grams + tri_grams + four_grams

##print(sample_Markov.dict_Gen().keys())
##print(sample_Markov.n_gram_counter())
##print(m_dict)

blog = []
for i in range (5):
    start_word = find_word(bi_grams)
    sample_Markov = Markov_Gen(n_grams)
    m_dict = sample_Markov.dict_Gen()
    new_sentence_list = sample_Markov.write_Sentence(start_word, m_dict)
    new_sentence_str = [' '.join(new_sentence_list)]
    blog.append(new_sentence_str)

for item in blog:
    print(item[0])
    print('')

##count = n_gram_counter(n_grams)
##print(count)

##print('')
##print('Write a word below and the computer will guess the next word that comes after it.')
##prev_word = input()
##
##next_word = sample_Markov.next_Word(prev_word)
##
##print('The next word is: ' + next_word + '.')

