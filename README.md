# Text Ascent
## A tool to upskill with friends

### Business Understanding
I’m a generalist, and I want to gain some niche topic understanding but don’t know where to begin. Here is an application that can take in text about the arts and sciences and return a piece of text of simpler or more complex reading level to support your understanding of the existing content. I'd like to simplify the process of finding related content that is of different reading level so readers of all levels can access a topic. This is a tool that can be used in preparation for lifelong learning. We are traversing along the slopes of topics where there is no clearly defined path. Let’s create one! 

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

