from nlp.core import get_encoder, MODELS, get_distance_func
import numpy as np
from scipy.spatial.distance import cosine
import math
gpt2_center = list(map(float, open("center.txt", 'r').read().strip('][').split(', ')))

def create_test(main_statement, comparisons):
    def tests(distance_func, file_p):
        # main_encoding = encoder(main_statement)
        s_d = []
        out = ""
        for statement in comparisons:
            distance = distance_func(main_statement, statement)
            s_d.append((statement, distance))
        
        s_d.sort(key=lambda x: x[1])

        for statement, distance in s_d:
            out += "%s:\n%.3f\n" % (statement, distance)
        file_p.write(out)
    return tests

def bear_test():
    # encoder_bert = get_encoder(*MODELS[0])
    encoder_gpt2 = get_encoder(*MODELS[2])
    # encoder_xlnet = get_encoder(*MODELS[4])
    # encoder_electra = get_encoder(*MODELS[5])

    df = get_distance_func(encoder_gpt2)
    ms = "The bear killed three people last Tuesday."
    comparisons = ["The bear killed four people last Tuesday.",
                   "The bear was nonviolent.",
                   "The bear killed three people last Wednesday.",
                   "The bear killed three people. This event occurred last Tuesday.",
                   "The bear ate three people last Tuesday.",
                   "The President spoke in Minnesota last Tuesday.",
                   "Pancakes are made with flour.",
                   "The bear did not kill anybody last Tuesday.",
                   "I am not Asian.",
                   "I am not not Asian.",
                   "The bear did not not kill anybody last Tuesday.",
                   "The bear was not nonviolent."]
    tests = create_test(ms, comparisons)
    # print("BERT")
    # tests(encoder_bert, df2(0.5))
    print("GPT-2")
    gpt2_file = open("gpt-2_bear_test.txt", 'w+')
    tests(df, gpt2_file)
    print()
    # print("XLNET")
    # tests(encoder_xlnet, df2(0.25))
    # print()
    # print("ELECTRA")
    # tests(encoder_electra, df2(0.01))

def get_diff(ms, same, encoder, num=10):
    ms_encoding = encoder(ms)
    same_encoding = encoder(same)
    A = np.abs(ms_encoding - same_encoding)
    A_sort = np.argsort(A)[-1:-num:-1]
    print(A_sort)
    print(A[A_sort])
    return A_sort

def get_rank(sorts):
    ranking = dict()
    for sort in sorts:
        length = len(sort)
        for i, e in enumerate(sort):
            if e not in ranking.keys():
                ranking[e] = 0
            ranking[e] += length - i
    return ranking


def centering():
    '''
    Find the center in vector space of statements with opposite meanings
    '''
    encoder_gpt2 = get_encoder(*MODELS[2])
    ms = [
        ("The bear was very violent.", "The bear was not violent."), #1
        ("The bear was killed 3 people.", "The bear killed nobody."),
        ("I hate cookies.", "I love cookies."), 
        ("The President gave a speech in Minnesota.",
            "The President did not give a speech in Minnesota."), 
        ("My television is broken.", "My television is not broken."),
        ("I know him better than you know him.", "You know him better than I know him."),
        ("Buttermilk scotch tastes like heaven.", "Buttermilk scotch tastes awful."),
    ]
    centers = [(encoder_gpt2(s1)+encoder_gpt2(s2))/2 for s1,s2 in ms]
    dists = np.zeros(shape=(len(centers), len(centers)))
    for i in range(len(centers)):
        for j in range(len(centers)):
            dists[i, j] = np.linalg.norm(centers[i] - centers[j])
    # Print distances between measured centers
    print(
        '\n'.join([' '.join(['%.3f' % dist for dist in row])
            for row in dists])
    )
    # Write the average center
    center_file = open("center.txt", "w")
    center_file.write(str(list(sum(centers) / len(centers))))



def linear_transform():
    '''
    Find which components of the vector differ most between statements with similar meanings
    and ignore them during the distance calculation.
    This did not work very well.
    '''
    ms = "The bear killed 3 people last Tuesday."
    same = "The bear killed 3 people. This event occurred last Tuesday."
    o = "The bear was nonviolent. This was observed last Tuesday."
    o2 = "The bear did not kill anybody last Tuesday."
    a = "The President spoke in Minnesota to a crowd of bystanders."
    a2 = "In Minnesota, the President gave a speech to bystanders."
    two_short = "My television is broken. It is Karen’s fault."
    one_long = "Because of Karen, my television is broken."
    encoder_gpt2 = get_encoder(*MODELS[2])
    rank1=get_diff(ms, same, encoder_gpt2, 200)
    rank2=get_diff(o, o2, encoder_gpt2, 200)
    rank3=get_diff(a, a2, encoder_gpt2, 200)
    rank4=get_diff(two_short, one_long, encoder_gpt2, 200)
    ranking = get_rank([rank1, rank2, rank3])
    sorted_ranking = [(k,v) for k, v in sorted(ranking.items(), key=lambda item: item[1], reverse=True)]
    print(sorted_ranking)
    ignore_indices = [index for index, _ in sorted_ranking[:15]]
    print("IGNORE")
    print(ignore_indices)


