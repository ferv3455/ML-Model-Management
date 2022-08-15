from traceback import print_exc
from numpy import array

from celery import Celery
from model import Model

app = Celery('task', backend='redis://localhost:6379/1',
             broker='redis://localhost:6379/2')


@app.task
def predict(modelID, type, data, pre_processer=None):
    for key, value in data.items():
        try:
            # convert back to ndarray if it is a list
            if isinstance(value, list):
                data[key] = array(value, dtype='uint8')
                print(data[key].shape, data[key].dtype)
        except:
            print_exc()

    model = Model('name', 'des', type, './models/{}.{}'.format(modelID, type))
    return model.predict(data, pre_processer)


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
