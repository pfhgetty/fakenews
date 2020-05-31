from newspaper import Article
from googlesearch import search
import os

def loadsources():
    relevant_text = []
    with open(os.path.join(os.getcwd(), "trustedsources.config"), "r") as f:
        relavent_text = f.read().splitlines()
    
    return relavent_text


if __name__ == '__main__':
    trusted_sources = loadsources()
    print("Enter URL for comparison")
    url = input()

    other_texts = [] # title, text
    target_article = Article(url)
    target_article.download()
    target_article.parse()

    target_text = target_article.text

    for source in trusted_sources:
        relavent_url = search(query=(target_article.title + " site:" + source) , stop=1, pause=2)
        article = Article(relavent_url[0])
        article.download()
        article.parse() 
        other_texts.append(article.text)


    






    
