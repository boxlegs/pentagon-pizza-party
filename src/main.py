import requests
import os
from dotenv import load_dotenv
import populartimes

load_dotenv() 

GCP_API_KEY = os.getenv('GCP_API_KEY')
NTFY_URL = os.getenv('NTFY_URL')

PLACE_ID = "ChIJI6ACK7q2t4kRFcPtFhUuYhU" # Domino's Pizza, 2602 Columbia Pike, Arlington, VA

def get_dominos_data():
    # Todo - add Freddie's Beach Bar
    data = populartimes.get_id(GCP_API_KEY, PLACE_ID)
    
    # Make sure we don't try and get current popularity data if it's not available (i.e. if the place is closed)
    print(data)
    
    
def publish_notification(content, title, priority, tags):
    
    req = requests.post(NTFY_URL+"/dominos",
    data=content,
    headers={
        "Title": title,
        "Priority": priority,
        "Tags": tags
    })
    
    

def notify():
    publish_notification(content="Remote access to phils-laptop detected. Act right away!", priority="urgent", title="Remote Access Detected", tags="warning,skull")
     

def main():
    get_dominos_data()
    notify()
    if not GCP_API_KEY:
        print("GCP_API_KEY is not set in the .env file.")
        exit(1)

    
if __name__ == "__main__":
   main()