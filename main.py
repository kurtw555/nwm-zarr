import zarr
import xarray as xr
import s3fs


if __name__ == '__main__':


    # Define the S3 path to your Zarr file
    s3_path = 's3://noaa-nwm-retrospective-3-0-pds/CONUS/zarr/chrtout.zarr'

    # Create an S3 filesystem object
    s3 = s3fs.S3FileSystem(anon=True)

    store = s3fs.S3Map(s3_path, s3=s3)
    #z = zarr.open(store, mode='r')

    # Print the Zarr file structure
    #print(z.tree())

    # Open the Zarr file using xarray
    ds = xr.open_zarr(s3fs.S3Map(s3_path, s3=s3), consolidated=True)
    vals = ds['streamflow'].sel(feature_id= 11137344).values

    print(ds['streamflow'])

    ds_nwm_chrtout = ds
    usgs_station_id = "13317000"
    ds_nwm_gage = (
        ds_nwm_chrtout
            .where(ds_nwm_chrtout.gage_id == f'{usgs_station_id.rjust(15, " ")}'.encode(), drop=True))

    # Print the dataset to verify
    print(ds)
    
    
    chrout_file = "noaa-nwm-retrospective-3-0-pds/CONUS/zarr/chrtout.zarr"

    ds_nwm_chrtout = xr.open_zarr(chrout_file)
    ds_nwm_gage = (
        ds_nwm_chrtout
            .where(ds_nwm_chrtout.gage_id == f'{usgs_station_id.rjust(15, " ")}'.encode(), drop=True))
    
    ival = 1