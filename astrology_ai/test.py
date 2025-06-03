from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

# Example birth details
date = '1995-06-15'       # YYYY-MM-DD
time = '14:30'            # HH:MM (24hr)
location = GeoPos('28.6139', '77.2090')  # Delhi, India

# Create datetime object
dt = Datetime(date, time, '+05:30')  # Local timezone offset

# Create chart
chart = Chart(dt, location)

# Print planetary positions
for obj in [const.SUN, const.MOON, const.MERCURY, const.MARS,
            const.VENUS, const.JUPITER, const.SATURN,
            const.ASC, const.MC]:
    print(f"{obj}: {chart[obj].sign} at {chart[obj].lon}")
