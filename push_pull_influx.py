from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import os

def pull_from_influx(url, token, org, bucket, measurement, filter_dictionary, ignore_cols_list, normalise_timestamp):

    client = InfluxDBClient(url=url, token=token, enable_gzip=True, org=org, debug=False, verify_ssl = False, timeout=300000)
    query_api = client.query_api()

    key = list(filter_dictionary.keys())[0]
    value = filter_dictionary.get(key)
    ignore_cols_list.extend(["_start", "_stop", "_measurement", "table", "result"])

    query = (f'from(bucket: "{bucket}")'
        f' |> range(start: -1y) |> filter(fn: (r) => r["_measurement"] == "{measurement}")'
        f' |> filter(fn: (r) => r["{key}"] == "{value}")'
        f' |> drop(columns: {ignore_cols_list})'
        ' |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
    )

    raw_data = query_api.query_data_frame(query, org=org)
    data = clean_data(raw_data, normalise_timestamp)

    return data


def clean_data (raw_data, normalise_timestamp):
    
    if 'result' in data.columns:
        data = data.drop("result", axis = 1)

    if 'table' in data.columns:
        data = data.drop("table", axis =1)

    if normalise_timestamp:
        to_unix = lambda x: x.value / 1000000
        data['Timestamp'] = data['_time'].apply(to_unix)
        data["Timestamp"] = data["Timestamp"] - data["Timestamp"].iloc[0]
        data = data.drop(['_time'], axis=1)

    return data


def push_to_influx(url, token, org, bucket, measurement, tables, tags_list):

    with InfluxDBClient(url=url, token=token, org=org, debug=False, verify_ssl = False, timeout=3000000) as client:
        
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket = bucket, record=tables, data_frame_measurement_name=measurement,
                        data_frame_tag_columns=tags_list)

                        