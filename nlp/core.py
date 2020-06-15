import torch
from transformers import *
import numpy as np
from scipy.spatial.distance import cosine
import math

def get_encoder(model_class, tokenizer_class, pretrained, use_special_tokens=True, add_prefix_space=False, ignore_indices=[]):
    '''
    Creates the function which encodes any string using 
    the given model and tokenizer classes.
    ignore_indices: list of indices to remove from output encoding
    '''
    print("Loading model...")
    model, tokenizer = (model_class.from_pretrained(pretrained),
                        tokenizer_class.from_pretrained(pretrained))
    def encode(text):
        input_ids = torch.tensor([tokenizer.encode(text,
            add_special_tokens=use_special_tokens, add_prefix_space=add_prefix_space, max_length=1024)])
        with torch.no_grad():
            outputs = model(input_ids)
            arr = np.array(outputs[0][0,-1,:])
            return arr
    print("Success!")
    return encode


def get_distance_func(encoder):
    def get_distance_from(x):
        enc_x = encoder(x)
        def get_distance_to(y):
            enc_y = encoder(y)
            dist = 0
            bound_1 = lambda a: min(max(a, -1), 1)
            # for a in enc_x:
                # for b in enc_y:
            cos_sim = bound_1(1 - cosine(enc_x,enc_y))
            dist +=  1 - (math.acos(abs(cos_sim))/math.pi)
            print(dist)
            return dist
        return get_distance_to
    return get_distance_from


MODELS = [(BertModel,       BertTokenizer,       'bert-base-uncased', True), # 0
          (OpenAIGPTModel,  OpenAIGPTTokenizer,  'openai-gpt', True), # 1
          (GPT2Model,       GPT2Tokenizer,       'distilgpt2', False, True), # 2
          (DistilBertModel, DistilBertTokenizer, 'distilbert-base-cased', True), # 3
          (XLNetModel,      XLNetTokenizer,      'xlnet-base-cased', True), #4
          (ElectraModel,    ElectraTokenizer,    'google/electra-large-discriminator', True) #5
         ]