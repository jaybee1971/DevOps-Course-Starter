from flask_login import UserMixin

class todo_user(UserMixin):
    def __init__(self, gh_user):
        self.id = gh_user['id']
        self.login = gh_user['login']
        self.role = self.get_role(self.login)
    
    def get_role(self, login):
        if login == "jaybee1971":
            role = "writer"
        else:
            role = "reader"
        return role
            