import csv
import random
from datetime import datetime, timedelta

# Constants with weights
HTTP_METHODS = [('GET', 70), ('POST', 20), ('PUT', 5), ('DELETE', 3), ('PATCH', 1), ('OPTIONS', 0.5), ('HEAD', 0.5)]
HTTP_VERSIONS = ['HTTP/1.1', 'HTTP/2.0']
STATUS_CODES = [(200, 70), (404, 10), (302, 5), (500, 3), (201, 2), (204, 2), (301, 2), (400, 2), (401, 1), (403, 1), (502, 1), (503, 1)]
REFERRERS = [
    ("https://www.google.com", 30), ("https://www.youtube.com", 20), ("https://www.facebook.com", 15),
    ("https://www.amazon.com", 10), ("https://www.wikipedia.org", 5), ("https://www.twitter.com", 5),
    ("https://www.instagram.com", 5), ("https://www.linkedin.com", 3), ("https://www.netflix.com", 2),
    ("https://www.spotify.com", 2), ("https://www.reddit.com", 1), ("https://www.pinterest.com", 1),
    ("https://www.wordpress.com", 0.5), ("https://www.ebay.com", 0.5), ("https://www.craigslist.org", 0.25),
    ("https://www.microsoft.com", 0.25), ("https://www.github.com", 0.1), ("https://www.quora.com", 0.1),
    ("https://www.medium.com", 0.05), ("https://www.tumblr.com", 0.05), ("https://www.paypal.com", 0.05), ("", 5)
]
URIS = [
    ("/home", 50), ("/login", 10), ("/about", 5), ("/contact", 5), ("/products", 5), ("/services", 5),
    ("/privacy-policy", 2), ("/terms-of-service", 2), ("/logout", 2), ("/profile", 2),
    ("/search", 10), ("/help", 1), ("/settings", 1), ("/download", 1), ("/upload", 1),
    ("/404", 0.5), ("/dashboard", 3), ("/reports", 2), ("/analytics", 2), ("/user/edit", 1),
    ("/notifications", 1), ("/messages", 1), ("/friends", 1)
]
USER_AGENTS = [
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36", 20),
    ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15", 20),
    ("Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1", 15),
    ("Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1", 15),
    ("Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36", 15),
    ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", 5),
    ("Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)", 5),
    ("Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)", 2.5),
    ("DuckDuckBot/1.0; (+https://duckduckgo.com/duckduckbot.html)", 2.5)
]

def choose_weighted(options):
    """Choose an option based on weights."""
    values, weights = zip(*options)
    total = sum(weights)
    rnd = random.uniform(0, total)
    upto = 0
    for value, weight in zip(values, weights):
        if upto + weight >= rnd:
            return value
        upto += weight

def generate_http_method():
    return choose_weighted(HTTP_METHODS)

def generate_http_version():
    return random.choice(HTTP_VERSIONS)

def generate_status_code():
    return choose_weighted(STATUS_CODES)

def generate_referrer():
    return choose_weighted(REFERRERS)

def generate_uri():
    return choose_weighted(URIS)

def generate_user_agent():
    return choose_weighted(USER_AGENTS)

def generate_bytes():
    """Generate a random number of bytes up to 2 GB."""
    return random.randint(0, 2**31)


def create_log_line(start, end):
    """Create a single log line with random values for each field, including weighted choices."""
    _time = generate_time(start, end).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    bytes_ = generate_bytes()
    http_method = generate_http_method()
    http_version = generate_http_version()
    referrer = generate_referrer()
    status_code = generate_status_code()
    uri = generate_uri()
    user_agent = generate_user_agent()
    return [_time, bytes_, http_method, http_version, referrer, status_code, uri, user_agent]

def create_csv_file(filename, start, end, num_lines):
    """Create a CSV file with specified number of log lines, incorporating weighted random choices."""
    with open(filename, 'w', newline='') as csvfile:
        log_writer = csv.writer(csvfile)
        log_writer.writerow(["_time", "Bytes", "HTTPMethod", "HTTPVersion", "Referrer", "StatusCode", "URI", "UserAgent"])
        for _ in range(num_lines):
            log_writer.writerow(create_log_line(start, end))

def generate_time(start, end):
    """Generate a random datetime between start and end."""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

start_time = datetime(2024, 3, 1)
end_time = datetime(2024, 3, 15)
create_csv_file("weighted_logs.csv", start_time, end_time, 70000)
