# cloudflare-ddns

## 安裝
```
uv sync
```

## crontab
```
*/5 * * * * (cd /home/danny/cloudflare-ddns; /home/danny/.local/bin/uv python3 cloudflare-ddns.py >/dev/null 2>&1)
```
