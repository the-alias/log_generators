import csv
import random
import time
from datetime import datetime, timedelta
from datetime import datetime, timedelta

# Expanded Constants and weights for log types
LOG_TYPES = [
    ('System', 15),
    ('Cron', 20),
    ('SSHD', 15),
    ('Kernel', 10),
    ('Nginx', 10),
    ('CRON_CMD', 15),
    ('Systemd', 10),
    ('Sudo', 5),
    ('PackageKit', 5),
    ('Postfix', 5),
    ('UserAdd', 1),
    ('Network', 4),
    ('Session', 10)
]

# Expanded example components for each log type
COMMANDS = [
    'cd / && run-parts --report /etc/cron.hourly',
    '/bin/systemctl restart nginx',
    'apt update && apt upgrade -y',
    'php /var/www/html/scheduled_task.php',
    'echo "Hello World" >> /var/log/custom.log',
    'mysqldump --all-databases > /backup/dbs.sql'
]
CRON_COMMANDS = [
    'cd / && run-parts --report /etc/cron.hourly',
    '/bin/systemctl restart nginx',
    'apt update && apt upgrade -y',
    'php /var/www/html/scheduled_task.php',
    'echo "Hello World" >> /var/log/custom.log',
    'mysqldump --all-databases > /backup/dbs.sql'
]
CRON_USERS = ['root', 'user1', 'user2', 'www-data', 'jdoe', 'jane', 'backup', 'deploy'] 

USERS = ['root', 'www-data', 'jdoe', 'jane', 'backup', 'deploy']
HOSTNAMES = ['server01', 'server02', 'web01', 'db01', 'mail01', 'backup01']
IP_ADDRESSES = ['192.168.1.105', '192.168.1.120', '127.0.0.1', '10.0.0.5', '10.0.0.15']


# Helper functions to generate log components
def generate_timestamp(current_time):
    """Generate a timestamp, incrementally increasing from the current time with a random amount of seconds or minutes."""
    # Decide randomly whether to add seconds or minutes
    if random.choice(['seconds', 'minutes']) == 'seconds':
        # Add a random number of seconds, say up to 120 seconds (2 minutes)
        increment = timedelta(seconds=random.randint(1, 120))
    else:
        # Add a random number of minutes, say up to 5 minutes
        increment = timedelta(minutes=random.randint(1, 5))
    
    new_time = current_time + increment
    return new_time.strftime("%b %d %H:%M:%S")


def generate_hostname():
    """Randomly choose a hostname."""
    return random.choice(HOSTNAMES)

def generate_process():
    """Randomly choose a process based on predefined weights."""
    processes, weights = zip(*LOG_TYPES)
    process = random.choices(processes, weights)[0]
    return process

def generate_cron_message():
    """Generate a message for cron log entries."""
    user = random.choice(CRON_USERS)
    command = random.choice(CRON_COMMANDS)
    return f'({user}) CMD ({command})'

def generate_sshd_log(hostname):
    ip_address = random.choice(IP_ADDRESSES)
    user = random.choice(['user=guest', 'user=root', 'user unknown'])
    log_parts = [
        f"logname= uid=0 euid=0 tty=NODEVssh ruser= rhost={ip_address}",
        user
    ]
    return " ".join(log_parts)

def generate_message(process,hostname):
    """Generate a message based on the process type."""
    if process == 'System':
        return 'Started Cleanup of Temporary Directories.'
    elif process == 'Cron':
        return f'CRON job scheduled for user {random.choice(USERS)}'
    if process == 'SSHD':
        return f"authentication failure; {generate_sshd_log(hostname)}"
    elif process == 'Kernel':
        return f'Kernel alert: device eth0 entered promiscuous mode'
    elif process == 'Nginx':
        return f'Nginx access: {random.choice(IP_ADDRESSES)} - - [17/Mar/2024:08:27:12 +0000] "GET / HTTP/1.1" 200 612'
    elif process == 'CRON_CMD':
        return generate_cron_message()
    elif process == 'Systemd':
        return f'Systemd started service {random.choice(["nginx", "mysql", "apache2"])}'
    elif process == 'Sudo':
        return f'{random.choice(USERS)} executed sudo command'
    elif process == 'PackageKit':
        return f'PackageKit: software update check'
    elif process == 'Postfix':
        return f'Postfix: mail queued for delivery'
    elif process == 'UserAdd':
        return f'New user account {random.choice(USERS)} added'
    elif process == 'Network':
        return f'NetworkManager: interface eth0 connected'
    elif process == 'Session':
        user = random.choice(USERS)
        action = random.choice(['opened', 'closed'])
        return f"session {action} for user {user} by (uid=0)"

def generate_log_line(start_time):
    timestamp = generate_timestamp(start_time)
    hostname = generate_hostname()
    process = generate_process()
    message = generate_message(process, hostname)
    return f'{timestamp} {hostname} {process}[{random.randint(1000, 9999)}]: {message}'


def create_syslog_file(filename, start_date, end_date, time_increment_seconds=60):
    """Create a syslog file with specified number of lines between start_date and end_date."""
    current_time = start_date
    with open(filename, 'w') as f:
        while current_time <= end_date:
            log_line = generate_log_line(current_time)
            f.write(log_line + '\n')
            # Increment the time for the next log entry
            current_time += timedelta(seconds=time_increment_seconds)



# Example usage
start_date = datetime(2023, 9, 1, 0, 0, 0)
end_date = datetime(2024, 3, 2, 23, 59, 59)
create_syslog_file("syslog.txt", start_date, end_date)  # Create a syslog file with 100 lines
