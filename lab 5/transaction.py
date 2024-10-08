class Transaction:
    def __init__(self, name, resources):
        self.name = name
        self.resources = resources
        self.waiting_for = None
