import subprocess
import time
import os


def awaitFacetime():
    await_start_time = time.time()
    while True:
        time.sleep(1) 
        facetimeIsRunning = subprocess.run(['pgrep', '-x', 'FaceTime'], capture_output=True).returncode == 0

        if facetimeIsRunning:
            subprocess.run(['open', '-a', 'Safari'])           
            subprocess.run(['osascript', '-e', perplexityStartScript])
            time.sleep(5)

        else:
            elapsed_time = time.time() - await_start_time
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            print(f"FaceTime is not running. Script uptime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.")

        facetimeIsRunning = subprocess.run(['pgrep', '-x', 'FaceTime'], capture_output=True).returncode == 0
        
        if facetimeIsRunning:
            subprocess.run(['osascript', '-e', answerCallScript])
            print("FaceTime call answered.")
            awaitCallEnd()



def awaitCallEnd():
    call_start_time = time.time()
    while True:
        time.sleep(5) 
        facetimeIsRunning = subprocess.run(['pgrep', '-x', 'FaceTime'], capture_output=True).returncode == 0
        if facetimeIsRunning:
            elapsed_time = time.time() - call_start_time   
            print(f"FaceTime has been running for {elapsed_time:.2f} seconds.")
            if elapsed_time > 1800:
                print("FaceTime has been running for more than 30 minutes. Exiting script.")
                os.system("pkill -i 'safari'")
                os.system("pkill -i 'facetime'")
                break
        else:
            print("FaceTime is not running. Exiting script.")
            os.system("pkill -i 'safari'")
            os.system("pkill -i 'facetime'")
            break



answerCallScript = '''
tell application "System Events"
    -- First, try to activate FaceTime application
    try
        tell application "FaceTime" to activate
        delay 1
        -- Press space key (key code 49)
        key code 49
        key code 49
        key code 49
        key code 49
    on error
        display dialog "FaceTime is not running or not accessible" buttons {"OK"} default button "OK"
    end try
end tell
'''

perplexityStartScript = '''
                tell application "Safari"
                    activate
                    tell window 1
                        set current tab to (make new tab with properties {URL:"https://www.perplexity.ai"})
                        delay 3
                        do JavaScript "document.querySelector('button[aria-label*=Voice]').click();" in current tab
                    end tell
                end tell
                '''
os.system("pkill -i 'safari'")
os.system("pkill -i 'facetime'")
awaitFacetime()






    




