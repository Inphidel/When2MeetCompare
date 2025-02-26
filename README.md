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

![Example](https://raw.githubusercontent.com/Inphidel/When2MeetCompare/main/Compare.png)

Example URLS:
```
when2meet_links = [
        "https://www.when2meet.com/?29202537-8Ue7q",  # Captain's team
        "https://www.when2meet.com/?29263246-ePIGh",  # Opponent 1
        "https://www.when2meet.com/?29202537-8Ue7q"   # Opponent 2
    ]
```
Output:
```
Overlapping slots between Howlers Week 1 and Other Test:
  - Fri 28 Feb 2025 08:15 PM - 08:45 PM EST
  - Fri 28 Feb 2025 08:30 PM - 09:00 PM EST
  - Fri 28 Feb 2025 08:45 PM - 09:15 PM EST
  - Fri 28 Feb 2025 09:00 PM - 09:30 PM EST
  - Fri 28 Feb 2025 09:15 PM - 09:45 PM EST
  - Fri 28 Feb 2025 09:30 PM - 10:00 PM EST
  - Fri 28 Feb 2025 09:45 PM - 10:15 PM EST
  - Fri 28 Feb 2025 10:00 PM - 10:30 PM EST
  - Sat 01 Mar 2025 08:15 PM - 08:45 PM EST
  - Sat 01 Mar 2025 08:30 PM - 09:00 PM EST
  - Sat 01 Mar 2025 08:45 PM - 09:15 PM EST
  - Sat 01 Mar 2025 09:00 PM - 09:30 PM EST
  - Sat 01 Mar 2025 09:15 PM - 09:45 PM EST
  - Sat 01 Mar 2025 09:30 PM - 10:00 PM EST
  - Sat 01 Mar 2025 09:45 PM - 10:15 PM EST
  - Sat 01 Mar 2025 10:00 PM - 10:30 PM EST

Overlapping slots between Howlers Week 1 and Howlers Week 1:
  - Fri 28 Feb 2025 07:00 PM - 07:30 PM EST
  - Fri 28 Feb 2025 07:15 PM - 07:45 PM EST
  - Fri 28 Feb 2025 07:30 PM - 08:00 PM EST
  - Fri 28 Feb 2025 07:45 PM - 08:15 PM EST
  - Fri 28 Feb 2025 08:00 PM - 08:30 PM EST
  - Fri 28 Feb 2025 08:15 PM - 08:45 PM EST
  - Fri 28 Feb 2025 08:30 PM - 09:00 PM EST
  - Fri 28 Feb 2025 08:45 PM - 09:15 PM EST
  - Fri 28 Feb 2025 09:00 PM - 09:30 PM EST
  - Fri 28 Feb 2025 09:15 PM - 09:45 PM EST
  - Fri 28 Feb 2025 09:30 PM - 10:00 PM EST
  - Fri 28 Feb 2025 09:45 PM - 10:15 PM EST
  - Fri 28 Feb 2025 10:00 PM - 10:30 PM EST
  - Fri 28 Feb 2025 10:15 PM - 10:45 PM EST
  - Fri 28 Feb 2025 10:30 PM - 11:00 PM EST
  - Sat 01 Mar 2025 07:00 PM - 07:30 PM EST
  - Sat 01 Mar 2025 07:15 PM - 07:45 PM EST
  - Sat 01 Mar 2025 07:30 PM - 08:00 PM EST
  - Sat 01 Mar 2025 07:45 PM - 08:15 PM EST
  - Sat 01 Mar 2025 08:00 PM - 08:30 PM EST
  - Sat 01 Mar 2025 08:15 PM - 08:45 PM EST
  - Sat 01 Mar 2025 08:30 PM - 09:00 PM EST
  - Sat 01 Mar 2025 08:45 PM - 09:15 PM EST
  - Sat 01 Mar 2025 09:00 PM - 09:30 PM EST
  - Sat 01 Mar 2025 09:15 PM - 09:45 PM EST
  - Sat 01 Mar 2025 09:30 PM - 10:00 PM EST
  - Sat 01 Mar 2025 09:45 PM - 10:15 PM EST
  - Sat 01 Mar 2025 10:00 PM - 10:30 PM EST
  - Sat 01 Mar 2025 10:15 PM - 10:45 PM EST
  - Sat 01 Mar 2025 10:30 PM - 11:00 PM EST

```
# Notes
- The slot_duration is adjustable to any number of minutes (e.g., 60 for an hour-long meeting).
- The tool assumes When2Meet uses 15-minute intervals and calculates the required consecutive slots accordingly.
- Timezone defaults to EST (America/New_York), but can be changed by modifying the timezone parameter in the process_when2meet_links function.
