#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import os
import requests
import yaml
import logging


def main():
    logger = get_logger()

    # 讀取設定檔
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # 取得目前 IP
    r = requests.get(config['get_ip_url'])
    ip = r.text

    last_ip = None
    if os.path.isfile('last_ip'):
        with open('last_ip', 'r') as f:
            last_ip = f.readline().strip()

    # 檢查是否需要更新，若需要就更新到 cloudflare
    if ip != last_ip:
        print('Start update ip on cloudflare.')

        success = True
        for domain in config['target_domains']:
            # https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
            zone_id = domain['zone_id']
            record_id = domain['record_id']
            url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + domain['api_token']
            }

            data = {
                'type': 'A',
                'name': domain['domain'],
                'content': ip,
                'proxied': domain['proxied']
            }

            r = requests.put(url, headers=headers, data=json.dumps(data))

            print(r.status_code, r.text)

            if r.status_code != 200:
                success = False
                logger.error(domain['domain'])
                logger.error(r.status_code)
                logger.error(r.text)

        if success:
            # 紀錄這次的 IP
            with open('last_ip', 'w') as f:
                f.write(ip)

            logger.info('Update IP: ' + ip)
    else:
        print('IP no change, skip update.')


def get_logger():
    logger = logging.getLogger('cloudflare-ddns')
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('cloudflare-ddns.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger


if __name__ == '__main__':
    main()
