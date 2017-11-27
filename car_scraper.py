"""Simple scrapper for www.nydailynews.com/autos."""

from bs4 import BeautifulSoup
import requests
import queue
import threading

from utils import Storage


PAGE_TRUCKS = 'http://www.nydailynews.com/autos/types/truck'
PAGE_SPORTS = 'http://www.nydailynews.com/autos/types/sports-car'

# Most popular user agent
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/40.0.2214.85 Safari/537.36 '}
WORKERS_NUMBER = 3


def get_car_links(page):
    """Find all the car links."""
    r = requests.get(page, headers=HEADERS)
    html_doc = r.content

    soup = BeautifulSoup(html_doc, 'html.parser')
    car_list = soup.find("div", {"class": "rtww"}).find_all('a')

    car_links = set()

    for car_item in car_list:
        car_links.add(car_item['href'])

    return car_links


def car_worker(queue):
    """Parse a car link for details."""
    storage = Storage()

    while True:
        job = queue.get()
        if job is None:
            break

        job_name, car_link = job
        car_data = {}

        session = requests.Session()
        session.headers.update(HEADERS)

        page_response = session.get(car_link)
        html_car = page_response.content
        soup = BeautifulSoup(html_car, 'html.parser')

        title = soup.find("h1", {"id": "ra-headline"}).text
        car_data['title'] = title
        car_data['summary'] = {}

        table = soup.find("div", {"class": "ymm-specs-wrap"}).find_all("dl")
        for row in table:
            key = row.find("dt").text
            values = [v.text for v in row.find_all("dd")]

            car_data['summary'][key] = values

        overview = soup.find("article", {"id": "ra-body"}).find("p")
        car_data['overview'] = overview.text.strip()

        # API call to
        # http://api.edmunds.com/api/vehicle/v2/styles/401693759?view=full&fmt=json&api_key=b72ndgbvxw4vp92eugantyr4

        storage[job_name].update({car_link: car_data})
        queue.task_done()
        session.close()
        print('Successfully parsed {}'.format(car_link))


def main():
    """Parse http://www.nydailynews.com/autos/types/truck."""
    storage = Storage()
    storage['trucks'] = {}
    storage['sports'] = {}

    links_queue = queue.Queue()
    threads = []
    for i in range(WORKERS_NUMBER):
        t = threading.Thread(target=car_worker, args=(links_queue,))
        t.start()
        threads.append(t)

    truck_links = get_car_links(PAGE_TRUCKS)
    for item in truck_links:
        links_queue.put(('trucks', item))

    sport_links = get_car_links(PAGE_SPORTS)
    for item in sport_links:
        links_queue.put(('sports', item))

    # block until all tasks are done
    links_queue.join()

    # stop workers
    for i in range(WORKERS_NUMBER):
        links_queue.put(None)
    for t in threads:
        t.join()

    storage.dump()
    print('Done.')


if __name__ == "__main__":
    main()
