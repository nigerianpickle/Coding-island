import random


APP_NAME="Stock Bud"
#Deafault display is a command line app

praises=("Nice!","Perfect!","Lemme see..","Wonderful")
class Display:
    def __init__(self):
        self.user=None
        pass
    
    
    def praise(self):
        
        #Added [0] because random.choices returns a list of one element
        #This is a workaround for the fact that random.choice returns a single element, not a list
        print(random.choices(praises)[0])
    
    def setUser(self):
        user=input("Enter your user name")
        try:
            self.user = str(user)
        except Exception as e:
            print(f"An error occurred: {e}")
            
            
    def getOpenAIKey(self):
        print("In order to get started, you would need to have an openaiAPI key[A future revision is coming that would allow users to use mine]")
        key=input("Enter you openAI api key\n If you are unsure, checkout this link for how to get started!\nhttps://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key")
        return key
            
    
    def welcome(self):
        print("="*80)
        print("Welcome to"+ APP_NAME+"!")
        
    def printOptions(self):
        print("1. See summarized news from articles of main page [WARNING]\n2. See summarized news from a specific article\n3. See summarized news for multiple custom urls")
        
        
    def printMessage(self,message):
        print(message)
    
    def goodBye(self):
        print("Thanks for using "+ APP_NAME+ " " + self.user+"!")
        
    
    