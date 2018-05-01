./run.sh oxford_11JAN2018.csv oxford.json
./run.sh Resolved_study_codes_27APR2018.txt resolved_studies.json
./run.sh solaris_species.csv solaris_species.json
./runsss.sh 2017_06_07_report_sample_status.xls
./run.sh pf_6_metadata.txt pf_6_metadata.json
./run.sh Pv4_manifest_20180326.txt pv_4_manifest.json
for i in ../../ROMA_Deploy/data/genre_dump.20180116103346.json ../../ROMA_Deploy/data/vivax_dump.20180116103346.json ../../ROMA_Deploy/data/spotmalaria_dump.20180116103346.json ../../ROMA_Deploy/data/vobs_dump.20180116103346.json
do
    ./run_roma.sh $i
done
./run.sh sanger_lims_dump_11JAN2018.csv sanger_lims.json
./run.sh vivax1128.csv vivax1128.json
./run.sh ag1000g.samples.meta.txt ag1000g.json
./run.sh manage_sites.denormalized.txt denorm_manage_sites.json
./run_load_country_oxford.sh oxford_11JAN2018.csv 2017_06_07_report_sample_status.xls
./run_set_taxa.sh
