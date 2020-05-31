import torch
from transformers import *
import numpy as np
from scipy.spatial.distance import cosine

def get_encoder(model_class, tokenizer_class, pretrained, use_special_tokens):
    '''
    Creates the function which encodes any string using 
    the given model and tokenizer classes.
    '''
    model, tokenizer = (model_class.from_pretrained(pretrained),
                        tokenizer_class.from_pretrained(pretrained))
    def encode(text):
        input_ids = torch.tensor([tokenizer.encode(text, add_special_tokens=use_special_tokens)])
        with torch.no_grad():
            outputs = model(input_ids)
            return np.array(outputs[0][0,-1,:]).flatten()
    return encode

def create_test(main_statement, comparisons):
    def tests(encoder, distance_func):
        main_encoding = encoder(main_statement)
        for statement in comparisons:
            distance = distance_func(main_encoding, encoder(statement))
            print("%s:\n%.3f" % (statement, distance))
    return tests


MODELS = [(BertModel,       BertTokenizer,       'bert-base-uncased', True), # 0
          (OpenAIGPTModel,  OpenAIGPTTokenizer,  'openai-gpt', True), # 1
          (GPT2Model,       GPT2Tokenizer,       'gpt2', False), # 2
          (DistilBertModel, DistilBertTokenizer, 'distilbert-base-cased', True), # 3
          (XLNetModel,      XLNetTokenizer,      'xlnet-base-cased', True), #4
          (ElectraModel,    ElectraTokenizer,    'google/electra-large-discriminator', True) #5
         ]
if __name__ == '__main__':
    encoder_bert = get_encoder(*MODELS[0])
    encoder_gpt2 = get_encoder(*MODELS[2])
    encoder_xlnet = get_encoder(*MODELS[4])
    encoder_electra = get_encoder(*MODELS[5])

    df = lambda x, y: np.linalg.norm(x - y)
    def df2(a=1):
        '''
        Returns a distance function from a scale of 0 to 1
        The greater a is, the less strict we are in judging similarity
        '''
        def func(x, y):
            dist = cosine(x, y)
            return 1 - dist / (dist + a)
        return func
    
    ms = "The bear killed 3 people last Tuesday."
    comparisons = ["The bear killed 4 people last Tuesday.",
                   "The bear was nonviolent.",
                   "The bear killed 3 people last Wednesday.",
                   "The bear killed 3 people last Thursday.",
                   "The bear killed 3 people. This event occurred last Tuesday.",
                   "The bear ate 3 people last Tuesday.",
                   "The President spoke in Minnesota last Tuesday.",
                   "Pancakes are made with flour.",
                   "The bear did not kill anybody last Tuesday."]
    tests = create_test(ms, comparisons)
    print("BERT")
    tests(encoder_bert, df2(0.5))
    print()
    print("GPT-2")
    tests(encoder_gpt2, df2(0.002))
    print()
    print("XLNET")
    tests(encoder_xlnet, df2(0.25))
    print()
    print("ELECTRA")
    tests(encoder_electra, df2(0.01))
