import pickle
import pymongo

# import wikipedia
import wikipediaapi
import sys

mc = pymongo.MongoClient()
db = mc["wikicache"]
articles = db["articles"]


def fetch_article(article_title, wiki_wiki):
    """Check MongoDB cache for article, scrape if needed, return stored article"""
    found_articles = list(articles.find({"title": article_title}))
    if len(found_articles) == 0:
        sys.stdout.write(f"Scraping {article_title}...")
        try:
            article = wiki_wiki.page(article_title)
        except requests.exceptions.Timeout:
            sys.stdout.write(f"Timeout on {article_title}...")
            return None

        #         try:
        #             url = article.fullurl
        #         except:
        #             url = None

        article_data = {
            "title": article.title,
            # 'backlinks': article.backlinks,
            "text": article.text,
            "summary": article.summary,
            # 'url': url,
        }
        sys.stdout.write(" Saving...")
        articles.insert_one(article_data)
        sys.stdout.write(" Done!\n")
        found_articles = list(articles.find({"title": article_title}))
    return found_articles[0]


def collect_articles(article_titles, return_dict=False, min_length=300):
    """Collect articles longer than min_length words."""
    docs = []
    wiki_wiki = wikipediaapi.Wikipedia(
        language="en", extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    for article_title in article_titles:
        article = fetch_article(article_title, wiki_wiki)
        if not article:
            continue
        if len(article["text"]) >= min_length:
            if return_dict:
                docs.append(article)
            else:
                docs.append(article["text"])
        else:
            continue
    return docs


def main():
    """Scrape all unique articles to MongoDB"""
    with open("../data/unique_articles.pkl", "rb") as f:
        article_titles = pickle.load(f)
    collect_articles(article_titles)


if __name__ == "__main__":
    main()
