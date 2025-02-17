# Moist_Dycore_for_zenodo
Associated Ref:
https://github.com/CliMA/IdealizedSpectralGCM.jl/tree/master

## Install JGCM
(0) Before Installation, clean up the pre-installed library 
```
julia> ]
pkg> rm JGCM 
```
(1) JGCM will be installed under the path, so move to this location first 
```
`/Moist_Dycore_for_zenodo/IdealizeSpetral.jl/`
```

(2) Switch to developer mode and install the model
```
julia> ]
pkg> dev .
```
(3) Load model
```
julia> using JGCM
```


# Run Experiments
Before you run the model for test, please make sure you're at 
```
`/Moist_Dycore_for_zenodo/IdealizeSpetral.jl/exp/HSt42/`
```
Test run 
```
julia For_test_Run_HS.jl
```
For extended-period experiment
```
sh PR0_long_run.sh
```
This script is designed for long-duration simulations, producing output results at intervals specified by 'space_day'. 
It helps prevent excessive memory usage by periodically saving results instead of waiting until the end of the simulation.

And, L represent latent heat release efficiency, you can adjust L=0 to 50 (meaing L=0 ~ 0.5 to avoid point in code).
