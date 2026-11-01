import asyncio 
import time


def sync_function(test_param : str) -> str: 
    print(f"this is sync function ")

    time.sleep(2)

    return f"sync result : {test_param}"



async def async_function(test_param : str) -> str: 
    print(f"this is async coroutine functon ")

    await asyncio.sleep(2)

    return f"async result : {test_param}"


async def main():
    # sync_result = sync_function("test1")
    # print(sync_result)

    # loop = asyncio.get_running_loop()
    # future = loop.create_future()
    # print(f"Empty Future : {future}")

    # future.set_result("test2")
    # future_result = await future
    # print(f"Future Result : {future_result}")

    # coroutine_obj = async_function("test3")
    # print(f"Coroutine Object : {coroutine_obj}")

    # coroutine_result = await coroutine_obj
    # print(f"Coroutine Result : {coroutine_result}")

    task = asyncio.create_task(async_function("test4"))
    print(f"Task : {task}")

    task_result = await task
    print(f"Task Result : {task_result}")



if __name__ == "__main__":
    asyncio.run(main())