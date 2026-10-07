
from asyncio import sleep
import asyncio
import time

from fastapi import FastAPI

app=FastAPI()


'''
Runs in main thread
No awaitable operation, cannot be paused
Sequential Order
Request 1
    Endpoint 1 called
    Endpoint 1 completed
Request 2
    Endpoint 1 called
    Endpoint 1 completed
'''
@app.get("/1")
async def endpoint1(): #processed sequentially
    print("Endpoint 1 called")  
    time.sleep(5)  # Blocking io operation, fn exec isn't paused, during which the event loop is blocked while waiting for the results and cannot process other requests
    print("Endpoint 1 completed")

'''
Runs in main thread
Has awaitable operation, can be paused
Request 1
    Endpoint 2 called
Request 2
    Endpoint 2 called
Request 1
    Endpoint 2 completed
Request 2
    Endpoint 2 completed
'''
@app.get("/2")
async def endpoint2(): #processed concurrently
    print("Endpoint 2 called")  
    await asyncio.sleep(5)  # Non-blocking io operation, awaited, fn exec paused until the sleep is done during which the event loop can run other tasks like processing other requests
    print("Endpoint 2 completed")

'''
runs  in separate threads, hence parallely
Request 1 & Request 2 parallel threads
    Endpoint 3 called
    Endpoint 3 called

waits

Request 1 & Request 2 parallel threads
    Endpoint 3 completed
    Endpoint 3 completed
'''
@app.get("/3")
def endpoint3(): #processed parallely
    print("Endpoint 3 called")  
    time.sleep(5)  # Simulate a long-running task
    print("Endpoint 3 completed")



'''
Endpoint 2: "I'm waiting → let someone else use the event loop."
Endpoint 3: "I'm blocking → put me in a separate thread so I don't block the event loop."
'''



#when we run a fast api using uvicorn it starts a main thread
#all endpts are defined as coroutines running in event loop within main thread


'''
BEST PRACTICES

1. Use async def for endpoint with non-blocking I/O operations
2. Don't use async def for endpoint with blocking I/O operations
3. Use normal function for endpoints with blocking I/O operations
'''