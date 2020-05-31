from newspaper import Article
from googlesearch import search
import os

def loadsources():
    with open(os.path.join(os.getcwd(), "trustedsources.config"), "r") as f:
        return f.read().splitlines()


if __name__ == '__main__':
    trusted_sources = loadsources()
    print("Enter URL for comparison")
    url = "https://www.space.com/elon-musk-emotional-spacex-astronaut-launch.html"
    print(trusted_sources)
    target_article = Article(url)
    target_article.download()
    target_article.parse()

    target_text = target_article.text
    other_texts = []

    for source in trusted_sources:
        relavent_url = search(query=(target_article.title + " site:" + source) , stop=1, pause=2)
        for url in relavent_url:
            article = Article(url)
            break
        article.download()
        article.parse() 
        other_texts.append(article.text)
        print()
        print()
        print(article.text)
    



    






    
