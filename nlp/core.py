import torch
from transformers import *
import numpy as np
from scipy.spatial.distance import cosine

def get_encoder(model_class, tokenizer_class, pretrained, use_special_tokens, ignore_indices=[]):
    '''
    Creates the function which encodes any string using 
    the given model and tokenizer classes.
    ignore_indices: list of indices to remove from output encoding
    '''
    print("Loading model...")
    model, tokenizer = (model_class.from_pretrained(pretrained),
                        tokenizer_class.from_pretrained(pretrained))
    def encode(text):
        input_ids = torch.tensor([tokenizer.encode(text, add_special_tokens=use_special_tokens)])
        with torch.no_grad():
            outputs = model(input_ids)
            arr = np.array(outputs[0][0,-1,:]).flatten()
            return np.delete(arr, ignore_indices)
    print("Success!")
    return encode


def get_distance_func(encoder):
    def get_distance(x, y):
        return 1 - cosine(encoder(x), encoder(y))
    return get_distance


MODELS = [(BertModel,       BertTokenizer,       'bert-base-uncased', True), # 0
          (OpenAIGPTModel,  OpenAIGPTTokenizer,  'openai-gpt', True), # 1
          (GPT2Model,       GPT2Tokenizer,       'gpt2-xl', False), # 2
          (DistilBertModel, DistilBertTokenizer, 'distilbert-base-cased', True), # 3
          (XLNetModel,      XLNetTokenizer,      'xlnet-base-cased', True), #4
          (ElectraModel,    ElectraTokenizer,    'google/electra-large-discriminator', True) #5
         ]