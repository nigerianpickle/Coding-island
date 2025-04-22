#Actual App for stock bud
from Display import Display 
from NewsHelper import NewsHelper

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
    
    
    
    
    
    
    



    
    
    
    