#Actual App for stock bud
import Presentation
import Logic
from Presentation.Display import Display
from Logic.NewsHelper import NewsHelper

done=False
#To support dependency injections
DISPLAY=Display()
newsHelper=NewsHelper()

#Extracting news from a specific main page
def extractNewsFromMainPage(url):
    newsHelper.extractNewsFromMainPage(url)
    
    

while not done:
    DISPLAY.welcome()
    DISPLAY.setUser()
    DISPLAY.praise()
    # openAiKey=DISPLAY.getOpenAIKey()
    openAiKey="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"
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
        newsList=newsHelper.extractNewsFromMainPage(url)
        
        if newsList is None:
            DISPLAY.printMessage("Something went wrong")
            continue
        else:
            DISPLAY.printMessage("News extracted successfully.")
        
        
        DISPLAY.printMessage("Printing last news...")
        newsHelper.printAllNews()
        DISPLAY.printMessage("News printed successfully.")
        
        
    if answer == "2":
        url=input("Enter the url of the article\n")
        newsExtracted=newsHelper.extractNews(url)
        
        if newsExtracted is None:
            DISPLAY.printMessage("Something went wrong")
            continue
        else:
            DISPLAY.printMessage("News extracted successfully.")
            DISPLAY.printMessage("Printing News...")
            newsHelper.printLastNews()
            DISPLAY.printMessage("News printed successfully.")
        
        
    
        
        
    
    
    
    