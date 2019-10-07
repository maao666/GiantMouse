import requests
import datetime
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)

def get_chp(api_url="https://chp.shadiao.app/api.php?from_shortcuts",
            headers={"site": "www.shadiao.app"}) -> str:
    r = requests.get(api_url, headers=headers)
    log = "[{0}]Status Code: {1}".format(
        datetime.datetime.now(), r.status_code)
    logging.debug(msg=log)
    try:
        return r.text
    finally:
        r.close()

def write_to_csv(filename='chp_DB.csv', time_interval=0.5):
    
    while True:
        try:
            chp_text = get_chp()
            with open(filename, 'r') as f:
                file_content = f.read()
            if file_content.find(chp_text) == -1:
                csv_line = '''"{0}","{1}"\n'''.format(
                    chp_text, datetime.datetime.now())
                print(csv_line)
                with open(filename, 'a') as f:
                    f.write(csv_line)
        except:
            log = "[{0}] Fetch failed!".format(datetime.datetime.now())
            logging.warning(msg=log)
        sleep(time_interval)


def main():
    write_to_csv()

if __name__ == '__main__':
    main()
