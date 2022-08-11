from multiprocessing import Process

import task

'''
Using Celery to execute async tasks. Tasks and results are saved in MEMORY.
'''


def initWorker(serviceID):
    args = [
        'worker',
        '--loglevel=INFO',
        '-Q',
        'service{}'.format(serviceID),
        '--without-gossip',
        '--without-mingle',
        '--without-heartbeat',
        '-Ofair',
        '--purge'
    ]
    task.app.worker_main(argv=args)


class Service:
    def __init__(self, serviceID, model, modelID):
        self.id = serviceID
        self.model = model
        self.modelID = modelID
        self.status = True          # True for ON, False for OFF
        self.tasks = dict()

        self.proc = Process(target=initWorker, args=(self.id,))
        self.proc.daemon = True
        self.proc.start()

        self.count = 0

    def predict(self, data):
        assert self.status
        return self.model.predict(data)

    def batch(self, data):
        assert self.status
        self.count += 1
        taskID = self.count

        sub_tasks = list()
        for d in data:
            sub_tasks.append(task.predict.apply_async(
                args=(self.modelID, self.model.type, d), queue='service{}'.format(self.id)))

        self.tasks[taskID] = sub_tasks
        return taskID

    def getResult(self, taskID):
        assert self.status
        assert all(t.ready() for t in self.tasks[taskID])
        return [t.get() for t in self.tasks[taskID]]

    def getTaskStatus(self, taskID):
        if all(t.ready() for t in self.tasks[taskID]):
            return 'finished'
        elif all(t.status == 'PENDING' for t in self.tasks[taskID]):
            return 'waiting'
        else:
            return 'running'

    def getTasks(self):
        return ({'id': i, 'status': self.getTaskStatus(i)} for i, _ in self.tasks.items())

    def changeStatus(self, cmd):
        if cmd == 'start':
            self.status = True
        elif cmd == 'pause':
            self.status = False

    def close(self):
        self.proc.terminate()
        self.proc.join()
        self.proc.close()


class ServiceList:
    def __init__(self):
        self.services = dict()      # Mapping Service ID to Service object

    def get(self, serviceID):
        return self.services.get(serviceID)

    def add(self, serviceID, service):
        self.services[serviceID] = service

    def delete(self, serviceID):
        if serviceID in self.services:
            self.services[serviceID].close()
            del self.services[serviceID]
