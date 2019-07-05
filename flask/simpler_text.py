import textstat
import operator
import wikipedia
import wikipediaapi

def give_simpler_level(text):
    """
    Takes in text and returns an easier level read
    """
    ##find all the articles that are easier than this article 
    all_simpler_text = []
    input_score = textstat.flesch_kincaid_grade(text)
    for i in range(len(df_corpus2['score'])):
        if df_corpus2['score'][i] < input_score:
            all_simpler_text.append(df_corpus2['content'][i])
    
    vec = TfidfVectorizer(stop_words='english', max_features=2000)
    vec = vec.fit(all_simpler_text)
    corpus2_vectors = vec.transform(all_simpler_text).toarray()
    user_doc = text
    user_doc_vector = vec.transform([user_doc]).toarray()    
    distances = cdist(user_doc_vector,
                  corpus2_vectors,
                  metric='cosine')[0]
    ranking = np.argsort(distances)
    top = ranking[0]
    best_match = df_corpus2['content'][top]
        
    print(distances[top])
    return (best_match)