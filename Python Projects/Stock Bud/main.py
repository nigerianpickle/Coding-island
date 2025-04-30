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
    
#Get multiple urls from the user and extract news from them
def getMultipleUrls():
    #Get the urls
    urls=[]
    
    done=False
    
    while not done:
        url=input("Enter the url of the article\n")
        urls.append(url)
        
        #Ask if the user wants to add more urls
        answer=input("Do you want to add more urls? (y/n)\n")
        
        if answer.lower() == "n":
            done=True
        elif answer.lower() == "y":
            continue
        
    return urls


def deleteAllNews(): 
    DISPLAY.printMessage("Deleting all news...")
    newsHelper.deleteAllNews()
    DISPLAY.printMessage("All news deleted successfully.")
    

    
    
    

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
            
            
    if answer == "3":
        urls=getMultipleUrls()
        newsList=newsHelper.extractMultipleNews(urls)
        
        print(len(newsList))        
        for news in newsList:
            # if news is None:
            #     DISPLAY.printMessage("Something went wrong")
            #     continue
            #else:
                DISPLAY.printMessage("News extracted successfully.")
                DISPLAY.printMessage("Printing News...")
                newsHelper.printAllNews()
                DISPLAY.printMessage("News printed successfully.")
    
    
    if answer == "q":
        DISPLAY.goodBye()
        done=True
        #Delete all news
        deleteAllNews()
                
    deleteAllNews()
        
        
        
    
        
        
    
    
    
    