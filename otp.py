import datetime
import json
import os
import pyotp
import re
import time
import typer


f = os.path.join(os.path.dirname(__file__), 'codes.json')
os.system("")  # enables ansi escape characters in terminal

# Function to extract URLs and TOTP secrets
def extract_totp_data(data):
    totp_data = []
    
    for line in data:
        # Find the full URL (assuming it starts with 'otpauth://')
        url_match = re.search(r"(otpauth://[\w\W]+)", line.strip())
        if url_match:
            url = url_match.group(1).split("?")[0]
            # Extract the 'secret' from the URL
            secret_match = re.search(r"(secret=[\w\d]+)", line)
            if secret_match:
                secret = secret_match.group(1)
                totp_data.append(f"{url}?{secret}")  # Append the URL and secret
    return totp_data


def main(file: str = f, search: str = "", runs: int = 5):
    try:
        with open(file) as fh:
            data = json.load(fh)
    except json.decoder.JSONDecodeError:
        with open(file) as fh:
            data = fh.read().split("\n")
    except FileNotFoundError:
        print(f"{file} not found. Going on with demo file...")
        with open("demo.json") as fh:
            data = json.load(fh)
    data = extract_totp_data(data)
    if search:
        search = search.lower()
        sites = [pyotp.parse_uri(d.replace(' ', '')) for d in data 
            if search in d.lower()]
    else:
        sites = [pyotp.parse_uri(d.replace(' ', '')) for d in data]
    lines = len(sites) + 1
    if lines <= 1:
        print("No match found")
        return
    sec = 30
    print("\033[?25l", end="\r")  # Hide cursor - ANSI escape sequences
    print("\033[s", end="\r")     # Save cursor position
    r = "Remaining seconds: "
    try:
        while (runs := runs - 1) >= 0:
            print("-" * 60)
            for site in sites:
                x = f"{site.issuer} ({site.name})"
                otp = site.now()
                print(f"{x: <50}{otp[:3]} {otp[3:]}")

            while True:
                valid = int(sec - datetime.datetime.now().timestamp() % sec)
                print(f"{r: <50} {valid}   ", end='\r')
                if sec - time.time() % sec < 1:
                    time.sleep(1.0 - time.time()%1.0)
                    break
                time.sleep(1.0 - time.time()%1.0)
            print("\033[u", end="\r")  # Restore cursor position
            print(f"\033[{lines}A")
            clean_console(lines)
    except (KeyboardInterrupt, Exception):
        pass
    print(f"\033[?25h")  # display cursor



def clean_console(lines):
    print(f"\033[{lines+1}A")  # Go up n lines
    # for i in range(lines):
    #     print("\033[2K")  # Clear line
    # print(f"\033[{lines+3}A")
    print(chr(27) + "[2J")
        

if __name__ == "__main__":
    typer.run(main)
