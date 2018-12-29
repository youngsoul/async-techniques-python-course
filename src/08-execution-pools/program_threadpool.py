import requests
import bs4
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor
# from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor
import time

def main():
    urls = [
        'https://talkpython.fm',
        'https://pythonbytes.fm',
        'https://google.com',
        'https://realpython.com',
        'https://training.talkpython.fm/',
    ]

    work = []

    with PoolExecutor() as executor:
        for url in urls:
            # print("Getting title from {}".format(url.replace('https', '')),
            #       end='... ',
            #       flush=True)
            # title = get_title(url)
            f: Future = executor.submit(get_title, url, time.time())
            work.append(f)

        print("Waiting for downloads...", flush=True)

    print("All jobs submitted", flush=True)
    for f in work:
        print("{}".format(f.result()), flush=True)


def get_title(url: str, t: float) -> str:
    import multiprocessing
    p = multiprocessing.current_process()
    print("Getting title from {}, PID: {}, ProcName: {}, at t: {}".format(
        format(url.replace('https://', ''), " <25s"), p.pid, p.name, t),
        flush=True)

    a = "unset"
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
                                                        'Gecko/20100101 Firefox/61.0'})
        resp.raise_for_status()

        html = resp.text

        soup = bs4.BeautifulSoup(html, features="html.parser")
        tag: bs4.Tag = soup.select_one('h1')

        if not tag:
            a = "NONE"
        elif not tag.text:
            a = tag.select_one('a')
            if a and a.text:
                a = a.text
            elif a and 'title' in a.attrs:
                a = a.attrs['title']
            else:
                a = "NONE"
        else:
            a = tag.get_text(strip=True)

        print("DONE: Getting title from {}, PID: {}, ProcName: {}".format(
            format(url.replace('https://', ''), " <25s"), p.pid, p.name),
            flush=True)
        return a
    except Exception as exc:
        print(f"EXCEPTION IN get_title: {exc}")

    return "ERROR"


if __name__ == '__main__':
    main()
