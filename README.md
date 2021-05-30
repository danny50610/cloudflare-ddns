# cloudflare-ddns

## 安裝
```
pipenv install
```

## crontab
```
*/5 * * * * (cd /home/danny/cloudflare-ddns; /home/danny/.local/bin/pipenv run python3 cloudflare-ddns.py >/dev/null 2>&1)
```
