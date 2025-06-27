import argparse
import os
from dotenv import load_dotenv
import populartimes
from datetime import datetime
import pytz
import sys
from python_ntfy import NtfyClient


load_dotenv() 

GCP_API_KEY = os.getenv('GCP_API_KEY')
ANOMALY_THRESHOLD = float(os.getenv('THRESHOLD', 1.5)) # Default threshold is 1.5x
PLACE_ID =  os.getenv('PLACE_ID', "ChIJI6ACK7q2t4kRFcPtFhUuYhU") # Domino's Pizza, 2602 Columbia Pike, Arlington, VA
STATE_FILE = os.getenv('STATE_FILE', '.dominos_state') # File to store state, e.g. if a notification was sent
DEFAULT_NTFY_URL = "https://ntfy.sh"

def get_dominos_data():
    
    # Get current time for comparison
    data = populartimes.get_id(GCP_API_KEY, PLACE_ID)
    
    if "current_popularity" not in data.keys():
        print("Current popularity data is unavailable - Domino's is closed!")
        exit(0)
    
    return data

def get_previous_state():
    if not os.path.exists(STATE_FILE):
        return None
    
    with open(STATE_FILE, 'r') as f:
        state = f.read().strip()
    
    return state

def set_current_state(state):
    with open(STATE_FILE, 'w') as f:
        f.write(state)
    print(f"State set to: {state}")

def main():
    
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument("-u", "--url", help="URL for the ntfy server. Default is \"https://ntfy.sh\"")
    parser.add_argument("-t", "--topic", help="Topic the notification will be published to. Default is \"pentagon\"")
    args = parser.parse_args()
    ntfy_url = args.url if args.url else DEFAULT_NTFY_URL
    ntfy_topic = args.topic if args.topic else "pentagon"
        
    if not GCP_API_KEY:
        print("GCP_API_KEY is not set - add it to your .env file or .[ba|z|k]shrc config")
        exit(1)
        
    # Get time in Virginia
    current_time = datetime.now(pytz.timezone('America/New_York')) # Use America/New_York for VA
    weekday = current_time.weekday()
    current_day_str = current_time.strftime('%A')  
    current_hour = current_time.hour
    print(f"Current time at the Pentagon: " +
          f"{current_hour % 12}{'PM' if current_hour >= 12 else 'AM'} on {current_day_str}")
    
    data = get_dominos_data()
        
    current_popularity = data["current_popularity"]
    regular_popularity = data["populartimes"][weekday]["data"][current_hour]
    
    if current_popularity / regular_popularity > ANOMALY_THRESHOLD:
        
        print("High activity detected!")
        
        if get_previous_state() != "NOTIFIED": # Only notify on activity rising edge
        
            print("Sending notification...")
            content = f"Massive spike in Domino's activity at " + \
            f"{current_hour % 12}{'PM' if current_hour >= 12 else 'AM'} by a factor of {current_popularity/regular_popularity:.1f}.\n" + \
            f"Current business is reading {current_popularity}, compared to average activity of {regular_popularity}.\n\n{'Shit is about to get variably real.' if current_popularity/regular_popularity > 2 else ''}"
            
            client = NtfyClient(server=ntfy_url, topic=ntfy_topic)
            client.send(content, 
                        "MASSIVE ACTIVITY DETECTED at the Pentagon Domino's",
                        priority=client.MessagePriority.URGENT, 
                        tags=["biohazard", "pizza"],
                        format_as_markdown=True)
            
        else:
            print("Notification already sent. Skipping until next rising edge...")
    else:
        set_current_state("")

    return
    
if __name__ == "__main__":
   main()
   