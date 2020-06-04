import nlp.tests
import nlp.core as core

if __name__ == '__main__':
    gpt2 = core.MODELS[2]
    gpt2_encoder = core.get_encoder(*gpt2)
    gpt2_distance = core.get_distance_func(gpt2_encoder)

    