from _datetime import datetime

import tzlocal


def convert_to_iso_timestamp(timestamp_string):
    timestamp = datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M")
    timestamp_iso = timestamp.astimezone(tzlocal.get_localzone()).isoformat(timespec='milliseconds')
    return timestamp_iso
