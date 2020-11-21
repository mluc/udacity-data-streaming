import datetime

from models import Weather

curr_time = datetime.datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

weather = Weather(curr_time.month)
weather.run(curr_time.month)
