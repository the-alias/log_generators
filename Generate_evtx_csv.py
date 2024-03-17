import csv
import random
from datetime import datetime, timedelta

# Constants
EVENT_IDS = [
    (4624, 'LoginSuccess', 30),              # Successful logon
    (4625, 'LoginFailed', 5),               # Logon failure
    (4634, 'Logout', 20),                    # An account was logged off
    (4672, 'SpecialPrivilegesAssigned', 4),  # Special privileges assigned to new logon
    (4740, 'AccountLockedOut', 3),           # Account locked out
    (4633, 'AccountUnlocked', 2),            # An account was unlocked
    (4647, 'UserInitiatedLogoff', 25),       # User initiated logoff
    (4662, 'OperationPerformedOnObject', 1), # An operation was performed on an object
    (4673, 'PrivilegedServiceCalled', 2),    # A privileged service was called
    (4688, 'ProcessCreated', 70),            # A new process has been created, very common
    (4697, 'ServiceInstalled', 1),           # A service was installed in the system
    (4720, 'UserAccountCreated', 1),         # A user account was created
    (4728, 'MemberAddedToGlobalGroup', 1),   # A member was added to a security-enabled global group
    (4732, 'MemberAddedToLocalGroup', 1),    # A member was added to a security-enabled local group
    (4741, 'ComputerAccountCreated', 1),     # A computer account was created
    (4776, 'CredentialValidation', 4),       # The computer attempted to validate the credentials for an account
    (6005, 'EventLogStarted', 2),            # The Event Log service was started
    (6006, 'EventLogStopped', 2),            # The Event Log service was stopped
    (6013, 'SystemUptime', 3),               # System uptime
    (7026, 'ServiceControlManagerError', 1), # Service control manager encountered an error when starting services
    (7040, 'ServiceStartTypeChanged', 1),    # Service start type was changed
    (1000, 'ApplicationError', 3),           # Application error
    (1001, 'ApplicationHang', 3),            # Application hang
    (1002, 'ApplicationTerminated', 2)       # Application hang and terminated
]


DOMAINS = ['WINSEC']
USERNAMES = ['AdminUser', 'Developer', 'HRUser', 'ServiceAccount'] + ['User'+str(i) for i in range(1, 21)]  # 20 normal users
MACHINES_AND_IPS = {
    # Servers
    'SRV001': '192.168.1.100', 'SRV002': '192.168.1.101', 'SRV003': '192.168.1.102',
    # Desktops
    'DESK001': '192.168.2.50', 'DESK002': '192.168.2.51', 'DESK003': '192.168.2.52',
    'DESK004': '192.168.2.53', 'DESK005': '192.168.2.54',
    # Laptops
    'LAP001': '192.168.2.60', 'LAP002': '192.168.2.61', 'LAP003': '192.168.2.62'
}


def generate_event_id_action():
    """Choose an event ID and corresponding action based on weights."""
    event_id, action = choose_weighted(EVENT_IDS)
    return event_id, action


def generate_domain():
    """Randomly choose a domain."""
    return random.choice(DOMAINS)

def generate_username():
    """Randomly choose a username."""
    return random.choice(USERNAMES)

def generate_machine_and_ip():
    """Randomly choose a machine and its corresponding source IP."""
    machine_name = random.choice(list(MACHINES_AND_IPS.keys()))
    source_ip = MACHINES_AND_IPS[machine_name]
    return machine_name, source_ip

def choose_weighted(options):
    """Choose an option based on weights, returning both event ID and action."""
    event_ids, actions, weights = zip(*options)
    chosen_event = random.choices(
        population=list(zip(event_ids, actions)), 
        weights=weights, 
        k=1)[0]
    return chosen_event  # chosen_event is a tuple of (event_id, action)


def generate_time(start, end):
    """Generate a random datetime between start and end."""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def create_evtx_log_line(start, end):
    _time = generate_time(start, end).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    event_id, action = generate_event_id_action()
    machine_name, source_ip = generate_machine_and_ip()
    domain = generate_domain()
    username = generate_username()
    return [_time, event_id, action, source_ip, domain, username, machine_name]

def create_csv_file(filename, start, end, num_lines):
    """Create a CSV file with specified number of EVTX log lines."""
    headers = ["_time", "EVENTID", "Action", "SourceIP", "Domain", "Username", "MachineName"]
    with open(filename, 'w', newline='') as csvfile:
        log_writer = csv.writer(csvfile)
        log_writer.writerow(headers)
        for _ in range(num_lines):
            log_writer.writerow(create_evtx_log_line(start, end))

# Example usage
start_time = datetime(2024, 3, 1, 10, 0, 0)
end_time = datetime(2024, 3, 14, 10, 12, 0)
create_csv_file("evtx_logs.csv", start_time, end_time, 70000)  # Create a CSV file with 12 EVTX log lines
