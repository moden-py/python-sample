# Python Developer Sample Project

## Run scraper
1. Install requirements `pip install -r ./requirements.txt`
2. Run main script `python ./car_scraper.py`

Result files stored in: `trucks.json` and `sports.json`


# Run web server
1. Run script `python ./web.py`
2. Open `http://127.0.0.1:8000/` in your browser


# Found issues
1. Price and other data are rendered by JS.
Thus, it is not possible to simply obtain this data from the markup.
There are two options:
  - Use Selenium / WebKit based "headless" browsers. Then grab already renders data.
  This approach is fraught with a large overhead, but it looks more universal.

  - Investigate API calls used by the JS scripts.
  I was able to determine that the extended data is received from this node - `api.edmunds.com`.
  There is an example of a query - `http://api.edmunds.com/api/vehicle/v2/styles/401693759?view=full&fmt=json&api_key=b72ndgbvxw4vp92eugantyr4`.
  An example of the answer can be found in file - `./401693759.json`.
  So it is for certain that additional information can be obtained from the API.
  This approach will be most effective if we have access to the API.

2. `requests` and `beautifulsoup` are not the best candidates for web scraping.
`Beautifulsoup` works slowly, it also does not support XPath.
For python 3, I would advise `asyncio` + `aiohttp` in conjunction with `lxml`.


# Build Docker image
`docker build -t car_scraper`

# Run image
`docker run -ti -d car_scraper`