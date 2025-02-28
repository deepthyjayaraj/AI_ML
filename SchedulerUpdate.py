import json
from datetime import datetime, timedelta

# Sample JSON schedule
schedule_json = {
    "schedule": [
        {"day": "Sunday", "start_time": "10:00 AM", "duration": 1140},
        {"day": "Monday", "start_time": "05:00 AM", "duration": 1320},
        {"day": "Tuesday", "start_time": "05:00 AM", "duration": 1320},
        {"day": "Wednesday", "start_time": "05:00 AM", "duration": 1320},
        {"day": "Thursday", "start_time": "05:00 AM", "duration": 1320},
        {"day": "Friday", "start_time": "05:00 AM", "duration": 1320},
        {"day": "Saturday", "start_time": "05:00 AM", "duration": 1320}
    ]
}

# Define outage time
outage_start = "12:00 PM"
outage_duration = 120  # minutes

# Convert outage start time to datetime
outage_start_time = datetime.strptime(outage_start, "%I:%M %p")
outage_end_time = outage_start_time + timedelta(minutes=outage_duration)

# Create new schedule dictionary
adjusted_schedule = {"schedule": []}

try:
    # Process each day's schedule
    for day_schedule in schedule_json["schedule"]:
        start_time = datetime.strptime(day_schedule["start_time"], "%I:%M %p")
        end_time = start_time + timedelta(minutes=day_schedule["duration"])

        # Create a copy of the current schedule
        new_schedule = day_schedule.copy()

        # If schedule overlaps with outage
        if day_schedule["day"] == "Sunday":
            if start_time < outage_start_time and end_time > outage_start_time:
                # Adjust the duration to end at outage start
                new_duration = (outage_start_time - start_time).seconds // 60
                new_schedule["duration"] = new_duration

                # Create a second schedule segment after the outage
                post_outage = day_schedule.copy()
                post_outage["start_time"] = outage_end_time.strftime("%I:%M %p")
                post_outage["duration"] = (end_time - outage_end_time).seconds // 60
                adjusted_schedule["schedule"].append(post_outage)

        adjusted_schedule["schedule"].append(new_schedule)

    # Write to files with explicit path
    with open('C:/temp/original_schedule.json', 'w') as f:
        json.dump(schedule_json, f, indent=4)
        print("Original schedule written successfully")

    with open('C:/temp/adjusted_schedule.json', 'w') as f:
        json.dump(adjusted_schedule, f, indent=4)
        print("Adjusted schedule written successfully")

except Exception as e:
    print(f"Error occurred: {e}")

print("Program completed")