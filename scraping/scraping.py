def collect_articles():
    docs2_long_text = []
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI) 
    for i in range(len(all_articles_unique)):
        temp = wiki_wiki.page(all_articles_unique[i])
        if len(temp.text) > 300:
            docs2_long_text.append(temp.text)
        else: 
            continue
    return docs2_long_text