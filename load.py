from newspaper import Article



if __name__ == '__main__':
    print("Enter URL for comparison")
    url = input()

    target_article = Article(url)
    target_article.download()
    target_article.parse()


    
