#!bin/sh
"""
This script is designed for long-duration simulations, producing output results at intervals specified by 'space_day'. It helps prevent excessive memory usage by periodically saving results instead of waiting until the end of the simulation.
"""
# this iteration will make sure the model converge to the obs climatology 
for iteration in 1
do 
# each iteration has 500-day with every 25-day as an output
start_day=0
final_day=500
space_day=25
L=0


# echo the number to txt file and saved for later use
echo -n $L      >  Latent_heat.txt
echo $start_day >  day_label.txt
echo $final_day >> day_label.txt
echo $iteration >  obs_theta/iteration.txt



# calculate Q_{N} = Q_{N-1}-2/3(\bar{T}-T)/\tau
cd obs_theta
python Create_obs_climatology.py
cd ../
if [ $iteration -eq 1 ]; then 
rm "obs_theta/grid_Q1?.dat"
rm "obs_theta/grid_Q1??.dat"
cp "obs_theta/grid_Q1.dat" "grid_Q1.dat" 
cp "obs_theta/grid_t_obs.dat" "grid_t_eq.dat"
else
cp "obs_theta/grid_Q1_$(($iteration)).dat" "grid_Q1.dat" 
cp "obs_theta/grid_t_obs.dat" "grid_t_eq.dat"
fi


for i in `seq $start_day $space_day $final_day`
do
echo $i"day"

# for the first iteration and first chunk of simulation 
if [ $i -eq 0 ] && [ $iteration -eq 1 ]; then
	rm -rf HSt42_${L}
	mkdir HSt42_${L}

    rm -rf warmstart_cp_HSt42_${L}
    mkdir warmstart_cp_HSt42_${L}
	echo -n $space_day > HSt42_${L}/day_interval.txt
	echo -n "None" > HSt42_${L}/firstday_file.txt                  # no file on the first day 
# for the second and other iterations but the first chunk of simulation 
elif [ $i -eq 0 ] && [ $iteration -gt 1 ]; then 
    rm -rf HSt42_${L}
	mkdir HSt42_${L}

    rm -rf warmstart_cp_HSt42_${L}
    mkdir warmstart_cp_HSt42_${L}
    cp "HSt42_"${L}"_$(($iteration-1))/HSt42_"${L}"RH80_PR"$L"_"$final_day"day_startfrom_"$i"day_final.dat" "HSt42_${L}/warmstart_${L}.dat" # copy warmstart file from previous iteration 
    echo -n $space_day > HSt42_${L}/day_interval.txt
    echo -n "warmstart_${L}.dat" > HSt42_${L}/firstday_file.txt
else
	echo -n $space_day > HSt42_${L}/day_interval.txt
	echo -n "warmstart_${L}.dat" > HSt42_${L}/firstday_file.txt    # using warm start file on the first day
fi


julia Run_HS.jl
L=0 


if [ -f "HSt42_${L}/warmstart_${L}.dat" ] && [ $i -lt $final_day ]; then
	cp "HSt42_"${L}"/warmstart_${L}.dat" "warmstart_${L}.dat"
	cp "HSt42_"${L}"/warmstart_${L}.dat" "warmstart_cp_HSt42_${L}/warmstart_${L}_$(($i+$space_day))th_day.dat"
	mv "HSt42_"${L}"/all_L"${L}".dat"    "HSt42_"${L}"/RH80_PR"$L"_"$final_day"day_startfrom_"$i"day_final.dat"
	echo 'warmstart file exists.'
elif [ -f "HSt42_${L}/warmstart_${L}.dat" ] && [ $i -eq $final_day ]; then
	mv "HSt42_"${L}"/all_L"${L}".dat"    "HSt42_"${L}"/RH80_PR"$L"_"$final_day"day_startfrom_"$i"day_final.dat"
	cp "HSt42_"${L}"/warmstart_${L}.dat" "warmstart_cp_HSt42_${L}/warmstart_${L}_$(($i+$space_day))th_day.dat"
	mv "HSt42_"${L}"/warmstart_${L}.dat" "HSt42_"${L}"/HSt42_"${L}"RH80_PR"$L"_"$final_day"day_startfrom_"$i"day_final.dat"
	echo "All files have completed!!!"
fi
done
mv "HSt42_"${L} "HSt42_"${L}"_"${iteration} 
done
