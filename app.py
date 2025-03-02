import time
import redis
from flask import Flask, render_template_string

app = Flask(__name__)

# Use 'redis' as the hostname because of Docker Compose
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Redis Counter</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body { background: linear-gradient(120deg, #3498db, #8e44ad); color: white; font-family: Arial, sans-serif; text-align: center; }
        h1 { margin-top: 50px; }
        .counter { font-size: 4rem; font-weight: bold; color: yellow; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="display-4">Welcome to My Flask Redis App 🚀</h1>
        <p class="lead">This page has been viewed:</p>
        <h2 class="counter">{{ count }}</h2>
        <p class="text-muted">Refresh to see the count increase!</p>
    </div>
</body>
</html>"""

@app.route('/')
def home():
    count = get_hit_count()
    return render_template_string(html_template, count=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
