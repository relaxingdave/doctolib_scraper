from datetime import date

# enter latest date (inclusive) to check appointments for as string
latest_date = '2023-03-31'
# enter earliest date to check appointments for as a string
min_date = str(date.today())

# how often should doctolib be checked in minutes
loop_time = 1

# url to check appoitnments
url = f"https://www.doctolib.de/availabilities.json?start_date={min_date}&visit_motive_ids=724860&agenda_ids=123720-123721&practice_ids=46104&insurance_sector=public&telehealth=false&limit=5"
