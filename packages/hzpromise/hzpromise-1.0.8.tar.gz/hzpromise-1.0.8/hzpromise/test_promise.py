from promise import Promise 
from threading import Thread
from time import sleep
import asyncio
from pytest import mark
def test_create():
    a = Promise()
    a = Promise(lambda r,j:print("hello"))

def test_value():
    a = Promise(lambda r,j:r("huzheng"))
    assert a.value == "huzheng"

def test_reason():
    a = Promise(lambda r,j: 1/0)
    assert a._state == "REJECTED"
    print(a.reason)

def test_then():
    a = Promise()
    a.then(print)
    a.set_value("huzheng, nihao")
    
def test_then_many():
    a = Promise()
    a.then(lambda r:[print(r), "huang"][1])
    a.then(print)
    a.set_value("huzheng")

def test_then_chain():
    a = Promise()
    b = a.then(lambda r:[print(r), "huang"][1])
    print(b._state)
    b.then(print)
    a.set_value("huzheng")
    print(b._state)

def test_thread_promise():
    def work(resolve, reject):
        Thread(target=lambda:[sleep(2), print("work done!"), resolve("huzheng"), None][-1], args=()).start()
    a = Promise(work).then(lambda v:[print(v), "huang"][-1]).then(print)
    print("start")

@mark.coroutine
def test_coroutine_promise():
    async def work(resolve, reject):
        await asyncio.sleep(3)
        print("work done!")
        resolve("huzheng")
    a = Promise(work)
    a.then(print)
    loop = asyncio.get_event_loop()
    print("start")
    loop.run_until_complete(a._task) 

@mark.other
def test_all():
    def work(name, n):
        def job(resolve, reject):
            def run():
                sleep(n)
                print("hello")
                resolve(name)
            Thread(target=run, args=()).start()
        return job
    print("start")
    a = Promise(work("huzheng", 1))
    b = Promise(work("huang", 2))
    c = Promise(work("baobao",3))
    d = Promise.all([a,b,c]).then(print)

@mark.race
def test_race():
    def work(name, n):
        def job(resolve, reject):
            def run():
                sleep(n)
                print("hello")
                resolve(name)
            Thread(target=run, args=()).start()
        return job
    print("start")
    a = Promise(work("huzheng", 1))
    b = Promise(work("huang", 2))
    c = Promise(work("baobao",3))
    d = Promise.race([a,b,c]).then(print)

   
    
