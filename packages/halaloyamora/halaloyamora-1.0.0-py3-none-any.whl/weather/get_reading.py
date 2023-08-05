import requests
import sys 
import datetime

APIKEY="http://api.openweathermap.org/data/2.5/forecast?zip=85051,de&APPID=73427c9ce4ba48bcf631342683697c7a"



def get_next_5days_reading(verbose=True):
    """
    Function get next 5days temprature readings of Ingolstadt, Germany. 
    """

    response = requests.get(url=APIKEY)
    

    # check api response 
    if response.status_code != 200:
        print(f'failed with status code {response.status_code}')
        sys.exit()
        
    # get response in dictinaory 
    response = response.json()

    output = dict()

    # save results in a dictionary 
    for i in range(0, 40, 8):
        # date
        date = response['list'][i]['dt']
        date = datetime.datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')

        # temp reading in celuious 
        reading = response['list'][i]['main']['temp']
        reading = reading - 273.15

        if verbose: print(f'Read temprature of {date}...{reading:.2f}°')

        # save results 
        output[date] = reading
    
    return output


if __name__ == "__main__":
    get_next_5days_reading()
