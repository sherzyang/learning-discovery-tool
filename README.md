# Text Ascent
A tool to upskill with friends

[Presentation of Text Ascent, PDF](text_ascent_presentation.pdf)

### Background
<p> I've often found myself reading an article, say on data science, and wondering, where can I read something simpler on this topic? I realized I wasn't the only one when a friend posted a similar question on LinkedIn. She asked how to find articles in a specific range between most simple and most complex. I realized we don't have an easy system for that type of search besides manually reading for a good fit.
</p>
<p>
Building on my interests in web search, I created Text Ascent, a web app that uses unsupervised ML to help users discover content based on text complexity. I hope Text Ascent can be one tool used to address searching for content along all the stages of our learning journeys. Central to the goals I have for Text App is for it to make niche topics of interest between people more accessible.
</p>

![traverse image](traverse_flask/static/img/ted-bryan-yu-5mezpWin6T8-unsplash.jpg)
Photo Credit: Ted Bryan Yu, Unsplash

### Data Understanding
I used [Wikipedia-API](https://pypi.org/project/Wikipedia-API/), a python wrapper for [Wikipedia](https://www.wikipedia.org/)'s API to gather article titles on topics ranging from art to science. Then I ran a data gathering function (scrape_to_mongodb.py) that took those titles and scraped 11k+ articles for summaries, full text, and urls into a MongoDB database. I excluded articles that had full text less than 300 words because there are entries in Wikipedia like 'music file' that did not serve my model's purpose.

[Data Collection Notebook](collect_data.ipynb) & [Data Exploration Notebook](data_exploration.ipynb)

### Data Preparation
I graded the full text of each document using the [textstat package](https://pypi.org/project/textstat/)'s Flesch-Kincaid Grade. 

These files are saved in an AWS S3 bucket to allow make the web app accessible.   

[Data Preparation Notebook](data_preparation.ipynb)

### Modeling

#### Reproduce this model: 
* Get a list of documents of interest and format into a dataframe like ```clean_df```. Get text difficulty scores using TextStat.
*My example on AWS S3: [clean_df](https://text-ascent.s3-us-west-2.amazonaws.com/clean_df.pkl)*
* Fit your corpus to your vectorizer (learns vocabulary and idf from training set), which is the text series in your df 
*My example on AWS S3: [vectorizer](https://text-ascent.s3-us-west-2.amazonaws.com/vectorizer.pkl)*
* Use a vectorizer transform function (transforms documents to document-term matrix) to create your corpus vectors
*My example on AWS S3: [corpus vectors](https://text-ascent.s3-us-west-2.amazonaws.com/corpus_vectors.pkl)*
* Implement the flask app by running flask in ```traverse_flask``` in the terminal with ```$ export FLASK_APP=app $ flask run ``` . This flask ```app.py``` takes in functions from ```functions.py```. Adjust the functions to change the data pipeline on the backend. Adjust the brython in the ```static/templates/index.html``` to change the way data is reflected to the user. 

[Modeling Notebook]()

### Evaluation
This product is successful if users are able to discover content related to what they were already reading that is of a different reading difficulty. User satisfaction, repeat usage, web app traffic, and sharing of the app are the metrics I am using to evaluate Text Ascent's success. I evaluated 4 models before going with the model deployed on the web app: 

* Model 1: Used TextStat, Gensim, and Spacy. 
* Model 2: Used Latent Dirichlet Allocation (LDA) topic modeling with 10 topics, then sorts user content into a topic. 
* Model 3: Used TextStat and TF-IDF Vectorizer with 2000 dimensions. 
* Model 4: Used TextStat and TF-IDF Vectorizer with top 20 features.

Each iteration was done to so the resulting content was more similar to the user input content.

Future Modeling: I would also like to compare a pre-trained neural network to my current TFIDF Vectorization to see if the quality of returned content improves. Improvement would be measured through user feedback in a simple manual grading system to be added to the web app.

[Evaluation Notebook]()

### Deployment 
Text Ascent has been deployed as a flask-enabled web app [traverse.sherzyang.com](https://traverse.sherzyang.com) on an EC2 instance. The app uses brython to interact between python functions and html. 

As part of my interests in search and our [new world of one-shot answers](https://www.wired.com/story/amazon-alexa-search-for-the-one-perfect-answer/)--thank you Alexa, Siri and Google Home--I plan on deploying Text Ascent as an Amazon Alexa skill. The skill will allow a user to "scroll" or "traverse" along a gradient of simpler to more complex summaries on a topic just like telling Alexa to play a song louder or softer. I believe creating options in content will expand us beyond the world of one-shot answers in a positive way. 

Additionally, I am eager to grow the corpus to include books from Project Guttenberg and beyond. If you have some content you'd like to see added to the current library of wikipedia articles please send me a message on [LinkedIn](www.linkedin.com/in/sherzyang). I've seen several web extensions that grade a book's reading difficulty on Amazon or Goodreads ([Read Up](http://www.arialvetica.com/readup/) is a great one). Those products inspire me to develop a corpus-free search functionality for Text Ascent in the future. I envision Text Ascent becoming much more useful when it can return Google or Bing web search API enabled content.   

### Credits
* [Werlindo Mangrobang, Visualization and Web App Deployment](https://towardsdatascience.com/plotly-express-yourself-98366e35ad0f) 
* [Kayli Leung, Brython](https://github.com/kayschulz/travel_destination_recommendation/blob/master/travel_destination_recommendation/recommend.py)
