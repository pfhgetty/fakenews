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
            add_special_tokens=use_special_tokens, add_prefix_space=add_prefix_space)])
        with torch.no_grad():
            outputs = model(input_ids)
            arr = np.array(outputs[0][0,:,:])
            return arr
    print("Success!")
    return encode


def get_distance_func(encoder):
    def get_distance(x, y):
        enc_x = encoder(x)
        enc_y = encoder(y)
        dist = 0
        bound_1 = lambda a: min(max(a, -1), 1)
        for a in enc_x:
            for b in enc_y:
                cos_sim = bound_1(1 - cosine(a,b))
                dist +=  1 - (math.acos(abs(cos_sim))/math.pi)
        return dist / (len(enc_x)* len(enc_y))
    return get_distance


MODELS = [(BertModel,       BertTokenizer,       'bert-base-uncased', True), # 0
          (OpenAIGPTModel,  OpenAIGPTTokenizer,  'openai-gpt', True), # 1
          (GPT2Model,       GPT2Tokenizer,       'gpt2-xl', False, True), # 2
          (DistilBertModel, DistilBertTokenizer, 'distilbert-base-cased', True), # 3
          (XLNetModel,      XLNetTokenizer,      'xlnet-base-cased', True), #4
          (ElectraModel,    ElectraTokenizer,    'google/electra-large-discriminator', True) #5
         ]