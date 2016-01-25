class User:
    def __init__(self,accountId,map):
        self.accountId = accountId
        self.name = map.get("username","")