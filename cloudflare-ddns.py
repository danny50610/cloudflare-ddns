#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import os
import requests
from dotenv import load_dotenv


def main():
    # 讀取設定檔
    load_dotenv()

    # 取得目前 IP
    r = requests.get(os.getenv('get_ip_url'))
    ip = r.text

    last_ip = None
    if os.path.isfile('last_ip'):
        with open('last_ip', 'r') as f:
            last_ip = f.readline().strip()

    # 檢查是否需要更新，若需要就更新到 cloudflare
    if ip != last_ip:
        print('Start update ip on cloudflare.')

        # https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
        zone_id = os.getenv('zone_id')
        record_id = os.getenv('record_id')
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.getenv('api_token')
        }

        data = {
            'type': 'A',
            'name': os.getenv('target_domain'),
            'content': ip,
            'proxied': False
        }

        r = requests.put(url, headers=headers, data=json.dumps(data))

        print(r.status_code, r.text)

        # 紀錄這次的 IP
        if r.status_code == 200:
            with open('last_ip', 'w') as f:
                f.write(ip)
    else:
        print('IP no change, skip update.')


if __name__ == '__main__':
    main()
