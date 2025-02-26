import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz
import math

# Extract event ID from a When2Meet link
def extract_event_id(link):
    match = re.search(r'\?(\d+)-', link)
    if match:
        return match.group(1)
    raise ValueError(f"Invalid When2Meet link: {link}")

# Fetch HTML from a When2Meet URL
def fetch_html(link):
    response = requests.get(link)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Failed to fetch {link}: Status {response.status_code}")

# Extract team name from HTML
def extract_event_name(html):
    soup = BeautifulSoup(html, 'html.parser')
    event_name_div = soup.find('div', id='NewEventNameDiv')
    if event_name_div:
        full_text = event_name_div.get_text(separator=' ', strip=True)
        if 'To invite' in full_text:
            return full_text.split('To invite')[0].strip()
        return full_text.split('\n')[0].strip()
    return "Unknown Event"

# Extract availability data from HTML
def extract_availability_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    script_tags = soup.find_all('script', type='text/javascript')

    time_of_slot = {}
    available_at_slot = {}
    people_names = {}
    people_ids = []

    for script in script_tags:
        if script.string:
            time_matches = re.findall(r'TimeOfSlot\[\s*(\d+)\s*\]\s*=\s*(\d+)\s*;', script.string)
            for index, timestamp in time_matches:
                time_of_slot[int(index)] = int(timestamp)

            avail_matches = re.findall(r'AvailableAtSlot\[\s*(\d+)\s*\]\.push\(\s*(\d+)\s*\);', script.string)
            for index, person_id in avail_matches:
                index = int(index)
                person_id = int(person_id)
                if index not in available_at_slot:
                    available_at_slot[index] = []
                available_at_slot[index].append(person_id)

            name_matches = re.findall(r'PeopleNames\[\s*(\d+)\s*\]\s*=\s*\'([^\']+)\'\s*;\s*PeopleIDs\[\s*\1\s*\]\s*=\s*(\d+)\s*;', script.string)
            for index, name, pid in name_matches:
                people_names[int(pid)] = name
                people_ids.append(int(pid))

    if not time_of_slot or not available_at_slot:
        raise ValueError("Failed to extract availability data")
    return time_of_slot, available_at_slot, people_names, people_ids

# Find the best times from availability data
def find_best_times(time_of_slot, available_at_slot, people_names, timezone='UTC'):
    if not time_of_slot or not available_at_slot:
        return []
    total_participants = len(set().union(*available_at_slot.values()))
    slot_counts = {slot: len(people) for slot, people in available_at_slot.items()}
    max_count = max(slot_counts.values()) if slot_counts else 0

    best_slots = []
    tz = pytz.timezone(timezone)
    for slot, count in slot_counts.items():
        if count == max_count:
            dt = datetime.fromtimestamp(time_of_slot[slot], tz)
            best_slots.append({
                'timestamp': time_of_slot[slot],
                'readable_time': dt.strftime('%a %d %b %Y %I:%M %p %Z'),
            })
    return best_slots

# Find overlapping slots between two teams
def find_overlapping_slots(best_times_a, best_times_b, slot_duration=30, timezone='America/New_York'):
    timestamps_a = set(bt['timestamp'] for bt in best_times_a)
    timestamps_b = set(bt['timestamp'] for bt in best_times_b)
    common_timestamps = timestamps_a.intersection(timestamps_b)

    if not common_timestamps:
        return []

    sorted_timestamps = sorted(common_timestamps)
    slot_seconds = slot_duration * 60
    valid_starts = []
    for i in range(len(sorted_timestamps) - 1):
        if sorted_timestamps[i + 1] - sorted_timestamps[i] == 900:  # 15-minute intervals
            required_slots = math.ceil(slot_duration / 15)
            if all((sorted_timestamps[i] + j * 900) in common_timestamps for j in range(1, required_slots)):
                valid_starts.append(sorted_timestamps[i])

    tz = pytz.timezone(timezone)
    return [
        f"{datetime.fromtimestamp(t, tz).strftime('%a %d %b %Y %I:%M %p')} - "
        f"{datetime.fromtimestamp(t + slot_seconds, tz).strftime('%I:%M %p %Z')}"
        for t in valid_starts
    ]

# Process the list of When2Meet links
def process_when2meet_links(links, timezone='America/New_York', slot_duration=30):
    if len(links) < 2:
        return "Please provide at least two When2Meet links"

    # Process captain's team (first link)
    captain_link = links[0]
    try:
        captain_html = fetch_html(captain_link)
        captain_name = extract_event_name(captain_html)
        time_of_slot, available_at_slot, people_names, _ = extract_availability_data(captain_html)
        captain_best_times = find_best_times(time_of_slot, available_at_slot, people_names, timezone)
    except Exception as e:
        return f"Error processing captain's link {captain_link}: {str(e)}"

    results = []
    for opponent_link in links[1:]:
        try:
            opponent_html = fetch_html(opponent_link)
            opponent_name = extract_event_name(opponent_html)
            time_of_slot, available_at_slot, people_names, _ = extract_availability_data(opponent_html)
            opponent_best_times = find_best_times(time_of_slot, available_at_slot, people_names, timezone)
            overlapping_slots = find_overlapping_slots(captain_best_times, opponent_best_times, slot_duration, timezone)
            if overlapping_slots:
                results.append(f"Overlapping slots between {captain_name} and {opponent_name}:\n" + "\n".join([f"  - {slot}" for slot in overlapping_slots]))
            else:
                results.append(f"No overlapping slots found between {captain_name} and {opponent_name}")
        except Exception as e:
            results.append(f"Error processing {opponent_link}: {str(e)}")
    return "\n\n".join(results)

# Example usage
if __name__ == "__main__":
    when2meet_links = [
        "https://www.when2meet.com/?29202537-8Ue7q",  # Captain's team
        "https://www.when2meet.com/?29263246-ePIGh",  # Opponent 1
        "https://www.when2meet.com/?29202537-8Ue7q"   # Opponent 2
    ]
    slot_duration = 30  # Duration in minutes
    results = process_when2meet_links(when2meet_links, slot_duration=slot_duration)
    print(results)
