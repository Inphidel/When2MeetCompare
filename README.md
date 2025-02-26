# When2MeetCompare

When2MeetCompare is a Python tool designed to find overlapping time slots from multiple When2Meet links where all groups are at their maximum availability. It aggregates availability data from different events and identifies the best times for scheduling meetings across groups, adjustable for your desired meeting duration.

## Usage

### Prerequisites
- Python 3.x
- Required libraries: `requests`, `beautifulsoup4`, `pytz`

Install the dependencies using the following command:
```bash
pip install requests beautifulsoup4 pytz
```
## Running the Script
- Update the Links: Replace the URLs in the when2meet_links list with your own When2Meet URLs.
- Set Meeting Duration: Adjust the slot_duration variable to your desired meeting length in minutes (default is 30 minutes).
- Run the Script: Execute the script to see the overlapping time slots where all groups are available.
Here’s an example of how to use it:

```
when2meet_links = [
    "https://www.when2meet.com/?29202537-8Ue7q",
    "https://www.when2meet.com/?29263246-ePIGh"
]
slot_duration = 30  # Meeting duration in minutes
results = process_when2meet_links(when2meet_links, slot_duration=slot_duration)

if isinstance(results, list):
    print(f"Overlapping {slot_duration}-minute slots with maximum availability:")
    for slot in results:
        print(f"  - {slot}")
else:
    print(results)
```
# Notes
- The slot_duration is adjustable to any number of minutes (e.g., 60 for an hour-long meeting).
- The tool assumes When2Meet uses 15-minute intervals and calculates the required consecutive slots accordingly.
- Timezone defaults to EST (America/New_York), but can be changed by modifying the timezone parameter in the process_when2meet_links function.
