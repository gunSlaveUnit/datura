import gzip

import requests

url = "http://localhost:8000/download/"
response = requests.get(url, stream=True)
file_name = response.headers.get("Content-Disposition").split('=')[1]
with open(file_name, "wb") as f:
    with gzip.GzipFile(fileobj=response.raw, mode="rb") as gz:
        while True:
            chunk = gz.read(8192)
            if not chunk:
                break
            f.write(chunk)
            print(f"Wrote {len(chunk)} bytes to file")
