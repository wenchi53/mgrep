import sys, re
from gensim.models import KeyedVectors


def mg(input, num, word_vectors):
    out = [input]
    s = word_vectors.most_similar(input)
    for x in range(0, num):
        out.append((s[x][0]))
    return out


def reg(pattern, data):
    result = [];
    pat = re.compile(pattern)
    for d in data:
        if pat.search(d):
            result.append(d)
    return result;


def parseMG(string, sim_num, word_vectors, data):
    if(string[0].find("(mg(") == -1):
        return string


    while(string[0].find("(mg(") != -1):
        result = []
        for str in string:
            begin = str.find("(mg(")
            end = str.find(")mg)")
            reg_sub = reg(str[begin+4:end], data)
            for substring in reg_sub:
                similar_sub = mg(substring, int(sim_num), word_vectors)
                for sub in similar_sub:
                    result.append(str[:begin] + sub + str[end+4:])
            string = list(set(result))
    return string

def dlm(f1, f2, f3, word_vectors):
    value = word_vectors.most_similar(positive=[f3, f2], negative=[f1])
    return value[1][0]


def parseDL(string, sim_num, word_vectors, data):
    if(string[0].find("(dl1(") == -1):
        return string


    while(string[0].find("(dl1(") != -1):
        result = []
        for str in string:
            begin1 = str.find("(dl1(")
            end1 = str.find(")dl1)")

            begin2 = str.find("(dl2(")
            end2 = str.find(")dl2)")

            reg_sub1 = reg(str[begin1+5:end1], data)
            reg_sub2 = reg(str[begin2+5:end2], data)

            for substring1 in reg_sub1:
                for substring2 in reg_sub2:
                    '''
                    similar_sub1 = dlm(substring, int(sim_num), word_vectors)
                    for sub in similar_sub:
                        result.append(str[:begin] + sub + str[end+5:])
                    '''




            string = list(set(result))
    return string


def grep(input, model):
    print("grep '%s' %s" % (input, model))

word_vectors = KeyedVectors.load_word2vec_format(sys.argv[2], binary=False)

dataSet = word_vectors.most_similar('F2V_CONDBR')
data = []

for d in dataSet:
    data.append(d[0])


input = sys.argv[1]
sim_num = sys.argv[3]


result = parseMG([input],sim_num, word_vectors, data)

for r in result:
    grep(r,sys.argv[2])












