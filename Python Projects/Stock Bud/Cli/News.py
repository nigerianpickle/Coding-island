class News:
    
    #First constructor: Wjithout data
    def __init__(self, title, description, date, source):
        self.title = title
        self.description = description
        self.date = date
        self.source = source
        self.data = None
        
        
    #Second constructor: With data
    def __init__(self, title, description, date, source,data):
        self.title = title
        self.description = description
        self.date = date
        self.source = source
        self.data = data
        
    
    #Getters
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_date(self):
        return self.date
    
    def get_source(self):
        return self.source
    
    def set_data(self, data):
        self.data = data
        
        
        
    def __str__(self):
        return f"Title:{self.title}\nDescription: {self.description}\nDate: {self.date}\nSource: {self.source}\nData:{self.data}"
    
    


