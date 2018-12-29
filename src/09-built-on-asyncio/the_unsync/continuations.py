from unsync import unsync, Unfuture
import asyncio
import time
import math

@unsync
async def initiate(initial_value: int):
    await asyncio.sleep(0.1)
    return initial_value + 1

@unsync
async def process(task: Unfuture):
    print("process...")
    await asyncio.sleep(0.1)
    return task.result() * 2

# you cannot have a Multiprocess ( cpu_bound=True ) as a contination as the asyncio.Task
# is not pickaleable
# TypeError: can't pickle _asyncio.Task objects
@unsync(cpu_bound=False)
def process_cpu(task: Unfuture):
    print("Computing...")
    result: float = 0.0
    number = task.result()
    for _ in range(1, 10_000_000):
        result = math.sqrt(number ** number + .01)

    return result


start = time.time()
result = initiate(3).then(process).result()
print(result)
assert result == 8
print('Executed in {} seconds'.format(time.time() - start))


start = time.time()
result = initiate(5).then(process).then(process).result()
print(result)
assert result == 24
print('Executed in {} seconds'.format(time.time() - start))

start = time.time()
result = initiate(6).then(process).then(process).then(process_cpu).result()
print(result)
print('Executed in {} seconds'.format(time.time() - start))
