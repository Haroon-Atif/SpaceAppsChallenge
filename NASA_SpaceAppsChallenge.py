#Space Apps 2022 Challenge : Team Northern Lights 

#import libraries
import os
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from wordcloud import WordCloud
import nltk
import heapq


#working path for the project 
path = os.path.expanduser('D:\\') + 'Projects/NASA SpaceAppsChallenge/'
id_folder_path = path + "id_data"


#Make RESTful Api requests and get the data
#then pass the data into folder 
def get_data(): 
    #Make POST request and store the result as a python dictionary
    param={"distribution": "PUBLIC",
           "center":[
               "CDMS"],
           "page":{
               "size": 1,
               "from": 0}
           }
    post_result = requests.post("https://ntrs.nasa.gov/api/citations/search", data=param).json()['results']
    

    #Get list of ids to pass to GET request
    id_list = [d['id'] for d in post_result]

    #Make directory for get reuests to download into if not exists
    
    if not os.path.exists(id_folder_path):
        os.makedirs(id_folder_path)
    #Make GET requests and download files 
    for id in id_list:
        get_result = requests.get("https://ntrs.nasa.gov/api/citations/{}/downloads/{}.txt".format(id,id),allow_redirects=True)
        if get_result.ok == True:
            with open('id_data/{}.txt'.format(id), 'wb') as f:
                f.write(get_result.content)

#Read the files from the folder and put the data into a format
#that NLTK reads easily 
def process_data(path):
    nltk.download("stopwords")
    nltk.download("punkt")

    items = os.listdir(path)
    for item in items:
        with open(path+'/'+item, 'r') as f:
           article_text = f.read()
        article_text = re.sub(r'\[0-9]*\ ', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        formatted_article_text = re.sub(r'[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        formatted_article_text = re.sub(r"\b[a-zA-Z]\b", "",article_text)

        sentence_list = nltk.sent_tokenize(article_text)

        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

  
        mod_data = {'Word': word_frequencies.keys(), 'Count': word_frequencies.values()}
        df = pd.DataFrame(data=mod_data)
        print(df)
   # return processed_data


#Pass the data to NLTK 
#should make a list of topic key words found in each document,
#including the frequency with which those key words appear. 
#should summarize the document
def analyze_data(processed_data):
    pass
   # return summary, key_words

def chart_data():
    #Data should be in the format {"word1": 23, word2: 234, word3: 32, word4: 76, word5: 98, word6: 38, word7: 65, word8: 83, word9: 75, word10: 45, word11: 12, word12: 12}
    test_data = {'word1': 23, 'word2': 234, 'word3': 32, 'word4': 76, 'word5': 98, 'word6': 38, 'word7': 65, 'word8': 83, 'word9': 75, 'word10': 45, 'word11': 12, 'word12': 12}

    mod_data = {'Word': test_data.keys(), 'Count': test_data.values()}
    df = pd.DataFrame(data=mod_data)
    
    g1 = sns.catplot(y="Count", x='Word', kind="bar", data=df)
    fig1 = g1.fig
    fig1.savefig('barplot.png')


    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=test_data)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("wordcloud.png")
    plt.show()

#Create PDF report of file keywords and summaries
#and the titles of the docs analyzed 
#include download links to the file 
def generate_report(filename, title, summaries, key_words):
    
#basic reports generator function
  #  styles = getSampleStyleSheet()
  #  report = SimpleDocTemplate(filename)
  #  report_title = Paragraph(title, styles["h1"])
  #  report_info = Paragraph(summaries, styles["BodyText"])
  #  empty_line = Spacer(1,20)
  #  report.build([report_title, empty_line, report_info])
    pass
   # return report


if __name__ ==  "__main__":
    #get_data()
    process_data(id_folder_path)
    #chart_data()
