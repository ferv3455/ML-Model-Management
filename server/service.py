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
    def __init__(self, serviceID, model, modelID, pre_processer):
        self.id = serviceID
        self.model = model
        self.modelID = modelID
        self.pre_processer = pre_processer
        self.status = True          # True for ON, False for OFF
        self.tasks = dict()

        self.proc = Process(target=initWorker, args=(self.id,))
        self.proc.daemon = True
        self.proc.start()

        self.count = 0

    def predict(self, x):
        assert self.status
        return self.model.predict(x, self.pre_processer)

    def batch(self, x_gen):
        assert self.status
        self.count += 1
        taskID = self.count

        task_names = list()
        sub_tasks = list()
        for d in x_gen:
            tag, value, data = d
            task_names.append((tag, value))
            for key, value in data.items():
                try:
                    # convert to list if it is ndarray
                    data[key] = value.tolist()
                except:
                    pass

            sub_tasks.append(task.predict.apply_async(
                args=(self.modelID, self.model.type, data, self.pre_processer),
                queue='service{}'.format(self.id)))

        self.tasks[taskID] = (task_names, sub_tasks)
        return taskID

    def getResult(self, taskID):
        assert self.status
        task_names, sub_tasks = self.tasks[taskID]
        assert all(task.ready() for task in sub_tasks)
        return [{tag: value, 'result': task.get()}
                for (tag, value), task in zip(task_names, sub_tasks)]

    def getTaskStatus(self, taskID):
        _, sub_tasks = self.tasks[taskID]
        if all(t.ready() for t in sub_tasks):
            return 'finished'
        elif all(t.status == 'PENDING' for t in sub_tasks):
            return 'waiting'
        else:
            return 'running'

    def getTasks(self):
        return ({'id': i, 'status': self.getTaskStatus(i)} for i in self.tasks.keys())

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
