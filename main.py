import nlp.tests
import nlp.core as core
import load
if __name__ == '__main__':
    # nlp.tests.bear_test()
    gpt2 = core.MODELS[2]
    gpt2_encoder = core.get_encoder(*gpt2)
    gpt2_distance = core.get_distance_func(gpt2_encoder)


