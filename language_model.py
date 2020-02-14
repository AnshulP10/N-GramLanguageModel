import re
import sys

def preprocess(corpus):
    corpus = corpus.lower()
    corpus = corpus.replace('(', '')
    corpus = corpus.replace(')', '')
    corpus = corpus.replace('--', ' ')
    corpus = corpus.replace(',\n', ' .\n')
    corpus = corpus.replace(';', ' .')
    corpus = corpus.replace('!', ' .\n')
    corpus = corpus.replace(',', ' ,')
    corpus = corpus.replace('?', ' .\n')
    corpus = corpus.replace("\'s", " \'s")
    corpus = corpus.replace('.', ' .')
    corpus = re.sub(r'(?m)^\}.*\n?', '', corpus)
    corpus = re.sub('[*]','', corpus)
    corpus = re.sub('\n+','\n',corpus)
    return corpus

def get_unigrams(corpus):
    unigrams = {}
    for sentence in corpus.split('.'):
        words = sentence.split(' ')
        i = 0
        while i < len(words):
            if words[i] in unigrams:
                unigrams[words[i]] += 1
            else:
                unigrams[words[i]] = 1
            i += 1
    return unigrams

def get_bigrams(corpus):
    bigrams = {}
    for sentence in corpus.split('.'):
        words = sentence.split(' ')
        i = 0
        while i < len(words) - 1:
            if words[i] not in bigrams:
                bigrams[words[i]] = {}
            if words[i+1] not in bigrams[words[i]]:
                bigrams[words[i]][words[i+1]] = 1 
            else:
                bigrams[words[i]][words[i+1]] += 1
            i += 1                
    return bigrams

def get_trigrams(corpus):
    trigrams = {}
    for sentence in corpus.split('.'):
        words = sentence.split(' ')
        i = 0
        while i < len(words) - 2:
            if words[i] not in trigrams:
                trigrams[words[i]] = {}
            if words[i+1] not in trigrams[words[i]]:
                trigrams[words[i]][words[i+1]] = {}
            if words[i+2] not in trigrams[words[i]][words[i+1]]:
                trigrams[words[i]][words[i+1]][words[i+2]] = 1 
            else:
                trigrams[words[i]][words[i+1]][words[i+2]] += 1
            i += 1                
    return trigrams

def laplace(w, unigrams):
    prob = (unigrams[w] + 1)/(sum(unigrams.values()) + len(unigrams))
    return prob

def wittenBell1(w1, w2, unigrams, bigrams):
    if w1 not in unigrams:
        unigrams[w1] = 0.25
    if w2 not in unigrams:
        unigrams[w2] = 0.25
    if w1 not in bigrams:
        bigrams[w1] = {}
    if w2 not in bigrams[w1]:
        bigrams[w1][w2] = 0.2

    prob = float(bigrams[w1][w2])/float(unigrams[w1] + len(bigrams[w1]))
    wb=1-len(bigrams[w1])/float(len(bigrams[w1])+sum((bigrams[w1].values())))
    prob=(wb)*prob+(1-wb)*unigrams[w2]/float(sum(unigrams.values()))
    return prob

def wittenBell2(w1, w2, w3, unigrams, bigrams, trigrams):
    if w1 not in bigrams:
        bigrams[w1] = {}
    if w2 not in bigrams[w1]:
        bigrams[w1][w2] = 0.25
    if w1 not in trigrams:
        trigrams[w1] = {}
    if w2 not in trigrams[w1]:
        trigrams[w1][w2] = {}
    if w3 not in trigrams[w1][w2]:
        trigrams[w1][w2][w3] = 0.25
    prob = float(trigrams[w1][w2][w3])/float(bigrams[w1][w2] + len(trigrams[w1][w2]))
    wb=1-len(trigrams[w1][w2])/float(len(trigrams[w1][w2])+sum((trigrams[w1][w2]).values()))
    prob1 = wittenBell1(w2, w3, unigrams, bigrams)
    prob=(wb)*prob+(1-wb)*prob1
    return prob

def kneserNey1(w1, w2, unigrams, bigrams,trigrams):
    if w1 not in unigrams:
        unigrams[w1] = 0.25
    if w2 not in unigrams:
        unigrams[w2] = 0.25
    if w1 not in bigrams:
        bigrams[w1] = {}
    if w2 not in bigrams[w1]:
        bigrams[w1][w2] = 0.25
    
    d = 0.75
    cont_count1 = 0
    cont_count2 = 0
    for w in trigrams:
        if w1 in trigrams[w] and w2 in trigrams[w][w1]:
            cont_count1 += 1
    for w in bigrams:
        if w1 in bigrams[w]:
            cont_count2 +=1

    prob = max(cont_count1 - d, 0)/float(cont_count2)
    prob += (d/unigrams[w1])*(len(bigrams[w1]))*(unigrams[w2]/sum(unigrams.values()))
    return prob

def kneserNey2(w1, w2, w3, unigrams, bigrams, trigrams):
    if w1 not in bigrams:
        bigrams[w1] = {}
    if w2 not in bigrams:
        bigrams[w2] = {}
    if w2 not in bigrams[w1]:
        bigrams[w1][w2] = 0.25
    if w3 not in bigrams[w2]:
        bigrams[w2][w3] = 0.25
    if w1 not in trigrams:
        trigrams[w1] = {}
    if w2 not in trigrams[w1]:
        trigrams[w1][w2] = {}
    if w3 not in trigrams[w1][w2]:
        trigrams[w1][w2][w3] = 0.25

    d = 0.75
    prob = max(trigrams[w1][w2][w3]-d,0)/float(bigrams[w2][w3])
    prob1 = kneserNey1(w2, w3, unigrams, bigrams, trigrams)
    prob += (d/bigrams[w1][w2])*(len(trigrams[w1][w2]))*prob1
    return prob

if __name__ == '__main__':
    loc = sys.argv[3]
    file = open(loc)
    corpus = file.read()
    corpus = preprocess(corpus)

    unigrams = get_unigrams(corpus)
    bigrams = get_bigrams(corpus)
    trigrams = get_trigrams(corpus)

    string = input("input sentence: ")
    string = preprocess(string)
    words = string.split(' ')
    ans = 1

    if sys.argv[2] == 'k':
        
        if sys.argv[1] == '1':
            i = 0
            while i <len(words) - 1:
                prob = laplace(words[i], unigrams)
                ans *= prob
                i += 1

        if sys.argv[1] == '2':
            i = 0
            while i < len(words) - 1:
                prob = kneserNey1(words[i], words[i+1], unigrams, bigrams, trigrams)
                ans *= prob
                i += 1

        if sys.argv[1] == '3':
            i = 0
            while i < len(words) - 2:
                prob = kneserNey2(words[i], words[i+1], words[i+2], unigrams, bigrams, trigrams)
                ans *= prob
                i += 1

    if sys.argv[2] == 'w':

        if sys.argv[1] == '1':
            i = 0
            while i <len(words) - 1:
                prob = laplace(words[i], unigrams)
                ans *= prob
                i += 1

        if sys.argv[1] == '2':
            i = 0
            while i < len(words) - 1:
                prob = wittenBell1(words[i], words[i+1], unigrams, bigrams)
                ans *= prob
                i += 1

        if sys.argv[1] == '3':
            i = 0
            while i < len(words) - 2:
                prob = wittenBell2(words[i], words[i+1], words[i+2], unigrams, bigrams, trigrams)
                ans *= prob
                i +=1

    print(ans)
