
class Service:
    def __init__(self, model):
        self.model = model


class ServiceList:
    def __init__(self):
        self.services = dict()      # Mapping Service ID to Service object
