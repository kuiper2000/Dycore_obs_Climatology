#!bin/sh

cat <<EOF > grid.txt
gridtype = lonlat
xsize    = 128
ysize    = 64
xinc     = 2.83464567
xfirst   = 0
yfirst   = -90
yinc     = 2.857142857142861
EOF


for i in 1000 925 850 700 500 250 200 100
do
#cdo remapbil,grid.txt /work/DATA/Reanalysis/ERA5/t/t${i}_clim.nc t${i}_clim.nc
cdo remapbil,grid.txt /work/DATA/Reanalysis/ERA5/Q1/Q1${i}_clim.nc Q1${i}_clim.nc
done

rm grid.txt
