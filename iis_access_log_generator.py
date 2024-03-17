import random
from datetime import datetime, timedelta

# Sample data for generating log entries
methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.66",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.66",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0"
]


uris = [
    '/',
    '/about-us',
    '/services/3d-printing',
    '/services/3d-printing/custom-prototypes',
    '/services/3d-printing/model-printing',
    '/services/custom-pcbs',
    '/services/custom-pcbs/design',
    '/services/custom-pcbs/manufacturing',
    '/services/custom-gadget-creation',
    '/services/custom-gadget-creation/idea-development',
    '/services/custom-gadget-creation/product-realization',
    '/shop/computers-accessories',
    '/shop/computers-accessories/laptops/gaming-laptops/alienware-area-51m',
    '/shop/computers-accessories/laptops/business-laptops/lenovo-thinkpad-x1-carbon',
    '/shop/computers-accessories/accessories/keyboards/logitech-mx-keys',
    '/shop/computers-accessories/accessories/mice/razer-deathadder-v2',
    '/shop/smartphones-tablets',
    '/shop/smartphones-tablets/smartphones/android-phones/samsung-galaxy-s21-ultra',
    '/shop/smartphones-tablets/smartphones/iphones/iphone-13-pro-max',
    '/shop/smartphones-tablets/tablets/android-tablets/samsung-galaxy-tab-s7-plus',
    '/shop/smartphones-tablets/tablets/ipads/ipad-pro-m1-chip',
    '/shop/wearables',
    '/shop/wearables/smart-watches/apple-watch-series-7',
    '/shop/wearables/smart-watches/garmin-fenix-6',
    '/shop/wearables/fitness-trackers/fitbit-charge-5',
    '/shop/wearables/fitness-trackers/xiaomi-mi-band-6',
    '/shop/exclusive-gadgets/portable-projectors/anker-nebula-capsule',
    '/shop/exclusive-gadgets/smart-home-devices/google-nest-hub-max',
    '/shop/exclusive-gadgets/drones/dji-mini-2',
    '/blog/industry-insights',
    '/blog/tips-and-tricks',
    '/blog/product-highlights',
    '/login',
    '/register',
    '/user/profile',
    '/user/order-tracking',
    '/user/wishlist',
    '/faqs',
    '/contact-us',
    '/privacy-policy',
    '/upload-image',
    '/terms-of-use'
]

http_versions = ['HTTP/2.0']
status_codes = [200, 302, 404, 403, 500]

uri_referrers = {
    '/': [''],
    '/about-us': ['/', '/contact-us'],
    '/services/3d-printing': ['/', '/services/custom-gadget-creation'],
    '/services/3d-printing/custom-prototypes': ['/services/3d-printing'],
    '/services/3d-printing/model-printing': ['/services/3d-printing'],
    '/services/custom-pcbs': ['/', '/blog/industry-insights'],
    '/services/custom-pcbs/design': ['/services/custom-pcbs'],
    '/services/custom-pcbs/manufacturing': ['/services/custom-pcbs'],
    '/services/custom-gadget-creation': ['/', '/services/3d-printing'],
    '/services/custom-gadget-creation/idea-development': ['/services/custom-gadget-creation'],
    '/services/custom-gadget-creation/product-realization': ['/services/custom-gadget-creation/idea-development'],
    '/shop/computers-accessories': ['/', '/shop'],
    '/shop/computers-accessories/laptops/gaming-laptops/alienware-area-51m': ['/shop/computers-accessories/laptops/gaming-laptops'],
    '/shop/computers-accessories/laptops/business-laptops/lenovo-thinkpad-x1-carbon': ['/shop/computers-accessories/laptops/business-laptops'],
    '/shop/computers-accessories/accessories/keyboards/logitech-mx-keys': ['/shop/computers-accessories/accessories'],
    '/shop/computers-accessories/accessories/mice/razer-deathadder-v2': ['/shop/computers-accessories/accessories'],
    '/shop/smartphones-tablets': ['/', '/shop'],
    '/shop/smartphones-tablets/smartphones/android-phones/samsung-galaxy-s21-ultra': ['/shop/smartphones-tablets/smartphones/android-phones'],
    '/shop/smartphones-tablets/smartphones/iphones/iphone-13-pro-max': ['/shop/smartphones-tablets/smartphones/iphones'],
    '/shop/smartphones-tablets/tablets/android-tablets/samsung-galaxy-tab-s7-plus': ['/shop/smartphones-tablets/tablets/android-tablets'],
    '/shop/smartphones-tablets/tablets/ipads/ipad-pro-m1-chip': ['/shop/smartphones-tablets/tablets/ipads'],
    '/shop/wearables': ['/', '/shop'],
    '/shop/wearables/smart-watches/apple-watch-series-7': ['/shop/wearables/smart-watches'],
    '/shop/wearables/smart-watches/garmin-fenix-6': ['/shop/wearables/smart-watches'],
    '/shop/wearables/fitness-trackers/fitbit-charge-5': ['/shop/wearables/fitness-trackers'],
    '/shop/wearables/fitness-trackers/xiaomi-mi-band-6': ['/shop/wearables/fitness-trackers'],
    '/shop/exclusive-gadgets/portable-projectors/anker-nebula-capsule': ['/shop/exclusive-gadgets/portable-projectors'],
    '/shop/exclusive-gadgets/smart-home-devices/google-nest-hub-max': ['/shop/exclusive-gadgets/smart-home-devices'],
    '/shop/exclusive-gadgets/drones/dji-mini-2': ['/shop/exclusive-gadgets/drones'],
    '/blog/industry-insights': ['/'],
    '/blog/tips-and-tricks': ['/blog/industry-insights'],
    '/blog/product-highlights': ['/blog/tips-and-tricks'],
    '/login': ['/'],
    '/register': ['/login'],
    '/user/profile': ['/login'],
    '/user/order-tracking': ['/user/profile'],
    '/user/wishlist': ['/user/profile'],
    '/faqs': ['/'],
    '/contact-us': ['/'],
    '/privacy-policy': ['/'],
    '/terms-of-use': ['/'],
    '/upload-image': ['/user/profile']
}
shop_name="Kingizmos"
for uri in uri_referrers:
    uri_referrers[uri] = [f"http://{shop_name}.com" + path for path in uri_referrers[uri]]

