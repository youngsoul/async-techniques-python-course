from unsync import unsync
import asyncio
import datetime
import math

import aiohttp
import requests
import time

def main():
    t0 = datetime.datetime.now()

    # unsync allows up to remove the async/await event loop boilerplate
    # the tasks collection will ultimately be a collection of unfutures
    # the functions get called immediately
    tasks = [
        compute_some(),
        compute_some(),
        compute_some(),
        download_some(),
        download_some(),
        download_some_more(),
        download_some_more(),
        wait_some(),
        wait_some(),
        wait_some(),
        wait_some(),
    ]

    # .result() is blocking so very much like t.join waiting for all of the results to be done
    x = [t.result() for t in tasks]
    print(x)


    dt = datetime.datetime.now() - t0
    print("Synchronous version done in {:,.2f} seconds.".format(dt.total_seconds()))


# note no 'async' in front of the function. So this will not be run with the
# asyncio event loop.  Since we specified cpu_bound=True, this method will be
# run as a process NOT a thread.  cpu bound activities in python do not perform better on
# threads because of the GIL
@unsync(cpu_bound=True)
def compute_some():
    print("Computing...")
    result: float = 0.0
    for _ in range(1, 10_000_000):
        result = math.sqrt(25 ** 25 + .01)

    return result

# note the 'async' in front of the function.  this will be run in a typical async io event loop
@unsync()
async def download_some():
    print("Downloading...")
    url = 'https://talkpython.fm/episodes/show/174/coming-into-python-from-another-industry-part-2'
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as resp:
            resp.raise_for_status()

            text = await resp.text()

    msg = "Downloaded {:,} characters.".format(len(text))
    print(msg)
    return msg


# note no 'async' in front of the function.  Since this is not specified to be cpu bound
# this function will be run on multiple threads
@unsync()
def download_some_more():
    print("Downloading more ...")
    url = 'https://pythonbytes.fm/episodes/show/92/will-your-python-be-compiled'
    resp = requests.get(url)
    resp.raise_for_status()

    text = resp.text

    msg = "Downloaded (more) {:,} characters.".format(len(text))
    print(msg)
    return msg


# note the 'async' in front of the function.  this will be run in a typical async io event loop
@unsync()
async def wait_some():
    print("Waiting...")
    for _ in range(1, 1000):
        await asyncio.sleep(.001)

    return True

if __name__ == '__main__':
    main()
