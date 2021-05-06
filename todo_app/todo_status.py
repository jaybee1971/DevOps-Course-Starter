class todo_status:

    def __init__(self, mongo_id, status):
        self.mongo_id = mongo_id
        self.status = status
        
    def __str__(self):
        return "({0}, {1})".format(self.mongo_id, self.status)
