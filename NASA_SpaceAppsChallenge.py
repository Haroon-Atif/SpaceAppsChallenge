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
               "CDMS"]}
    post_result = requests.post("https://ntrs.nasa.gov/api/citations/search", data=param).json()['results']
    
    abstracts = [d['abstract'] for d in post_result]
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
    return abstracts
#Read the files from the folder and put the data into a format
#that NLTK reads easily 
def process_data(items):
    nltk.download("stopwords")
    nltk.download("punkt")
    summary_list = []
    word_list = []
    for item in items:
        article_text = re.sub(r'[[0-9]*]', ' ', item)
        article_text = re.sub(r'\s+', ' ', article_text)

        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

        sentence_list = nltk.sent_tokenize(article_text)

        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

       

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        summary_list.append(summary)
        word_list.append(word_frequencies)

    return summary_list, word_list
   # return processed_data


#Pass the data to NLTK 
#should make a list of topic key words found in each document,
#including the frequency with which those key words appear. 
#should summarize the document
def analyze_data(processed_data):
    pass
   # return summary, key_words

def chart_data(word_data):
    #Data should be in the format {"word1": 23, word2: 234, word3: 32, word4: 76, word5: 98, word6: 38, word7: 65, word8: 83, word9: 75, word10: 45, word11: 12, word12: 12}
    # test_data = {'word1': 23, 'word2': 234, 'word3': 32, 'word4': 76, 'word5': 98, 'word6': 38, 'word7': 65, 'word8': 83, 'word9': 75, 'word10': 45, 'word11': 12, 'word12': 12}
    
    #mod_data = {'Word': test_data.keys(), 'Count': test_data.values()}
    #df = pd.DataFrame(data=mod_data)
    for i, v in enumerate(word_data):
        mod_data = {'Word': v.keys(), 'Count': v.values()}
        df = pd.DataFrame(data=mod_data)
    
        g1 = sns.catplot(y="Count", x='Word', kind="bar", data=df)
        fig1 = g1.fig
        fig1.savefig('barplot{}.png'.format(i))


        wordcloud = WordCloud()
        wordcloud.generate_from_frequencies(frequencies=v)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("wordcloud{}.png".format(i))
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
    data = get_data()
    summary, word_data = process_data(data)
    chart_data(word_data)

    
