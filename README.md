# AI Voice Mode On Apple Watch Over FaceTime
This is a script that can be used to initiate calls between two facetime accounts from mac to enable voice mode assistants on apple watch

##Setup:
Create a new user with a new iCloud address.
Make sure that you can access https://www.perplexity.ai and use voice mode in Safari.
Download LoopBack for mac and create new virtual devices:
FaceTime: Pass-Thru -> Channels 1 & 2
Safari: Safari -> Channels 1 & 2

Select Safari device as your microphone for FaceTime application.
Select Facetime as your output device instead of speakers.

Download the script to a folder on your mac.
Start the script: python3 imp.py
In Accessibility settings of your Mac enable "Full Keyboard Access"

##Usage:
Call your mac using your the iCloud address of the new user you created. Your mac should take the call and you can start interacting with your voice assistant.
