cape_threshold = 1000

#for each airport
for i, airport_name in enumerate(airport_name_list):
    #load preprocessed data from numpyz files for both ERA5 and Weather radar
    with np.load('preprocessed_data/{name}_era5.npz'.format(name=airport_name)) as era_dict:
        era5_time = era_dict['era5_time']
        era5_crr  = era_dict['era5_crr']*60*60 #crr is in units of mm/s (kg/m2/s)
        era5_cape = era_dict['era5_cape']
    with np.load('preprocessed_data/{name}_radar.npz'.format(name=airport_name)) as radar_dict:
        radar_time = radar_dict['radar_time']
        radar_ref  = radar_dict['radar_ref']
        radar_eth  = radar_dict['radar_eth']

    #first, we need to pad our data to the time range of the era5 data
    radar_time_pad = np.concatenate(([era5_time[0]], radar_time, [era5_time[-1]]))
    radar_ref_pad = np.concatenate(([np.nan], radar_ref, [np.nan]))
    radar_eth_pad = np.concatenate(([np.nan], radar_eth, [np.nan]))

    #second, we need to create a pandas dataframe of our radar data
    radar_df = pd.DataFrame({'ref':radar_ref_pad, 'eth':radar_eth_pad},    # values
                        index=radar_time_pad)  #index

    #now we can resample to 3hourly intervals
    radar_df_3hr = radar_df.resample('3H').mean()


    #and convert back to numpy arrays
    radar_ref_3hrly = radar_df_3hr['ref'][:]
    radar_eth_3hrly = radar_df_3hr['eth'][:]
    radar_time_3hrly = radar_df_3hr.index

    #skill statistics
    a = np.sum(np.logical_and(era5_cape >= cape_threshold, ~np.isnan(radar_ref_3hrly)))
    b = np.sum(np.logical_and(era5_cape < cape_threshold, ~np.isnan(radar_ref_3hrly)))
    c = np.sum(np.logical_and(era5_cape >= cape_threshold, np.isnan(radar_ref_3hrly)))
    
    #print results
    print('for ', airport_name)
    print('POD:', int(a/(a+b)*100), '%')
    print('FAR:', int(c/(a+c)*100), '%')
    print('')