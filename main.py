#Space Apps 2022 Challenge : Team Northern Lights 

#import libraries
import os
import requests
import json


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
    items = os.listdir(path)
    print(items)
   # return processed_data


#Pass the data to NLTK 
#should make a list of topic key words found in each document,
#including the frequency with which those key words appear. 
#should summarize the document
def analyze_data(processed_data):
    pass
   # return summary, key_words


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
    process_data(id_folder_path)
