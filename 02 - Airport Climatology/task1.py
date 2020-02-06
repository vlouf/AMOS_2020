#create figure/axes for plotting with 2 columns and n rows
fig, axes = plt.subplots(nrows=number_airports, ncols=2, figsize=(20, 5*number_airports))

radar_volume_time = 0.1 #number of hours per radar sample (used to transform a count into hours)

#looping through each airport
for i, airport_name in enumerate(airport_name_list):
    
    #load preprocessed data from numpyz files for both ERA5 and Weather radar
    with np.load('preprocessed_data/{name}_era5.npz'.format(name=airport_name)) as era_dict:
        era5_time = era_dict['era5_time']
        era5_crr  = era_dict['era5_crr']*60*60 #crr is in units of mm/s (kg/m2/s)
        era5_cape = era_dict['era5_cape']
    with np.load('preprocessed_data/{name}_radar.npz'.format(name=airport_name)) as radar_dict:
        radar_time = radar_dict['radar_time']
        radar_eth  = radar_dict['radar_eth']
        radar_ref  = radar_dict['radar_ref']

    
        
    #build panda dataframes for era5 and weather radar datasets
    radar_df = pd.DataFrame({'ref':radar_ref, 'eth':radar_eth, 'time':radar_time})
    era_df = pd.DataFrame({'crr':era5_crr, 'cape':era5_cape, 'time':era5_time})
    
    #Diurnal Climatology
    #create twin axes
    ax1 = axes[i,0]
    ax2 = ax1.twinx()
    #for our weather radar data
    #use pandas groupby functionality for hours, apply a count to each group, rescale count to compute hours, and plot
    radar_df.groupby(radar_df['time'].dt.hour)['ref'].count().mul(radar_volume_time).plot(style='r', ax=ax1)
    #for our era5 data
    #use pandas groupby functionality for hours, apply a mean to each group and plot
    era_df.groupby(era_df['time'].dt.hour)['crr'].mean().plot(style='b', ax=ax2)
    #plot annotations
    ax1.set_title('Diurnal Climatology (UTC) for ' + airport_name)
    ax1.set_xlabel('')
    ax1.set_ylabel('Number of thunderstorm hours', color='r')
    ax2.set_ylabel('Mean CRR (mm/hr)', color='b')
    ax1.set_xlim((0,23))
    ax1.set_ylim((0,25))
    ax2.set_ylim((0,0.5))
    
    #Monthly Climatology (same as above, but using groupby month)
    ax1 = axes[i,1]
    ax2 = ax1.twinx()
    radar_df.groupby(radar_df['time'].dt.month)['ref'].count().mul(radar_volume_time).plot(style='r', ax=ax1)
    era_df.groupby(era_df['time'].dt.month)['crr'].mean().plot(style='b', ax=ax2)
    ax1.set_title('Monthly Climatology (UTC) for ' + airport_name)
    ax1.set_xlabel('')
    ax1.set_ylabel('Number of thunderstorm hours', color='r')
    ax2.set_ylabel('Mean CRR (mm/hr)', color='b')
    ax1.set_xlim((1,12))
    ax1.set_ylim((0,25))
    ax2.set_ylim((0,0.5))