# Function to generate a random timestamp
def generate_timestamp(previous_timestamp):
    # Increment by a random number of seconds, ensuring logs are sequential
    increment = timedelta(seconds=random.randint(1, 10))
    new_timestamp = previous_timestamp + increment
    # Ensure the new timestamp does not exceed the end date
    if new_timestamp > end_date:
        return None
    return new_timestamp

def select_status_code(uri, method):
    # Simulating special cases for certain URIs and methods
    if uri not in uris:
        return 404  # Not Found for URIs not listed
    elif '/admin' in uri or '/user/profile' in uri and method == 'POST':
        return 403  # Forbidden for specific admin or sensitive user actions
    elif '/services/custom-pcbs/manufacturing' in uri:
        # Simulate occasional server error on a complex service
        return random.choice([200, 500])
    return 200  # OK for all other cases

def generate_referrer(uri):
    possible_referrers = uri_referrers.get(uri, [''])
    if possible_referrers == ['']:
        return "-"  # Indicate no referrer if it's an invalid path
    return random.choice(possible_referrers)

def generate_ip_addresses(ips_count):
    ips = []
    for _ in range(ips_count):
        # Generate random IP addresses
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        ips.append(ip)
    return ips

def generate_invalid_uri():
    invalid_paths = [
        "/admin",
        "/config",
        "/db",
        "/api/private",
        "/secure"
    ]
    random_invalid = random.choice(invalid_paths) + "/" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=5))
    return random_invalid

# Function to randomly choose between a valid URI and an invalid one
def choose_uri():
    if random.random() < 0.1:  # 10% chance to pick an invalid URI
        return generate_invalid_uri()
    else:
        return random.choice(uris)
# Updated function to generate a log entry
    
def generate_log_entries(filename, start_date, end_date, num_entries):
    current_timestamp = start_date
    with open(filename, 'w') as f:
        for _ in range(num_entries):
            if not current_timestamp or current_timestamp > end_date:
                break  # Stop if the current timestamp exceeds the end date
            ip = random.choice(ips)
            user_agent = random.choice(user_agents)
            method = random.choice(methods)
            uri = choose_uri()
            http_version = random.choice(http_versions)
            status_code = select_status_code(uri, method)
            response_size = random.randint(400, 2000)
            referrer = generate_referrer(uri)
            log_entry = f'{ip} - - [{current_timestamp.strftime("%d/%b/%Y:%H:%M:%S +0200")}] "{method} {uri} {http_version}" {status_code} {response_size} "{referrer}" "{user_agent}"'
            f.write(log_entry + '\n')
            current_timestamp = generate_timestamp(current_timestamp)  # Update timestamp for next entry


# Example usage
start_date = datetime(2023, 12, 15, 17, 30)
end_date = datetime(2024, 1, 3, 17, 36)
ips = generate_ip_addresses(1000)

generate_log_entries('iis_access.log', start_date, end_date, 1000000)