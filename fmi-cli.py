from urllib.request import urlopen
from xml.dom.minidom import parseString
from datetime import datetime, timedelta, UTC
from urllib.error import URLError

paramDict = {
    # Parameter : ( Description, Unit )
    "t2m" : ("Air temperature", "°C"),
    "ws_10min" : ("Wind speed", "m/s"),
    "wg_10min" : ("Gust speed", "m/s"),
    "wd_10min" : ("Wind direction", "°"),
    "rh" : ("Relative humidity", "%"),
    "td" : ("Dew-point", "°C"),
    "r_1h" : ("Rain", "mm"),
    "ri_10min" : ("Rain intensity", "mm/h"),
    "snow_aws" : ("Snow depth", "cm"),
    "p_sea" : ("Air pressure", "hPa"),
    "vis" : ("Visibility", "m"),
    "n_man" : ("Cloud amount", "oktas"),
    "wawa" : ("Present weather", "")
}

params = 't2m,rh,td,n_man'  # See above dictionary keys
place = 'hervanta'          # Your location
timestep = 10               # Difference between start and end in minutes
offset = 10                 # Difference from current time in minutes

# Calculate start and endpoints
end = datetime.now(UTC) - timedelta(minutes=offset)
start = end - timedelta(minutes=timestep)

# Format times to ISO strings
endStr = end.isoformat(sep='T', timespec='seconds').replace('+00:00', 'Z')
startStr = start.isoformat(sep='T', timespec='seconds').replace('+00:00', 'Z')

# Construct URL
urlStr = (f'https://opendata.fmi.fi/wfs?service=WFS'
          f'&version=2.0.0'
          f'&request=getFeature'
          f'&storedquery_id=fmi::observations::weather::multipointcoverage'
          f'&place={place}'
          f'&starttime={startStr}'
          f'&endtime={endStr}'
          f'&timestep={timestep}'
          f'&maxlocations=1'
          f'&parameters={params}')

# Get weather data in XML
try:
    fmiResponse = urlopen(urlStr).read()
except URLError:
    print(f'URL could not be read')
    exit(1)
except:
    print(f'Something went really wrong when opening URL')
    exit(1)
fmiDom = parseString(fmiResponse)

# Get and split data from response
weatherDataElems = fmiDom.getElementsByTagName('gml:doubleOrNilReasonTupleList')
if len(weatherDataElems) == 0:
    print(f'Could not get any data')
    exit(1)
weatherData = weatherDataElems[0].firstChild.nodeValue.split()
splitParams = params.split(',')

# Calculate the length of longest parameter description for formatting
longestDescription = 0
for i in range(len(splitParams)):
    l = len(paramDict[splitParams[i]][0])
    if l > longestDescription:
        longestDescription = l

# Print chosen parameters
for i in range(len(splitParams)):
    # Format and print
    print(f'{paramDict[splitParams[i]][0]:<{longestDescription}}'   # Description
          f' : '                                                    # Separator
          f'{weatherData[i]} '                                               # Value
          f'{paramDict[splitParams[i]][1]}')                        # Unit