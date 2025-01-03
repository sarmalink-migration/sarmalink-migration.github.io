import requests
import time
from datetime import datetime

# URL of the file
url = "http://your.thermom.ip.addr/sarmalink_pull.txt"

def normalize_date(date_str):
    """
    Normalize the DAT string to a standard format (YYYY-MM-DD HH:MM:SS).
    Removes the day of the week and timezone abbreviation.
    """
    # Split the date string into parts
    parts = date_str.split()
    if len(parts) == 6:
        # Exclude index 0 (day) and 4 (timezone)
        parts = [parts[1], parts[2], parts[3], parts[5]]
        date_without_day_and_tz = " ".join(parts)
        return datetime.strptime(date_without_day_and_tz, "%b %d %H:%M:%S %Y").strftime("%Y-%m-%d %H:%M:%S")

def parse_content(content_str):
    """
    Parse the fetched content into a structured dictionary.
    """
    content_lines = content_str.splitlines()
    result = {}
    rom, raw = [], []

    for line in content_lines:
        if line.startswith("DAT"):
            raw_date = line.split(" ", 1)[1]
            result["DAT"] = normalize_date(raw_date)
        elif line.startswith("SAMPLE"):
            sample = line.split(" ", 1)[1]
            result["SAMPLE"] = sample
        elif line.startswith("ROM"):
            rom.append(line.split(" ")[1])
        elif line.startswith("RAW"):
            raw.append(line.split(" ")[1])

    result["ROM"] = rom
    result["RAW"] = raw
    return result

def fetch_and_store_data():
    try:
        # Fetch the file
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        content = response.text.strip()
        parsed_data = parse_content(content)

        rom_list = parsed_data["ROM"]
        raw_list = parsed_data["RAW"]
        sample = parsed_data["SAMPLE"]

        # Ensure data integrity
        if len(rom_list) == len(raw_list):
            if fetch_and_store_data.previous_sample == sample:
                print("No update since the last fetch.")
                return
            else:
                fetch_and_store_data.previous_sample = sample
                for i in range(len(rom_list)):
                    filename = f"ROM_{rom_list[i]}.txt"
                    with open(filename, "a") as file:
                        file.write(f"{parsed_data['DAT']}\t{sample}\t{raw_list[i]}\n")
                    print(f"Data saved to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Initialize previous_sample to track updates
fetch_and_store_data.previous_sample = None

if __name__ == "__main__":
    # Run every 30 seconds
    while True:
        fetch_and_store_data()
        for _ in range(30):
            time.sleep(1)
            print(".", end='', flush=True)  # Ensure immediate output
        print()
