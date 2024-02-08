
# version 30001

data_job

_rlnJobTypeLabel             relion.reconstructtomograms
_rlnJobIsContinue                       0
_rlnJobIsTomo                           0
 

# version 30001

data_joboptions_values

loop_ 
_rlnJobOptionVariable #1 
_rlnJobOptionValue #2 
binned_angpix      11.72 
  do_queue        Yes 
generate_split_tomograms         No 
in_tiltseries AlignTiltSeries/job008/aligned_tilt_series.star 
min_dedicated          1 
    nr_mpi          3 
nr_threads          2 
other_args         "" 
      qsub     sbatch 
qsub_extra1          1 
qsub_extra2          3 
qsub_extra3    p.hpcl8 
qsub_extra4      gpu:2 
qsubscript ../../../../../01-Data/relion/qsub_gpu_Relion5.sh 
 queuename    openmpi 
 tomo_name         "" 
      xdim       4096 
      ydim       4096 
      zdim       2048 
 
