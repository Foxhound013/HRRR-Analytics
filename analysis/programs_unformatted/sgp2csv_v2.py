# this script is version 2 of the SingleGridPt2csv script previously used in the compilation of data.
# The point of this script is to check in a given directory and convert csv files of the HRRR forecast
# into a format that is much more conducive to analysis and plotting. This script was rebuilt in order
# to remove all manual processes that were involved in the previous work flow.
import pandas as pd
import numpy as np

def getRow(file):
    df = pd.read_csv(file, header=None, names=['lon', 'lat', 'delimit'])

    # Split on delimiters
    df[['val1', 'd', 'variables', 'level', 'fcstType', '']] = df.delimit.str.split(':', expand=True)
    df[['val2', 'val']] = df.val1.str.split('=', expand=True)

    # Add a column to denote the variable and level
    df['var_lev_type'] = df['variables'] + "_" + df['level'] + "_" + df['fcstType']

    # Transposed data to be added to csv
    valT = pd.DataFrame(df.val).T
    valT.columns = df.var_lev_type.values

    # Prep a timestamp column
    raw_time = np.nan
    timestamp_fcst = np.nan
    timestamp_est = np.nan
    valT.insert(loc=0, column="raw_timestamp", value=raw_time)
    valT.insert(loc=1, column="timestamp_fcst", value=timestamp_fcst)
    valT.insert(loc=2, column="timestamp_est", value=timestamp_est)

    # Convert sfc_tmp to C
    sfc_tmp = [col for col in valT.columns if 'TMP_surface' in col] # Find the surface temperature column
    valT[sfc_tmp] = valT[sfc_tmp].astype("float") - 273.15 # Kelvin to Celcius conversion

    valT = valT.reset_index(drop=True)

    return(valT)

def insertTime(df, year, month, day, hour, fcsthr, dst):
    df['raw_timestamp'] = pd.Timestamp(year=year, month=month, day=day, hour=hour) # duplicating the timestamp provides a means of troubleshooting later
    df['timestamp_fcst'] = df['raw_timestamp']  + pd.Timedelta(hours= fcsthr) # make the fcst adjustment
    df['timestamp_est'] = df['timestamp_fcst'] - pd.Timedelta(hours= dst) # make the utc to est adjustment

    return(df)

# Constants
### FOLLOWING FOUR LINES HAVE TO BE CHANGED TO RUN SCRIPT CORRECTLY
### MAKE SURE OUTPUT FOLDERS ARE EMPTY AND DST IS SET
year = "2019"
month = "02"
fpath = "/depot/wwtung/data/LoganD/hrrrOut/jtrp/rwis_feb/"
fout = "/depot/wwtung/data/LoganD/hrrrOut/jtrp/rwis_processed/feb/"
dst = 5

fmid = ".Reduced.hrrr.t"
fend = "z.wrfsfcf"
ftype = ".grib2.csv"
#directories = ["greensburg", "i65@i865", "i74@i465", "kokomo", "market_st_i65_70", "new_castle", "plainfield_i70_eb", "us31@sr32", "us31@sr38"]
directories = ["gas_city", "jeffersonville", "scottsburg"]

for directory in directories:
    rwis_loc = directory

    # loop through the files in fpath+rwis_loc and do the computation necessary
    # Final Ranges: (0, 19, 1) . . . (1, 32, 1) . . . (0, 24, 1)
    for fcsthr in range(0, 19, 1):
        flag = True
        for day in range(1, 29, 1):
            for hour in range(0, 24, 1):
                #Build your file name and output file name
                file = fpath + rwis_loc + '/' + year + '.' + month + '.' + "%02d"%day + fmid + "%02d"%hour + fend + "%02d"%fcsthr + ftype
                file_out = fout + rwis_loc + '/' + year + '.' + month + '.' + 'fcsthr' + "%02d"%fcsthr + '.csv'

                # Set dst conditionally
                if month == "03":
                    if day == 10:
                        if hour == 2:
                            dst = 4

                #send to function to get the row
                data = getRow(file)
                data = insertTime(data, int(year), int(month), day, hour, fcsthr, dst)

                #write to csv, flag says whether or not header is True or False
                if flag:
                    data.to_csv(file_out, mode='a', header=flag, index=False)
                    flag = False
                else:
                    data.to_csv(file_out, mode='a', header=flag, index=False)

                print("Processed " + month + "." + "%02d"%day + " hour:" + "%02d"%hour + " fcstHr:" + "%02d"%fcsthr + " for " + directory)
