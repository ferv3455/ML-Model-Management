from celery import Celery
from model import Model

app = Celery('task', backend='redis://localhost:6379/1',
             broker='redis://localhost:6379/2')


@app.task
def predict(modelID, type, data):
    model = Model('name', 'des', type, './models/{}.{}'.format(modelID, type))
    return model.predict(data)


'''
>>> res = mul.apply_async(args=(3, 5), queue='service1')
>>> res.ready()
True
>>> res.get()
15
>>> mul.apply_async(args=[1, 2], queue='service1') 
<AsyncResult: 51d86f25-7db8-4b5d-bc6a-b81faa516562>
'''

if __name__ == '__main__':
    args = [
        'worker',
        '--loglevel=INFO',
        '-Q',
        'service1',
        '--without-gossip',
        '--without-mingle',
        '--without-heartbeat',
        '-Ofair',
        '--purge'
    ]
    app.worker_main(argv=args)
