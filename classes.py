class trello_list:

    def __init__(self, trelloId, name):
        self.trelloId = trelloId
        self.name = name


class trello_card:

    def __init__(self, trelloId, id, title, status):
        self.trelloId = trelloId
        self.id = id
        self.title = title
        self.status = status
        