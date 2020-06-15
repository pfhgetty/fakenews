from newspaper import Article
from googlesearch import search
import os
import time
def loadsources():
    with open(os.path.join(os.getcwd(), "trustedsources.config"), "r") as f:
        return f.read().splitlines()

def get_relevant_texts(trusted_sources, target_article, keyword_search=False, use_summary=False): 
    other_texts = []
    other_urls = []
    if keyword_search:
        target_article.nlp()

    for source in trusted_sources:
        if keyword_search:
            search_term = target_article.keywords[0]
            for i in range(1, len(target_article.keywords)):
                search_term = search_term + " " + target_article.keywords[i]
        else:
            search_term = target_article.title
        while True:
            try:
                relavent_url = search(query= (search_term +" site:" + source), num=1, stop=1, pause=3)
                for url in relavent_url:
                    article = Article(url)
                    other_urls.append(url)
                    break
                break
            except:
                print("Retrying google lol")
                time.sleep(30)
        while True:
            try:
                article.download()
                break
            except:
                print(other_urls[-1])
                print('article download failed retrying')
        try:
            article.parse()
        except:
            print(other_urls[-1])
            print('article parse failed')
            other_urls.pop()
            continue
 
        if use_summary:
            article.nlp()
            other_texts.append((article.title, article.summary))
        else:
            other_texts.append((article.title, article.text))
    
    return other_texts, other_urls

def get_main_article(url):
    target_article = Article(url)
    target_article.download()
    target_article.parse()
    return target_article

def get_main_text(article, use_summary=False):
    if use_summary:
        article.nlp()
        return article.summary
    return article.text

if __name__ == '__main__':
    keyword_search = False
    target_summary = False
    auxillary_summary = True

    trusted_sources = loadsources()
    print("Enter URL for comparison")
    url = "https://www.space.com/elon-musk-emotional-spacex-astronaut-launch.html"

    main_article = get_main_article(url)
    main_text = get_main_text(main_article, target_summary)
    
    other_texts = get_relevant_texts(trusted_sources, get_main_article, keyword_search=False, use_summary=auxillary_summary)
    
