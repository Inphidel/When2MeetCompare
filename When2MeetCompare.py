import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import math

# Function to extract event ID from a When2Meet link
def extract_event_id(link):
    match = re.search(r'\?(\d+)-', link)
    if match:
        return match.group(1)
    raise ValueError(f"Invalid When2Meet link: {link}")

# Function to fetch HTML from a When2Meet URL
def fetch_html(link):
    response = requests.get(link)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Failed to fetch {link}: Status {response.status_code}")

# Function to extract availability data from HTML
def extract_availability_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    script_tags = soup.find_all('script', type='text/javascript')

    time_of_slot = {}
    available_at_slot = {}

    for script in script_tags:
        if script.string:
            # Extract TimeOfSlot: maps slot index to timestamp
            time_matches = re.findall(r'TimeOfSlot\[(\d+)\]=(\d+);', script.string)
            for index, timestamp in time_matches:
                time_of_slot[int(index)] = int(timestamp)

            # Extract AvailableAtSlot: maps slot index to list of person IDs
            avail_matches = re.findall(r'AvailableAtSlot\[(\d+)\]\.push\((\d+)\);', script.string)
            for index, person_id in avail_matches:
                index = int(index)
                person_id = int(person_id)
                if index not in available_at_slot:
                    available_at_slot[index] = []
                available_at_slot[index].append(person_id)

    return time_of_slot, available_at_slot

# Function to find timestamps where availability is maximum for a link
def find_max_availability_slots(time_of_slot, available_at_slot):
    if not available_at_slot:
        return set()
    # Find the maximum number of people available in any slot
    max_avail = max(len(available_at_slot[slot]) for slot in available_at_slot)
    # Collect timestamps where availability equals the maximum
    max_timestamps = {time_of_slot[slot] for slot in available_at_slot if len(available_at_slot[slot]) == max_avail}
    return max_timestamps

# Function to find valid starting times for meetings of specified duration
def find_valid_starts(intersection_set, slot_duration=30, slot_interval=15):
    # Calculate number of consecutive 15-minute slots needed
    num_slots = math.ceil(slot_duration / slot_interval)
    slot_offset = slot_interval * 60  # Convert interval to seconds (15 min = 900 sec)
    sorted_intersection = sorted(intersection_set)
    valid_starts = []
    # Check each timestamp to see if the required consecutive slots are available
    for t in sorted_intersection:
        if all((t + i * slot_offset) in intersection_set for i in range(1, num_slots)):
            valid_starts.append(t)
    return valid_starts

# Main function to process multiple When2Meet links and find overlapping slots
def process_when2meet_links(links, timezone='America/New_York', slot_duration=30):
    all_max_timestamps = []
    for link in links:
        try:
            html = fetch_html(link)
            time_of_slot, available_at_slot = extract_availability_data(html)
            max_timestamps = find_max_availability_slots(time_of_slot, available_at_slot)
            all_max_timestamps.append(max_timestamps)
        except Exception as e:
            print(f"Error processing {link}: {e}")
            continue

    # Check if any data was successfully processed
    if not all_max_timestamps:
        return "No valid data found for any link"

    # Find the intersection of maximum availability slots across all links
    intersection_set = set.intersection(*all_max_timestamps)
    if not intersection_set:
        return "No overlapping times found"

    # Find valid starting times for the specified meeting duration
    valid_starts = find_valid_starts(intersection_set, slot_duration=slot_duration)
    if not valid_starts:
        return f"No overlapping slots for {slot_duration}-minute meetings"

    # Convert timestamps to readable format with start and end times
    tz = pytz.timezone(timezone)
    readable_slots = [
        f"{datetime.fromtimestamp(t, tz).strftime('%a %d %b %Y %I:%M %p')} - "
        f"{datetime.fromtimestamp(t + slot_duration*60, tz).strftime('%I:%M %p %Z')}"
        for t in sorted(valid_starts)
    ]
    return readable_slots

# Example usage
if __name__ == "__main__":
    when2meet_links = [
        "https://www.when2meet.com/?29202537-8Ue7q",
        "https://www.when2meet.com/?29263246-ePIGh"
    ]
    slot_duration = 30  # Meeting duration in minutes, adjustable
    results = process_when2meet_links(when2meet_links, slot_duration=slot_duration)

    if isinstance(results, list):
        print(f"Overlapping {slot_duration}-minute slots with maximum availability:")
        for slot in results:
            print(f"  - {slot}")
    else:
        print(results)
