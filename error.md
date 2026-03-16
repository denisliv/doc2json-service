celery-worker-1  | [2026-03-16 18:38:17,948: ERROR/ForkPoolWorker-2] Job 4f2271d2-cf78-48b0-9669-473e82388542 failed: Foreign key associated with column 'jobs.created_by' could not find table 'users' with which to generate a foreign key to target column 'id'
celery-worker-1  | Traceback (most recent call last):
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 45, in _run_pipeline_async                                                                                        
celery-worker-1  |     await session.commit()                                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 1014, in commit                                                         
celery-worker-1  |     await greenlet_spawn(self.sync_session.commit)                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 203, in greenlet_spawn                                               
celery-worker-1  |     result = context.switch(value)                                                                                                                               
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^                                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2032, in commit                                                                 
celery-worker-1  |     trans.commit(_to_root=True)                                                                                                                                  
celery-worker-1  |   File "<string>", line 2, in commit                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go                                                               
celery-worker-1  |     ret_value = fn(self, *arg, **kw)                                                                                                                             
celery-worker-1  |                 ^^^^^^^^^^^^^^^^^^^^                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1313, in commit                                                                 
celery-worker-1  |     self._prepare_impl()                                                                                                                                         
celery-worker-1  |   File "<string>", line 2, in _prepare_impl                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go                                                               
celery-worker-1  |     ret_value = fn(self, *arg, **kw)                                                                                                                             
celery-worker-1  |                 ^^^^^^^^^^^^^^^^^^^^                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1288, in _prepare_impl                                                          
celery-worker-1  |     self.session.flush()                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4345, in flush                                                                  
celery-worker-1  |     self._flush(objects)                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4480, in _flush                                                                 
celery-worker-1  |     with util.safe_reraise():                                                                                                                                    
celery-worker-1  |          ^^^^^^^^^^^^^^^^^^^                                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__                                                           
celery-worker-1  |     raise exc_value.with_traceback(exc_tb)                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4441, in _flush                                                                 
celery-worker-1  |     flush_context.execute()                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 466, in execute                                                              
celery-worker-1  |     rec.execute(self)                                                                                                                                            
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 642, in execute                                                              
celery-worker-1  |     util.preloaded.orm_persistence.save_obj(                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/persistence.py", line 76, in save_obj                                                             
celery-worker-1  |     for table, mapper in base_mapper._sorted_tables.items():                                                                                                     
celery-worker-1  |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                              
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 1338, in __get__                                                           
celery-worker-1  |     obj.__dict__[self.__name__] = result = self.fget(obj)                                                                                                        
celery-worker-1  |                                            ^^^^^^^^^^^^^^                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/mapper.py", line 4060, in _sorted_tables                                                          
celery-worker-1  |     sorted_ = sql_util.sort_tables(                                                                                                                              
celery-worker-1  |               ^^^^^^^^^^^^^^^^^^^^^                                                                                                                              
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 1316, in sort_tables                                                                
celery-worker-1  |     for (t, fkcs) in sort_tables_and_constraints(                                                                                                                
celery-worker-1  |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 1386, in sort_tables_and_constraints                                                
celery-worker-1  |     filtered = filter_fn(fkc)                                                                                                                                    
celery-worker-1  |                ^^^^^^^^^^^^^^                                                                                                                                    
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 1306, in _skip_fn                                                                   
celery-worker-1  |     if fixed_skip_fn(fk):                                                                                                                                        
celery-worker-1  |        ^^^^^^^^^^^^^^^^^                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/mapper.py", line 4043, in skip                                                                    
celery-worker-1  |     dep = table_to_mapper.get(fk.column.table)                                                                                                                   
celery-worker-1  |                               ^^^^^^^^^                                                                                                                          
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 1226, in __get__                                                           
celery-worker-1  |     obj.__dict__[self.__name__] = result = self.fget(obj)                                                                                                        
celery-worker-1  |                                            ^^^^^^^^^^^^^^                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/schema.py", line 3199, in column                                                                  
celery-worker-1  |     return self._resolve_column()                                                                                                                                
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^                                                                                                                                
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/schema.py", line 3222, in _resolve_column                                                         
celery-worker-1  |     raise exc.NoReferencedTableError(                                                                                                                            
celery-worker-1  | sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'jobs.created_by' could not find table 'users' with which to generate a foreign key to target column 'id'                                                                                                                                                                  
celery-worker-1  | [2026-03-16 18:38:17,969: ERROR/ForkPoolWorker-2] Task process_job failed for job 4f2271d2-cf78-48b0-9669-473e82388542
celery-worker-1  | Traceback (most recent call last):                                                                                                                               
celery-worker-1  |   File "/app/app/processing/tasks.py", line 15, in process_job                                                                                                   
celery-worker-1  |     run_pipeline(job_id)                                                                                                                                         
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 27, in run_pipeline                                                                                               
celery-worker-1  |     asyncio.run(_run_pipeline_async(job_id))                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 195, in run                                                                                          
celery-worker-1  |     return runner.run(main)                                                                                                                                      
celery-worker-1  |            ^^^^^^^^^^^^^^^^                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 118, in run                                                                                          
celery-worker-1  |     return self._loop.run_until_complete(task)                                                                                                                   
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                   
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete                                                                       
celery-worker-1  |     return future.result()                                                                                                                                       
celery-worker-1  |            ^^^^^^^^^^^^^^^                                                                                                                                       
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 137, in _run_pipeline_async                                                                                       
celery-worker-1  |     await session.commit()                                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 1014, in commit                                                         
celery-worker-1  |     await greenlet_spawn(self.sync_session.commit)                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 190, in greenlet_spawn                                               
celery-worker-1  |     result = context.switch(*args, **kwargs)                                                                                                                     
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2032, in commit                                                                 
celery-worker-1  |     trans.commit(_to_root=True)                                                                                                                                  
celery-worker-1  |   File "<string>", line 2, in commit                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 103, in _go                                                               
celery-worker-1  |     self._raise_for_prerequisite_state(fn.__name__, current_state)                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 973, in _raise_for_prerequisite_state                                           
celery-worker-1  |     raise sa_exc.PendingRollbackError(
celery-worker-1  | sqlalchemy.exc.PendingRollbackError: This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: Foreign key associated with column 'jobs.created_by' could not find table 'users' with which to generate a foreign key to target column 'id' (Background on this error at: https://sqlalche.me/e/20/7s2a)
celery-worker-1  | [2026-03-16 18:38:17,985: INFO/MainProcess] Task app.processing.tasks.process_job[e2863348-26dc-45bc-83a0-d6fb6af1aa8a] received
celery-worker-1  | [2026-03-16 18:38:17,991: INFO/ForkPoolWorker-2] Task app.processing.tasks.process_job[e2863348-26dc-45bc-83a0-d6fb6af1aa8a] retry: Retry in 10s: PendingRollbackError("This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: Foreign key associated with column 'jobs.created_by' could not find table 'users' with which to generate a foreign key to target column 'id'")
backend-1        | INFO:     172.20.0.6:38452 - "GET /api/v1/documents/jobs?page=1&page_size=20 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:18 +0000] "GET /api/v1/documents/jobs?page=1&page_size=20 HTTP/1.1" 200 408 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"
backend-1        | INFO:     172.20.0.6:38460 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:19 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"                                                                             
backend-1        | INFO:     172.20.0.6:38470 - "GET /api/v1/documents/jobs?page=1&page_size=5 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:21 +0000] "GET /api/v1/documents/jobs?page=1&page_size=5 HTTP/1.1" 200 407 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"
backend-1        | INFO:     172.20.0.6:38484 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:22 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"
backend-1        | INFO:     172.20.0.6:38494 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:25 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"                                                                             
backend-1        | INFO:     172.20.0.6:38506 - "GET /api/v1/documents/jobs?page=1&page_size=20 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:25 +0000] "GET /api/v1/documents/jobs?page=1&page_size=20 HTTP/1.1" 200 408 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"
celery-worker-1  | [2026-03-16 18:38:27,983: ERROR/ForkPoolWorker-2] Exception terminating connection <AdaptedConnection <asyncpg.connection.Connection object at 0x7be5fba08320>>
celery-worker-1  | Traceback (most recent call last):
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 374, in _close_connection                                                         
celery-worker-1  |     self._dialect.do_terminate(connection)
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 1130, in do_terminate                                           
celery-worker-1  |     dbapi_connection.terminate()                                                                                                                                 
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 907, in terminate                                               
celery-worker-1  |     self.await_(asyncio.shield(self._connection.close(timeout=2)))                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only                                                   
celery-worker-1  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501                                                             
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn                                               
celery-worker-1  |     value = await result                                                                                                                                         
celery-worker-1  |             ^^^^^^^^^^^^                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/connection.py", line 1504, in close                                                                      
celery-worker-1  |     await self._protocol.close(timeout)                                                                                                                          
celery-worker-1  |   File "asyncpg/protocol/protocol.pyx", line 627, in close                                                                                                       
celery-worker-1  |   File "asyncpg/protocol/protocol.pyx", line 660, in asyncpg.protocol.protocol.BaseProtocol._request_cancel                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/connection.py", line 1673, in _cancel_current_command                                                    
celery-worker-1  |     self._cancellations.add(self._loop.create_task(self._cancel(waiter)))                                                                                        
celery-worker-1  |                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 455, in create_task                                                                              
celery-worker-1  |     self._check_closed()                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 545, in _check_closed                                                                            
celery-worker-1  |     raise RuntimeError('Event loop is closed')                                                                                                                   
celery-worker-1  | RuntimeError: Event loop is closed                                                                                                                               
celery-worker-1  | [2026-03-16 18:38:27,993: ERROR/ForkPoolWorker-2] Task process_job failed for job 4f2271d2-cf78-48b0-9669-473e82388542                                           
celery-worker-1  | Traceback (most recent call last):                                                                                                                               
celery-worker-1  |   File "/app/app/processing/tasks.py", line 15, in process_job                                                                                                   
celery-worker-1  |     run_pipeline(job_id)                                                                                                                                         
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 27, in run_pipeline                                                                                               
celery-worker-1  |     asyncio.run(_run_pipeline_async(job_id))                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 195, in run                                                                                          
celery-worker-1  |     return runner.run(main)                                                                                                                                      
celery-worker-1  |            ^^^^^^^^^^^^^^^^                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 118, in run                                                                                          
celery-worker-1  |     return self._loop.run_until_complete(task)                                                                                                                   
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                   
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete                                                                       
celery-worker-1  |     return future.result()                                                                                                                                       
celery-worker-1  |            ^^^^^^^^^^^^^^^                                                                                                                                       
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 34, in _run_pipeline_async                                                                                        
celery-worker-1  |     result = await session.execute(                                                                                                                              
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^                                                                                                                              
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 463, in execute                                                         
celery-worker-1  |     result = await greenlet_spawn(                                                                                                                               
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^                                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn                                               
celery-worker-1  |     result = context.throw(*sys.exc_info())                                                                                                                      
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2365, in execute                                                                
celery-worker-1  |     return self._execute_internal(
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal                                                      
celery-worker-1  |     conn = self._connection_for_bind(bind)                                                                                                                       
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind                                                   
celery-worker-1  |     return trans._connection_for_bind(engine, execution_options)                                                                                                 
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                 
celery-worker-1  |   File "<string>", line 2, in _connection_for_bind                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go                                                               
celery-worker-1  |     ret_value = fn(self, *arg, **kw)                                                                                                                             
celery-worker-1  |                 ^^^^^^^^^^^^^^^^^^^^                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind                                                   
celery-worker-1  |     conn = bind.connect()                                                                                                                                        
celery-worker-1  |            ^^^^^^^^^^^^^^                                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3273, in connect                                                                
celery-worker-1  |     return self._connection_cls(self)                                                                                                                            
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                            
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 145, in __init__                                                                
celery-worker-1  |     self._dbapi_connection = engine.raw_connection()                                                                                                             
celery-worker-1  |                              ^^^^^^^^^^^^^^^^^^^^^^^                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3297, in raw_connection                                                         
celery-worker-1  |     return self.pool.connect()                                                                                                                                   
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^                                                                                                                                   
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 449, in connect                                                                   
celery-worker-1  |     return _ConnectionFairy._checkout(self)                                                                                                                      
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1363, in _checkout                                                                
celery-worker-1  |     with util.safe_reraise():                                                                                                                                    
celery-worker-1  |          ^^^^^^^^^^^^^^^^^^^                                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__                                                           
celery-worker-1  |     raise exc_value.with_traceback(exc_tb)                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1301, in _checkout                                                                
celery-worker-1  |     result = pool._dialect._do_ping_w_event(                                                                                                                     
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 720, in _do_ping_w_event                                                     
celery-worker-1  |     return self.do_ping(dbapi_connection)                                                                                                                        
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 1163, in do_ping                                                
celery-worker-1  |     dbapi_connection.ping()                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 813, in ping                                                    
celery-worker-1  |     self._handle_exception(error)                                                                                                                                
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 794, in _handle_exception                                       
celery-worker-1  |     raise error                                                                                                                                                  
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 811, in ping                                                    
celery-worker-1  |     _ = self.await_(self._async_ping())                                                                                                                          
celery-worker-1  |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                          
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only                                                   
celery-worker-1  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501                                                             
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn                                               
celery-worker-1  |     value = await result                                                                                                                                         
celery-worker-1  |             ^^^^^^^^^^^^                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 820, in _async_ping                                             
celery-worker-1  |     await tr.start()                                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/transaction.py", line 146, in start                                                                      
celery-worker-1  |     await self._connection.execute(query)                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/connection.py", line 349, in execute                                                                     
celery-worker-1  |     result = await self._protocol.query(query, timeout)                                                                                                          
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                          
celery-worker-1  |   File "asyncpg/protocol/protocol.pyx", line 375, in query                                                                                                       
celery-worker-1  | RuntimeError: Task <Task pending name='Task-5' coro=<_run_pipeline_async() running at /app/app/processing/pipeline.py:34> cb=[_run_until_complete_cb() at /usr/local/lib/python3.12/asyncio/base_events.py:181]> got Future <Future pending cb=[BaseProtocol._on_waiter_completed()]> attached to a different loop                                   
celery-worker-1  | [2026-03-16 18:38:28,009: INFO/MainProcess] Task app.processing.tasks.process_job[e2863348-26dc-45bc-83a0-d6fb6af1aa8a] received
celery-worker-1  | [2026-03-16 18:38:28,011: INFO/ForkPoolWorker-2] Task app.processing.tasks.process_job[e2863348-26dc-45bc-83a0-d6fb6af1aa8a] retry: Retry in 10s: RuntimeError("Task <Task pending name='Task-5' coro=<_run_pipeline_async() running at /app/app/processing/pipeline.py:34> cb=[_run_until_complete_cb() at /usr/local/lib/python3.12/asyncio/base_events.py:181]> got Future <Future pending cb=[BaseProtocol._on_waiter_completed()]> attached to a different loop")
backend-1        | INFO:     172.20.0.6:33006 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:28 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"                                                                             
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:31 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"
backend-1        | INFO:     172.20.0.6:33016 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK
backend-1        | INFO:     172.20.0.6:33020 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK                                                   
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:34 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"
celery-worker-1  | [2026-03-16 18:38:38,055: ERROR/ForkPoolWorker-2] Job 4f2271d2-cf78-48b0-9669-473e82388542 failed: Foreign key associated with column 'jobs.created_by' could not find table 'users' with which to generate a foreign key to target column 'id'
celery-worker-1  | Traceback (most recent call last):
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 45, in _run_pipeline_async                                                                                        
celery-worker-1  |     await session.commit()                                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 1014, in commit                                                         
celery-worker-1  |     await greenlet_spawn(self.sync_session.commit)                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 203, in greenlet_spawn                                               
celery-worker-1  |     result = context.switch(value)                                                                                                                               
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^                                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2032, in commit                                                                 
celery-worker-1  |     trans.commit(_to_root=True)                                                                                                                                  
celery-worker-1  |   File "<string>", line 2, in commit                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go                                                               
celery-worker-1  |     ret_value = fn(self, *arg, **kw)                                                                                                                             
celery-worker-1  |                 ^^^^^^^^^^^^^^^^^^^^                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1313, in commit                                                                 
celery-worker-1  |     self._prepare_impl()                                                                                                                                         
celery-worker-1  |   File "<string>", line 2, in _prepare_impl                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go                                                               
celery-worker-1  |     ret_value = fn(self, *arg, **kw)                                                                                                                             
celery-worker-1  |                 ^^^^^^^^^^^^^^^^^^^^                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1288, in _prepare_impl                                                          
celery-worker-1  |     self.session.flush()                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4345, in flush                                                                  
celery-worker-1  |     self._flush(objects)                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4480, in _flush                                                                 
celery-worker-1  |     with util.safe_reraise():                                                                                                                                    
celery-worker-1  |          ^^^^^^^^^^^^^^^^^^^                                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__                                                           
celery-worker-1  |     raise exc_value.with_traceback(exc_tb)                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 4441, in _flush                                                                 
celery-worker-1  |     flush_context.execute()                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 466, in execute                                                              
celery-worker-1  |     rec.execute(self)                                                                                                                                            
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/unitofwork.py", line 642, in execute                                                              
celery-worker-1  |     util.preloaded.orm_persistence.save_obj(                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/persistence.py", line 76, in save_obj                                                             
celery-worker-1  |     for table, mapper in base_mapper._sorted_tables.items():                                                                                                     
celery-worker-1  |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                              
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 1338, in __get__                                                           
celery-worker-1  |     obj.__dict__[self.__name__] = result = self.fget(obj)                                                                                                        
celery-worker-1  |                                            ^^^^^^^^^^^^^^                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/mapper.py", line 4060, in _sorted_tables                                                          
celery-worker-1  |     sorted_ = sql_util.sort_tables(                                                                                                                              
celery-worker-1  |               ^^^^^^^^^^^^^^^^^^^^^                                                                                                                              
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 1316, in sort_tables                                                                
celery-worker-1  |     for (t, fkcs) in sort_tables_and_constraints(                                                                                                                
celery-worker-1  |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 1386, in sort_tables_and_constraints                                                
celery-worker-1  |     filtered = filter_fn(fkc)                                                                                                                                    
celery-worker-1  |                ^^^^^^^^^^^^^^                                                                                                                                    
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 1306, in _skip_fn                                                                   
celery-worker-1  |     if fixed_skip_fn(fk):                                                                                                                                        
celery-worker-1  |        ^^^^^^^^^^^^^^^^^                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/mapper.py", line 4043, in skip                                                                    
celery-worker-1  |     dep = table_to_mapper.get(fk.column.table)                                                                                                                   
celery-worker-1  |                               ^^^^^^^^^                                                                                                                          
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 1226, in __get__                                                           
celery-worker-1  |     obj.__dict__[self.__name__] = result = self.fget(obj)                                                                                                        
celery-worker-1  |                                            ^^^^^^^^^^^^^^                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/schema.py", line 3199, in column                                                                  
celery-worker-1  |     return self._resolve_column()                                                                                                                                
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^                                                                                                                                
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/sql/schema.py", line 3222, in _resolve_column                                                         
celery-worker-1  |     raise exc.NoReferencedTableError(                                                                                                                            
celery-worker-1  | sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'jobs.created_by' could not find table 'users' with which to generate a foreign key to target column 'id'                                                                                                                                                                  
celery-worker-1  | [2026-03-16 18:38:38,057: ERROR/ForkPoolWorker-2] Task process_job failed for job 4f2271d2-cf78-48b0-9669-473e82388542
celery-worker-1  | Traceback (most recent call last):                                                                                                                               
celery-worker-1  |   File "/app/app/processing/tasks.py", line 15, in process_job                                                                                                   
celery-worker-1  |     run_pipeline(job_id)                                                                                                                                         
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 27, in run_pipeline                                                                                               
celery-worker-1  |     asyncio.run(_run_pipeline_async(job_id))                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 195, in run                                                                                          
celery-worker-1  |     return runner.run(main)                                                                                                                                      
celery-worker-1  |            ^^^^^^^^^^^^^^^^                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 118, in run                                                                                          
celery-worker-1  |     return self._loop.run_until_complete(task)                                                                                                                   
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                   
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete                                                                       
celery-worker-1  |     return future.result()                                                                                                                                       
celery-worker-1  |            ^^^^^^^^^^^^^^^                                                                                                                                       
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 137, in _run_pipeline_async                                                                                       
celery-worker-1  |     await session.commit()                                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 1014, in commit                                                         
celery-worker-1  |     await greenlet_spawn(self.sync_session.commit)
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 190, in greenlet_spawn                                               
celery-worker-1  |     result = context.switch(*args, **kwargs)                                                                                                                     
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2032, in commit                                                                 
celery-worker-1  |     trans.commit(_to_root=True)                                                                                                                                  
celery-worker-1  |   File "<string>", line 2, in commit                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 103, in _go                                                               
celery-worker-1  |     self._raise_for_prerequisite_state(fn.__name__, current_state)                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 973, in _raise_for_prerequisite_state                                           
celery-worker-1  |     raise sa_exc.PendingRollbackError(                                                                                                                           
celery-worker-1  | sqlalchemy.exc.PendingRollbackError: This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: Foreign key associated with column 'jobs.created_by' could not find table 'users' with which to generate a foreign key to target column 'id' (Background on this error at: https://sqlalche.me/e/20/7s2a)
celery-worker-1  | [2026-03-16 18:38:38,059: INFO/MainProcess] Task app.processing.tasks.process_job[e2863348-26dc-45bc-83a0-d6fb6af1aa8a] received
celery-worker-1  | [2026-03-16 18:38:38,061: INFO/ForkPoolWorker-2] Task app.processing.tasks.process_job[e2863348-26dc-45bc-83a0-d6fb6af1aa8a] retry: Retry in 10s: PendingRollbackError("This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: Foreign key associated with column 'jobs.created_by' could not find table 'users' with which to generate a foreign key to target column 'id'")
backend-1        | INFO:     172.20.0.6:51982 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:38 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"                                                                             
backend-1        | INFO:     172.20.0.6:51986 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:42 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"
backend-1        | INFO:     172.20.0.6:56658 - "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.0" 200 OK
frontend-1       | 172.20.0.1 - - [16/Mar/2026:18:38:46 +0000] "GET /api/v1/documents/jobs/4f2271d2-cf78-48b0-9669-473e82388542 HTTP/1.1" 200 362 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36" "-"                                                                             
celery-worker-1  | [2026-03-16 18:38:48,062: ERROR/ForkPoolWorker-2] Exception terminating connection <AdaptedConnection <asyncpg.connection.Connection object at 0x7be5fb046210>>
celery-worker-1  | Traceback (most recent call last):
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 374, in _close_connection
celery-worker-1  |     self._dialect.do_terminate(connection)                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 1130, in do_terminate                                           
celery-worker-1  |     dbapi_connection.terminate()                                                                                                                                 
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 907, in terminate                                               
celery-worker-1  |     self.await_(asyncio.shield(self._connection.close(timeout=2)))                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only                                                   
celery-worker-1  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501                                                             
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn                                               
celery-worker-1  |     value = await result                                                                                                                                         
celery-worker-1  |             ^^^^^^^^^^^^                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/connection.py", line 1504, in close                                                                      
celery-worker-1  |     await self._protocol.close(timeout)                                                                                                                          
celery-worker-1  |   File "asyncpg/protocol/protocol.pyx", line 627, in close                                                                                                       
celery-worker-1  |   File "asyncpg/protocol/protocol.pyx", line 660, in asyncpg.protocol.protocol.BaseProtocol._request_cancel                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/connection.py", line 1673, in _cancel_current_command                                                    
celery-worker-1  |     self._cancellations.add(self._loop.create_task(self._cancel(waiter)))                                                                                        
celery-worker-1  |                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 455, in create_task                                                                              
celery-worker-1  |     self._check_closed()                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 545, in _check_closed                                                                            
celery-worker-1  |     raise RuntimeError('Event loop is closed')                                                                                                                   
celery-worker-1  | RuntimeError: Event loop is closed                                                                                                                               
celery-worker-1  | [2026-03-16 18:38:48,063: ERROR/ForkPoolWorker-2] Task process_job failed for job 4f2271d2-cf78-48b0-9669-473e82388542                                           
celery-worker-1  | Traceback (most recent call last):                                                                                                                               
celery-worker-1  |   File "/app/app/processing/tasks.py", line 15, in process_job                                                                                                   
celery-worker-1  |     run_pipeline(job_id)                                                                                                                                         
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 27, in run_pipeline                                                                                               
celery-worker-1  |     asyncio.run(_run_pipeline_async(job_id))                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 195, in run                                                                                          
celery-worker-1  |     return runner.run(main)                                                                                                                                      
celery-worker-1  |            ^^^^^^^^^^^^^^^^                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 118, in run                                                                                          
celery-worker-1  |     return self._loop.run_until_complete(task)                                                                                                                   
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                   
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete                                                                       
celery-worker-1  |     return future.result()                                                                                                                                       
celery-worker-1  |            ^^^^^^^^^^^^^^^                                                                                                                                       
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 34, in _run_pipeline_async                                                                                        
celery-worker-1  |     result = await session.execute(                                                                                                                              
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^                                                                                                                              
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 463, in execute                                                         
celery-worker-1  |     result = await greenlet_spawn(                                                                                                                               
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^                                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn
celery-worker-1  |     result = context.throw(*sys.exc_info())                                                                                                                      
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2365, in execute                                                                
celery-worker-1  |     return self._execute_internal(                                                                                                                               
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal                                                      
celery-worker-1  |     conn = self._connection_for_bind(bind)                                                                                                                       
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind                                                   
celery-worker-1  |     return trans._connection_for_bind(engine, execution_options)                                                                                                 
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                 
celery-worker-1  |   File "<string>", line 2, in _connection_for_bind                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go                                                               
celery-worker-1  |     ret_value = fn(self, *arg, **kw)                                                                                                                             
celery-worker-1  |                 ^^^^^^^^^^^^^^^^^^^^                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind                                                   
celery-worker-1  |     conn = bind.connect()                                                                                                                                        
celery-worker-1  |            ^^^^^^^^^^^^^^                                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3273, in connect                                                                
celery-worker-1  |     return self._connection_cls(self)                                                                                                                            
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                            
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 145, in __init__                                                                
celery-worker-1  |     self._dbapi_connection = engine.raw_connection()                                                                                                             
celery-worker-1  |                              ^^^^^^^^^^^^^^^^^^^^^^^                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3297, in raw_connection                                                         
celery-worker-1  |     return self.pool.connect()                                                                                                                                   
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^                                                                                                                                   
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 449, in connect                                                                   
celery-worker-1  |     return _ConnectionFairy._checkout(self)                                                                                                                      
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1363, in _checkout                                                                
celery-worker-1  |     with util.safe_reraise():                                                                                                                                    
celery-worker-1  |          ^^^^^^^^^^^^^^^^^^^                                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__                                                           
celery-worker-1  |     raise exc_value.with_traceback(exc_tb)                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1301, in _checkout                                                                
celery-worker-1  |     result = pool._dialect._do_ping_w_event(                                                                                                                     
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 720, in _do_ping_w_event                                                     
celery-worker-1  |     return self.do_ping(dbapi_connection)                                                                                                                        
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 1163, in do_ping                                                
celery-worker-1  |     dbapi_connection.ping()                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 813, in ping                                                    
celery-worker-1  |     self._handle_exception(error)                                                                                                                                
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 794, in _handle_exception                                       
celery-worker-1  |     raise error                                                                                                                                                  
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 811, in ping                                                    
celery-worker-1  |     _ = self.await_(self._async_ping())                                                                                                                          
celery-worker-1  |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                          
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only
celery-worker-1  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501                                                             
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn                                               
celery-worker-1  |     value = await result                                                                                                                                         
celery-worker-1  |             ^^^^^^^^^^^^                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 820, in _async_ping                                             
celery-worker-1  |     await tr.start()                                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/transaction.py", line 146, in start                                                                      
celery-worker-1  |     await self._connection.execute(query)                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/connection.py", line 349, in execute                                                                     
celery-worker-1  |     result = await self._protocol.query(query, timeout)                                                                                                          
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                          
celery-worker-1  |   File "asyncpg/protocol/protocol.pyx", line 375, in query                                                                                                       
celery-worker-1  | RuntimeError: Task <Task pending name='Task-14' coro=<_run_pipeline_async() running at /app/app/processing/pipeline.py:34> cb=[_run_until_complete_cb() at /usr/local/lib/python3.12/asyncio/base_events.py:181]> got Future <Future pending cb=[BaseProtocol._on_waiter_completed()]> attached to a different loop                                  
celery-worker-1  | [2026-03-16 18:38:48,071: WARNING/ForkPoolWorker-2] /usr/local/lib/python3.12/site-packages/billiard/einfo.py:27: RuntimeWarning: coroutine 'Connection._cancel' was never awaited                                                                                                                                                                   
celery-worker-1  |   self._co_positions = list(code.co_positions())
celery-worker-1  |                                                                                                                                                                  
celery-worker-1  | [2026-03-16 18:38:48,075: ERROR/ForkPoolWorker-2] Task app.processing.tasks.process_job[e2863348-26dc-45bc-83a0-d6fb6af1aa8a] raised unexpected: RuntimeError("Task <Task pending name='Task-14' coro=<_run_pipeline_async() running at /app/app/processing/pipeline.py:34> cb=[_run_until_complete_cb() at /usr/local/lib/python3.12/asyncio/base_events.py:181]> got Future <Future pending cb=[BaseProtocol._on_waiter_completed()]> attached to a different loop")
celery-worker-1  | Traceback (most recent call last):
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/celery/app/trace.py", line 453, in trace_task                                                                    
celery-worker-1  |     R = retval = fun(*args, **kwargs)                                                                                                                            
celery-worker-1  |                  ^^^^^^^^^^^^^^^^^^^^                                                                                                                            
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/celery/app/trace.py", line 736, in __protected_call__                                                            
celery-worker-1  |     return self.run(*args, **kwargs)                                                                                                                             
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                             
celery-worker-1  |   File "/app/app/processing/tasks.py", line 18, in process_job                                                                                                   
celery-worker-1  |     self.retry(exc=exc)                                                                                                                                          
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/celery/app/task.py", line 743, in retry                                                                          
celery-worker-1  |     raise_with_context(exc)                                                                                                                                      
celery-worker-1  |   File "/app/app/processing/tasks.py", line 15, in process_job                                                                                                   
celery-worker-1  |     run_pipeline(job_id)                                                                                                                                         
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 27, in run_pipeline                                                                                               
celery-worker-1  |     asyncio.run(_run_pipeline_async(job_id))                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 195, in run                                                                                          
celery-worker-1  |     return runner.run(main)                                                                                                                                      
celery-worker-1  |            ^^^^^^^^^^^^^^^^                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/runners.py", line 118, in run                                                                                          
celery-worker-1  |     return self._loop.run_until_complete(task)                                                                                                                   
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                   
celery-worker-1  |   File "/usr/local/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete                                                                       
celery-worker-1  |     return future.result()                                                                                                                                       
celery-worker-1  |            ^^^^^^^^^^^^^^^                                                                                                                                       
celery-worker-1  |   File "/app/app/processing/pipeline.py", line 34, in _run_pipeline_async                                                                                        
celery-worker-1  |     result = await session.execute(                                                                                                                              
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^                                                                                                                              
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/ext/asyncio/session.py", line 463, in execute                                                         
celery-worker-1  |     result = await greenlet_spawn(                                                                                                                               
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^                                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn                                               
celery-worker-1  |     result = context.throw(*sys.exc_info())                                                                                                                      
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2365, in execute                                                                
celery-worker-1  |     return self._execute_internal(                                                                                                                               
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2241, in _execute_internal                                                      
celery-worker-1  |     conn = self._connection_for_bind(bind)                                                                                                                       
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2110, in _connection_for_bind                                                   
celery-worker-1  |     return trans._connection_for_bind(engine, execution_options)                                                                                                 
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                 
celery-worker-1  |   File "<string>", line 2, in _connection_for_bind                                                                                                               
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/state_changes.py", line 139, in _go                                                               
celery-worker-1  |     ret_value = fn(self, *arg, **kw)                                                                                                                             
celery-worker-1  |                 ^^^^^^^^^^^^^^^^^^^^                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 1189, in _connection_for_bind                                                   
celery-worker-1  |     conn = bind.connect()                                                                                                                                        
celery-worker-1  |            ^^^^^^^^^^^^^^                                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3273, in connect                                                                
celery-worker-1  |     return self._connection_cls(self)                                                                                                                            
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                            
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 145, in __init__                                                                
celery-worker-1  |     self._dbapi_connection = engine.raw_connection()                                                                                                             
celery-worker-1  |                              ^^^^^^^^^^^^^^^^^^^^^^^                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3297, in raw_connection                                                         
celery-worker-1  |     return self.pool.connect()                                                                                                                                   
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^                                                                                                                                   
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 449, in connect                                                                   
celery-worker-1  |     return _ConnectionFairy._checkout(self)                                                                                                                      
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1363, in _checkout                                                                
celery-worker-1  |     with util.safe_reraise():                                                                                                                                    
celery-worker-1  |          ^^^^^^^^^^^^^^^^^^^                                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__                                                           
celery-worker-1  |     raise exc_value.with_traceback(exc_tb)                                                                                                                       
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/pool/base.py", line 1301, in _checkout                                                                
celery-worker-1  |     result = pool._dialect._do_ping_w_event(                                                                                                                     
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                     
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 720, in _do_ping_w_event                                                     
celery-worker-1  |     return self.do_ping(dbapi_connection)                                                                                                                        
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 1163, in do_ping                                                
celery-worker-1  |     dbapi_connection.ping()                                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 813, in ping                                                    
celery-worker-1  |     self._handle_exception(error)                                                                                                                                
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 794, in _handle_exception                                       
celery-worker-1  |     raise error                                                                                                                                                  
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 811, in ping                                                    
celery-worker-1  |     _ = self.await_(self._async_ping())                                                                                                                          
celery-worker-1  |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                          
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only                                                   
celery-worker-1  |     return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501                                                             
celery-worker-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                                                      
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn                                               
celery-worker-1  |     value = await result                                                                                                                                         
celery-worker-1  |             ^^^^^^^^^^^^                                                                                                                                         
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 820, in _async_ping                                             
celery-worker-1  |     await tr.start()                                                                                                                                             
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/transaction.py", line 146, in start                                                                      
celery-worker-1  |     await self._connection.execute(query)                                                                                                                        
celery-worker-1  |   File "/usr/local/lib/python3.12/site-packages/asyncpg/connection.py", line 349, in execute                                                                     
celery-worker-1  |     result = await self._protocol.query(query, timeout)                                                                                                          
celery-worker-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
celery-worker-1  |   File "asyncpg/protocol/protocol.pyx", line 375, in query
celery-worker-1  | RuntimeError: Task <Task pending name='Task-14' coro=<_run_pipeline_async() running at /app/app/processing/pipeline.py:34> cb=[_run_until_complete_cb() at /usr/local/lib/python3.12/asyncio/base_events.py:181]> got Future <Future pending cb=[BaseProtocol._on_waiter_completed()]> attached to a different loop