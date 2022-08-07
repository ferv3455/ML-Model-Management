
class Service:
    def __init__(self, serviceID, model):
        self.model = model
        self.status = True          # True for ON, False for OFF
        self.id = serviceID

    def changeStatus(self, cmd):
        if cmd == 'start':
            self.status = True
        elif cmd == 'pause':
            self.status = False

    def predict(self, data):
        return self.model.predict(data)

    def batch(self, data):
        return -1                    # TODO: return task id

    def getResult(self, taskID):
        return None                  # TODO: return task result (from json file)


class ServiceList:
    def __init__(self):
        self.services = dict()      # Mapping Service ID to Service object

    def get(self, serviceID):
        return self.services.get(serviceID)

    def add(self, serviceID, service):
        self.services[serviceID] = service

    def delete(self, serviceID):
        if serviceID in self.services:
            del self.services[serviceID]
