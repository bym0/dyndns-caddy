import os
import time
import socket

dyndns_domain = os.getenv('DYNDNS_DOMAIN')

print(f"Starting dyndns-resolver for {dyndns_domain}")

if not dyndns_domain:
    raise ValueError('DYNDNS_DOMAIN environment variable is not set')

def resolve_dyndns():
    try:
        resolved_ip = socket.gethostbyname(dyndns_domain)
        with open('/app/dyndns.conf', 'w') as f:
            f.write(f"@allowed_ip remote_ip {resolved_ip}\n")
            f.write("abort not @allowed_ip\n")
        print(f"Resolved {dyndns_domain} to {resolved_ip} and updated configuration. Will retry in 5 minutes.")
    except socket.gaierror as e:
        print(f"Error resolving {dyndns_domain}: {e}")

if __name__ == "__main__":
    while True:
        resolve_dyndns()
        time.sleep(300)