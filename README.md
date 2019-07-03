# New reading discovery  
## Application that takes in text and returns a similar topic text of different reading difficulty based on user need

### Business Understanding
Imagine you are looking online for an article about watermelon. You come across an article that is about the basics of watermelon, but you actually want to share new information with your friend who already knows a lot about watermelon. You could go and manually read articles until you find one that is appropriate for your friend's reading level, but that would take some time. I'd like to simplify the process of finding related content that is of different reading level so readers of all levels can access a topic. 

### Data Understanding
I am accessing the Wikipedia API to gather 14,000 articles on topics ranging from art to science. 

### Data Preparation
I will be stemming and lemmatizing my text. I am scoring my corpus using textstat's Flesch-Kincaid Grade. 

### Modeling
I will be comparing a Latent Dirichlet Allocation topic modeling algorithm versus a TFIDF vectorizer to return similar topic text by reading level.

### Evaluation
I will use log-likelihood ratio to score this model. 

### Deployment 
This application will live as a flask enabled webpage. In the next iteration, I will deploy a version as a chrome extension. 

