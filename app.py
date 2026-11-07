import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379)   # "redis" = the service name in compose

def get_count():
    for attempt in range(5):                   # retry in case redis is still starting
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError:
            time.sleep(0.5)
    raise RuntimeError("Could not connect to Redis")

@app.route("/")
def home():
    return f"Hello! This page has been visited {get_count()} times.\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)         # 0.0.0.0 so it is reachable outside the container