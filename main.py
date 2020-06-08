import nlp.tests
import nlp.core as core
import load

if __name__ == '__main__':
    # nlp.tests.bear_test()
    keyword_search = False
    target_summary = False
    auxillary_summary = True

    gpt2 = core.MODELS[2]
    gpt2_encoder = core.get_encoder(*gpt2)
    gpt2_distance = core.get_distance_func(gpt2_encoder)


    trusted_sources = load.loadsources()
    url = "https://www.space.com/elon-musk-emotional-spacex-astronaut-launch.html"
    print(url)
    main_article = load.get_main_article(url)
    main_text = load.get_main_text(main_article)
    other_texts = load.get_relevant_texts(trusted_sources, main_article, keyword_search=False, use_summary=auxillary_summary)

    s_d = []
    for source, (title, statement) in zip(trusted_sources, other_texts):
        print(source)
        distance = distance_func(main_text, statement)
        s_d.append((source + " " + title, distance))
    
    s_d.sort(key=lambda x: x[1])
    out = ""
    for statement, distance in s_d:
        out += "%s:\n%.3f\n" % (statement, distance)
    file_p.write(out)
    print("Finished!")

    
