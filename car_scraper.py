"""Simple scrapper for www.nydailynews.com/autos."""

from bs4 import BeautifulSoup
import requests
import queue
import threading

from utils import Storage


PAGE1 = 'http://www.nydailynews.com/autos/types/truck'
# PAGE2 = 'http://www.nydailynews.com/autos/types/sports-car'

# Most popular user agent
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/40.0.2214.85 Safari/537.36 '}
WORKERS_NUMBER = 3


def get_car_links():
    """Find all the car links."""
    r = requests.get(PAGE1, headers=HEADERS)
    html_doc = r.content

    soup = BeautifulSoup(html_doc, 'html.parser')
    car_list = soup.find("div", {"class": "rtww"}).find_all('a')

    car_links = set()

    for car_item in car_list:
        car_links.add(car_item['href'])

    return car_links


def car_worker(queue):
    """Parse a car link for details."""
    storage = Storage('cars')

    while True:
        car_link = queue.get()
        if car_link is None:
            break

        car_data = {}

        r = requests.get(car_link, headers=HEADERS)
        html_car = r.content
        soup = BeautifulSoup(html_car, 'html.parser')

        title = soup.find("h1", {"id": "ra-headline"}).text
        car_data['title'] = title
        car_data['summary'] = {}

        table = soup.find("div", {"class": "ymm-specs-wrap"}).find_all("dl")
        for row in table:
            key = row.find("dt").text
            values = [v.text for v in row.find_all("dd")]

            car_data['summary'][key] = values

        storage.update({car_link: car_data})
        queue.task_done()


def main():
    """Parse http://www.nydailynews.com/autos/types/truck."""
    car_links = get_car_links()
    storage = Storage('cars')

    links_queue = queue.Queue()
    threads = []
    for i in range(WORKERS_NUMBER):
        t = threading.Thread(target=car_worker, args=(links_queue,))
        t.start()
        threads.append(t)

    for item in car_links:
        links_queue.put(item)

    # block until all tasks are done
    links_queue.join()

    # stop workers
    for i in range(WORKERS_NUMBER):
        links_queue.put(None)
    for t in threads:
        t.join()

    storage.dump()


if __name__ == "__main__":
    main()
