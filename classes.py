class todoStatus:

    def __init__(self, trelloId, status):
        self.trelloId = trelloId
        self.status = status
        
    def __str__(self):
        return "({0}, {1})".format(self.trelloId, self.status)


class todoItem:

    def __init__(self, trelloId, id, title, status):
        self.trelloId = trelloId
        self.id = id
        self.title = title
        self.status = status
        