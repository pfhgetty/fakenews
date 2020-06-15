import nlp.tests
import nlp.core as core
import load

if __name__ == '__main__':
    # nlp.tests.bear_test()
    keyword_search = False
    target_summary = False
    auxillary_summary = False

    gpt2 = core.MODELS[2]
    gpt2_encoder = core.get_encoder(*gpt2)
    gpt2_distance = core.get_distance_func(gpt2_encoder)


    trusted_sources = load.loadsources()
    url = "https://www.space.com/elon-musk-emotional-spacex-astronaut-launch.html"
    # url = "https://www.foxnews.com/politics/coronavirus-wuhan-lab-china-compete-us-sources"
    print(url)
    main_article = load.get_main_article(url)
    main_text = load.get_main_text(main_article)
    other_texts, other_urls = load.get_relevant_texts(trusted_sources, main_article, keyword_search=False, use_summary=auxillary_summary)
    p_file = open("space.txt", 'w+')
    s_d = []
    gpt2_main_to = gpt2_distance(main_text)
    for source, (title, statement), url in zip(trusted_sources, other_texts, other_urls):
        print(source)
        distance = gpt2_main_to(statement)
        print(distance)
        s_d.append((source + " " + title + " " + url, distance))
    
    s_d.sort(key=lambda x: x[1])
    out = ""
    for statement, distance in s_d:
        out += "%s:\n%.3f\n" % (statement, distance)
        
    p_file.write(out)
    print("Finished!")

    
