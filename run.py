"""Run example."""

import car_scraper
import web


def main():
    """Run scraper and web server."""
    car_scraper.main()
    web.main()


if __name__ == '__main__':
    main()
