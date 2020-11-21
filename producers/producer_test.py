import datetime
from pathlib import Path
import pandas as pd

from models import Line

raw_df = pd.read_csv(
    f"{Path(__file__).parents[0]}/data/cta_stations.csv"
).sort_values("order")

curr_time = datetime.datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
time_step = datetime.timedelta(minutes=5)

line = Line(Line.colors.blue, raw_df[raw_df["blue"]])
line.run(curr_time, time_step)
