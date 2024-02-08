
# version 30001

data_job

_rlnJobTypeLabel             relion.select.onvalue
_rlnJobIsContinue                       1
_rlnJobIsTomo                           0
 

# version 30001

data_joboptions_values

loop_ 
_rlnJobOptionVariable #1 
_rlnJobOptionValue #2 
dendrogram_minclass      -1000 
dendrogram_threshold       0.85 
discard_label rlnImageName 
discard_sigma          4 
do_class_ranker         No 
do_discard         No 
do_filaments         No 
  do_queue         No 
 do_random         No 
do_recenter        Yes 
do_regroup         No 
do_remove_duplicates         No 
do_select_values        Yes 
  do_split         No 
duplicate_threshold         30 
   fn_data         "" 
    fn_mic CtfFind/job003/tilt_series_ctf.star 
  fn_model         "" 
image_angpix         -1 
min_dedicated          1 
 nr_groups          1 
  nr_split         -1 
other_args         "" 
      qsub     sbatch 
qsub_extra1          3 
qsub_extra2          3 
qsub_extra3    p.hpcl8 
qsub_extra4      gpu:2 
qsubscript ../../../01-Data/relion/qsub_gpu_Relion5.sh 
 queuename    openmpi 
rank_threshold        0.5 
select_label rlnDefocusU 
select_maxval      45000 
select_minval          0 
select_nr_classes         -1 
select_nr_parts         -1 
split_size        100 
 
