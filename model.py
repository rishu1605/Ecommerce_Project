class Product:
    def _init_(self, pid, name, price, category):
        self.pid = pid
        self.name = name
        self.price = price
        self.category = category

class Complaint:
    def _init_(self, cid, user, message, priority):
        self.cid = cid
        self.user = user
        self.message = message
        self.priority = priority  # 1: High, 2: Medium, 3: Low
        self.status = "Pending"