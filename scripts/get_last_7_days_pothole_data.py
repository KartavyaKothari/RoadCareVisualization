import pandas as pd
from datetime import datetime, timedelta

file_name = r'tmp/predictions_dump.txt'

def run():
    highLat = 19.14029877339673
    lowLat = 19.104229897359918

    highLng = 72.93203320151837
    lowLng = 72.84680143131232

    predictions_dump = pd.read_json (file_name)

    latFilter = predictions_dump[predictions_dump['lat']<highLat]
    data = latFilter[latFilter['lat']>lowLat]

    lngFilter = data[data['lng']>lowLng]
    data = lngFilter[lngFilter['lng']<highLng]
    predictions_dump = data

    last_one_week_data=predictions_dump[predictions_dump['date']>(predictions_dump['date'].max()-timedelta(days=7))]
    last_one_week_data.to_json(r'tmp/last_one_week_data.json')