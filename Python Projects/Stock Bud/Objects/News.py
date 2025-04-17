class News:
    def __init__(self, title, description, date, source):
        self.title = title
        self.description = description
        self.date = date
        self.source = source
        
    def __str__(self):
        return f"Title:{self.title}\nDescription: {self.description}\nDate: {self.date}\nSource: {self.source}"
    
    


