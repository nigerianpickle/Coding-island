#Actual App for stock bud

from Presentation import Display
from Logic import NewsHelper

done=False
#To support dependency injections
DISPLAY=Display()
newsHelper=NewsHelper()

def extractNewsFromMainPage(url):
    newsHelper.extractNewsFromMainPage(url)
    
    

while not done:
    DISPLAY.welcome()
    DISPLAY.setUser()
    DISPLAY.praise()
    openAiKey=DISPLAY.getOpenAIKey()
    DISPLAY.praise()
     #setting the api key
    DISPLAY.printMessage("Setting the API key...")
    newsHelper.setAPIKey(openAiKey)
    DISPLAY.printMessage("API key set successfully.")
    
    
    #Main part
    DISPLAY.printOptions()
    
    answer=input("Enter your choice\n")
    
    
    if answer == "1":
        url=input("Enter the url of the main page\n")
        newsHelper.extractNewsFromMainPage(url)
        DISPLAY.printMessage("News extracted successfully.")
        
        
    
    
    
    