from newspaper import Article
from googlesearch import search
import os

def loadsources():
    with open(os.path.join(os.getcwd(), "trustedsources.config"), "r") as f:
        return f.read().splitlines()

def get_relevant_texts(trusted_sources, target_article, keyword_search=False, use_summary=False): 
    other_texts = []
    if keyword_search:
        target_article.nlp()

    for source in trusted_sources:
        if keyword_search:
            search_term = target_article.keywords[0]
            for i in range(1, len(target_article.keywords)):
                search_term = search_term + " " + target_article.keywords[i]
        else:
            search_term = target_article.title
        relavent_url = search(query= (search_term +" site:" + source), stop=1, pause=2)
        for url in relavent_url:
            article = Article(url)
            break
        article.download()
        article.parse() 
        if use_summary:
            article.nlp()
            other_texts.append(article.summary)
        else:
            other_texts.append(article.text)

if __name__ == '__main__':
    keyword_search = False
    target_summary = False
    auxillary_summary = True

    trusted_sources = loadsources()
    print("Enter URL for comparison")
    url = "https://www.space.com/elon-musk-emotional-spacex-astronaut-launch.html"

    target_article = Article(url)
    target_article.download()
    target_article.parse()
    
    if target_summary:
        target_text.nlp()
        target_text = target_article.summary
    else:
        target_text = target_article.text

    other_texts = get_relevant_texts(trusted_sources, target_article, keyword_search=False, use_summary=auxillary_summary)
    
