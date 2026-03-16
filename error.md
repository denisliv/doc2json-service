celery-worker-1  | [2026-03-16 18:23:10,453: ERROR/MainProcess] Received unregistered task of type 'app.processing.tasks.process_job'.
celery-worker-1  | The message has been ignored and discarded.                                                                                                                           
celery-worker-1  |                                                                                                                                                                       
celery-worker-1  | Did you remember to import the module containing this task?                                                                                                           
celery-worker-1  | Or maybe you're using relative imports?                                                                                                                               
celery-worker-1  |                                                                                                                                                                       
celery-worker-1  | Please see                                                                                                                                                            
celery-worker-1  | https://docs.celeryq.dev/en/latest/internals/protocol.html                                                                                                            
celery-worker-1  | for more information.                                                                                                                                                 
celery-worker-1  |                                                                                                                                                                       
celery-worker-1  | The full contents of the message body was:                                                                                                                            
celery-worker-1  | b'[["dc60b196-3f68-4b87-9e22-2233c380cb02"], {}, {"callbacks": null, "errbacks": null, "chain": null, "chord": null}]' (115b)                                         
celery-worker-1  |                                                                                                                                                                       
celery-worker-1  | The full contents of the message headers:                                                                                                                             
celery-worker-1  | {'lang': 'py', 'task': 'app.processing.tasks.process_job', 'id': 'fabc9b83-1fe4-498a-8fe5-ac49915b914d', 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'group_index': None, 'retries': 0, 'timelimit': [None, None], 'root_id': 'fabc9b83-1fe4-498a-8fe5-ac49915b914d', 'parent_id': None, 'argsrepr': "('dc60b196-3f68-4b87-9e22-2233c380cb02',)", 'kwargsrepr': '{}', 'origin': 'gen10@eb6df5aa55ee', 'ignore_result': False, 'replaced_task_nesting': 0, 'stamped_headers': None, 'stamps': {}}
celery-worker-1  | 
celery-worker-1  | The delivery info for this task is:                                                                                                                                   
celery-worker-1  | {'exchange': '', 'routing_key': 'celery'}
celery-worker-1  | Traceback (most recent call last):
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/celery/worker/consumer/consumer.py", line 662, in on_task_received
celery-worker-1  |     strategy = strategies[type_]
celery-worker-1  |                ~~~~~~~~~~^^^^^^^
celery-worker-1  | KeyError: 'app.processing.tasks.process_job'

this._load is not a function