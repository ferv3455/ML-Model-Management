
class Service:
    count = 0

    def __init__(self, model):
        self.model = model
        self.status = True          # True for ON, False for OFF
        self.id = type(self).count
        type(self).count += 1

    def predict(data):
        return 0

    def beginBatch(data):
        return -1                    # task id


class ServiceList:
    def __init__(self):
        self.services = dict()      # Mapping Service ID to Service object
