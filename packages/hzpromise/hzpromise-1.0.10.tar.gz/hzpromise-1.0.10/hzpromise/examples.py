from promise import Promise
from time import sleep
from threading import Thread
import asyncio 
from concurrent.futures import ThreadPoolExecutor

def work(name, n, resolve=None, result=None):
    for i in range(n):
        print(name)
        sleep(.5)
    if resolve:
        resolve(result)
    return f'{name}, goodbye!'

def test_simple_then_solve():
    a = Promise(lambda resolve,reject: [print("hello"), resolve("world")])
    a.then(print)

def test_simple_then_reject():
    a = Promise(lambda resolve, reject: [print("hello"), 1/0])
    a.then(None, print)

def test_chen_chain():
    a = Promise()
    c = a.then(lambda v:[print(v), "obama!"][-1]).then(lambda v:[print(v), "trump!"][-1])
    a.resolve("president")
    print(c.value)

def test_chen_manytimes():
    a = Promise()
    a.then(lambda v:print(f"hello,{v}"))
    a.then(lambda v:print(f"goodbye,{v}"))
    a.resolve("obama")

def test_async_by_thread():
    def async_work(resolve, reject):
        Thread(target=work, args=("obama", 6, resolve, "trump")).start()
    a = Promise(async_work)
    a.then(print)

def test_async_by_coroutine():
    async def work(resolve, reject):
        for i in range(5):
            print("obama!")
            await asyncio.sleep(.5) 
        resolve("trump")
    a = Promise(work)
    a.then(print)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(a._task))

def test_promise_a_coroutine():
    async def work(name):
        for i in range(5):
            print(name)
            await asyncio.sleep(1)
        return f"{name}，再见"
    a = Promise()
    a.then(print)
    a.resolve(work("周冬雨"))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(a._task))
def test_promise_a_task():
    async def work(name):
        for i in range(5):
            print(name)
            await asyncio.sleep(1)
        return "zhou"
    loop = asyncio.get_event_loop()
    task = loop.create_task(work("lili"))
    a = Promise()
    a.then(print)
    a.resolve(task)
    loop.run_until_complete(task)

def test_promise_a_future():
    executor = ThreadPoolExecutor(2)
    future = executor.submit(work, "周杰伦", 6)
    a = Promise()
    a.then(print)
    a.resolve(future)
