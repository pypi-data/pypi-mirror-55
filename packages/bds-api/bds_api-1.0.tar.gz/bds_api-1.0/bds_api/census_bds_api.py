import requests
import pandas as pd

def get(variables, filters):

    if len(variables) > 1:
        x = (','.join(variables))
    else:
        x = variables[0]

    params_temp = []
    for key, value in filters.items():
        if key == 'state': # for whatever fucking reason 'state' has it's own identifier
            filter = key+':'+value
        else:
            filter = key+'='+value
        params_temp.append(filter)
    if len(params_temp) > 1:
        y = ('&'.join(params_temp))
    else:
        y = params_temp[0]

    request_url = f'https://api.census.gov/data/timeseries/bds/firms?get={x}&for={y}'
    content = requests.get(request_url)
    if content.status_code != 200: #handle errors
        error = content.text
        print(error)
    else:
        raw_data = content.json()
        processed_data = pd.DataFrame(list(raw_data))
        processed_data.columns = processed_data.iloc[0]
        processed_data = processed_data.drop(processed_data.index[0])
        return processed_data
