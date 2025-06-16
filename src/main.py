import requests
import os
from dotenv import load_dotenv

load_dotenv() 

GCP_API_KEY = os.getenv('GCP_API_KEY')
NTFY_URL = os.getenv('NTFY_URL')

def get_dominos_data():
    pass

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
    notify()
    if not GCP_API_KEY:
        print("GCP_API_KEY is not set in the .env file.")
        exit(1)

    
if __name__ == "__main__":
   main()