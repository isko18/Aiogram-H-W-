import schedule
import time
import requests
import logging
from requests.exceptions import RequestException
import argparse


def perform_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Request to {url} succeeded with status code {response.status_code}")
        return response.text
    except RequestException as e:
        print(f"Request to {url} failed: {e}")
        return None


def main(url, initial_delay, interval, log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    def job():
        result = perform_request(url)
        if result:
            logging.info(f"Request succeeded. Response: {result[:100]}")

    schedule.every(initial_delay).seconds.do(lambda: None)
    schedule.every(interval).seconds.do(job)

    print(f"Starting scheduler with initial delay of {initial_delay} seconds and interval of {interval} seconds")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Request Scheduler")
    parser.add_argument("url", type=str, help="URL для запросов")
    parser.add_argument("initial_delay", type=int, help="Начальная задержка в секундах")
    parser.add_argument("interval", type=int, help="Интервал между запросами в секундах")
    parser.add_argument("log_file", type=str, help="Файл для сохранения логов")

    args = parser.parse_args()
    
    main(args.url, args.initial_delay, args.interval, args.log_file)
