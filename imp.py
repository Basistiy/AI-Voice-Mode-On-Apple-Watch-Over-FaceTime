import sqlite3
import os
import datetime
import time
import subprocess
import phonenumbers


shortcut_name = "FaceTime"  # Replace with your actual shortcut name

# Path to CallHistory database
db_path = os.path.expanduser('~/Library/Application Support/CallHistoryDB/CallHistory.storedata')

# Ensure the database exists
if not os.path.exists(db_path):
    print("Call history database not found. Make sure FaceTime has been used and you have access.")
    exit(1)

def create_contact(name, email=None, phone=None, email_label="work", phone_label="mobile"):
    """
    Create a contact in macOS Contacts app with email and optional phone number.
    
    Args:
        name (str): Contact's name
        email (str): Contact's email address
        phone (str, optional): Contact's phone number
        email_label (str): Label for email (default: "work")
        phone_label (str): Label for phone (default: "work")
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Base AppleScript command
    applescript_cmd = f'''
    tell application "Contacts"
        make new person with properties {{first name:"{name}"}}
        set thePerson to the result
    '''
    
    # Add phone number if provided
    if phone:
        applescript_cmd += f'''
        make new phone at end of phones of thePerson with properties {{label:"{phone_label}", value:"{phone}"}}
    '''
        
     # Add email if provided
    if email:
        applescript_cmd += f'''
        make new email at end of emails of thePerson with properties {{label:"{email_label}", value:"{email}"}}
    '''
    
    # Close the AppleScript
    applescript_cmd += '''
        save addressbook
    end tell
    '''
    
    try:
        subprocess.run(['osascript', '-e', applescript_cmd], 
                      capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating contact: {e.stderr}")
        return False
    
def is_email(string):
    return '@' in string and '.' in string.split('@')[-1]

def contact_exists(name):
    """
    Check if a contact already exists by name.
    
    Args:
        name (str): Contact's name to search for
    
    Returns:
        bool: True if contact exists, False otherwise
    """
    search_by_name = f'''
    tell application "Contacts"
        set foundPeople to (every person whose name contains "{name}")
        return count of foundPeople
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', search_by_name], 
                               capture_output=True, text=True, check=True)
        return int(result.stdout.strip()) > 0
    except (subprocess.CalledProcessError, ValueError):
        # If there's an error, assume contact doesn't exist
        return False



# SQL query to fetch last FaceTime call (both audio and video)
query = """
SELECT
    ZADDRESS AS contact,
    ZDATE + 978307200 AS timestamp,
    ZDURATION AS duration,
    ZORIGINATED AS originated,
    ZCALLTYPE AS call_type
FROM ZCALLRECORD
WHERE ZORIGINATED = 0
ORDER BY ZDATE DESC
LIMIT 1;
"""
while True:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    time.sleep(5)   
    try:
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            time_from_last_call = time.time() - result[1] 
            timestamp = datetime.datetime.fromtimestamp(result[1])
            print(f"  Last call: {time_from_last_call} from {result[0]}")
            if time_from_last_call <5:
                os.system("pkill -i 'safari'")
                os.system("pkill -i 'facetime'")
                if is_email(result[0]):
                        with open('contact.txt', 'w') as file:
                            print(result[0], file=file)
                        if not contact_exists(result[0]):
                            create_contact(result[0], result[0])
                        result = subprocess.run(["shortcuts", "run", "MailCall"], capture_output=True, text=True)                       
                else:
                        phone_number = phonenumbers.parse(result[0], None)
                        formatted_phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                        if not contact_exists(formatted_phone):
                            create_contact(formatted_phone, None, formatted_phone)
                        with open('contact.txt', 'w') as file:
                            print(formatted_phone, file=file)
                        result = subprocess.run(["shortcuts", "run", "NumberCall"], capture_output=True, text=True)

                subprocess.run(['open', '-a', 'Safari'])

                applescript = '''
                tell application "Safari"
                    activate
                    tell window 1
                        set current tab to (make new tab with properties {URL:"https://www.perplexity.ai"})
                        delay 2
                        do JavaScript "document.querySelector('button[aria-label*=Voice]').click();" in current tab
                    end tell
                end tell
                '''

                subprocess.run(['osascript', '-e', applescript])                      
                                  
        else:
            print("No FaceTime calls found.")

    except sqlite3.Error as e:
        print(f"Error accessing the database: {e}")

    finally:
        conn.close()


