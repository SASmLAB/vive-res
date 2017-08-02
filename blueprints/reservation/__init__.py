from flask import Blueprint
from flask_caching import Cache
from icalendar import Calendar
import re
import requests

blueprint = Blueprint('reservation', __name__, url_prefix='/reservation')

cache = Cache(config={'CACHE_TYPE': 'redis'})


@cache.cached(timeout=86400, key_prefix='schedule')
def get_schedule():
    feed_url = 'https://sasaustin.myschoolapp.com/podium/feed/iCal.aspx?z=CK4yWdgjtxOilqm%2fCRUWMbVZh3IOV0oduVex%2fk28KE1T1iqjxj%2foZtxpgB8BoGMYl4fNBxr8Rdhq6YAW5qhTyA%3d%3d'

    ical_raw = requests.get(feed_url, headers={'User-agent': 'Mozilla/5.0'}).text  # header fakes out their security
    calendar = Calendar.from_ical(ical_raw)

    schedule = {
        'A': ['A', 'B', 'C', 'D', 'E', 'F', 'X'],
        'B': ['B', 'C', 'D', 'E', 'F', 'G', 'X'],
        'C': ['C', 'D', 'E', 'F', 'G', 'A', 'X'],
        'D': ['D', 'E', 'F', 'G', 'A', 'B', 'X'],
        'E': ['E', 'F', 'G', 'A', 'B', 'C', 'X'],
        'F': ['F', 'G', 'A', 'B', 'C', 'D', 'X'],
        'G': ['G', 'A', 'B', 'C', 'D', 'E', 'X']
    }

    days = {}
    pattern = re.compile(".\/.\/([A-G])")
    for event in calendar.walk('vevent'):
        match = pattern.search(str(event['summary']))
        if match:
            letter_day = match.group(1)
            days[event['dtstart'].dt] = schedule[letter_day]

    return days


from .views import index, create, calendar, admin
