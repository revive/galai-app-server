import galai as gal

import json
import falcon
import threading, queue
from datetime import datetime
import uuid

class Answer:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.time = datetime.now()

class Model:
    def __init__(self, type='base'):
        self.model = gal.load_model(type, num_gpus=1)
        self.queue = queue.Queue()
        self.finished_jobs = {}

    def __del__(self):
        if self.worker is not None:
            self.worker.join()

    def worker_func(self):
        while True:
            item = self.queue.get()
            question = item[1]
            answer = self.model.generate(question)
            a = Answer(question=question, answer=answer)
            self.finished_jobs[item[0]] = a
            self.queue.task_done()

    def start(self):
        self.worker = threading.Thread(target=self.worker_func, daemon=True).start()
            
    async def on_post(self, req, resp):
        data = await req.get_media()
        print(data)
        if 'query' not in data:
            resp.text = json.dumps({'error': 'no query'})
            resp.status = falcon.HTTP_400
        else:
            id = uuid.uuid4()
            self.queue.put((id, data['query']))
            resp.text = json.dumps({'uuid': str(id)})
            resp.status = falcon.HTTP_200

    async def on_get_generate(self, req, resp, generate_id):
        # generate_id: in url
        if generate_id in self.finished_jobs:
            a = self.finished_jobs[generate_id]
            resp.text = json.dumps({'question': a.question, 'answer': a.answer})
            resp.status = falcon.HTTP_200
        else:
            resp.text = json.dumps({'status': 'waiting for processing...'})
            resp.status = falcon.HTTP_200
