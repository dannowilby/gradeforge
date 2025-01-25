import atexit
from multiprocessing import Process, Queue
import os

from waitress import serve

from .app import app
from .generator import run

if __name__ == '__main__':

    port = os.environ['PORT'] or 5000

    queue = Queue()
    
    generator = Process(target=run, args=(queue,))
    generator.start()

    atexit.register(lambda: queue.put(None)) # send kill signal
    serve(app(queue), host='0.0.0.0', port=port)