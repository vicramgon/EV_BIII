#!/bin/bash
#WE CALCULATE THE HVREF FOR ALL DATA (ALL FINAL GENERATIONS OF ALL ALGORITHMS)
rm zdt3_all_seeds_nds.out
for eop in EOP1 EOP2 EOP3
    do
        for n in 40 80 100
            do
            	g=$(( 4000/$n ))
            	for i in {1..9} 99
		    do
			 cat ../MOEA_D_${eop}/ZDT3/EVAL4000/N${n}_G${g}_T$((15*$n/100))/outputs/s${i}_nds.out >> zdt3_all_seeds_nds.out
		    done
            done
    done
lines=`wc -l < zdt3_all_seeds_nds.out`
    
echo -e "1\n0\n2\nzdt3_all_seeds_nds.out\n${lines}\n1\n1" > getReferencePoint4000EV.in
./metrics < getReferencePoint4000EV.in

hvrefx=`cut -f1 hvref.out`
hvrefy=`cut -f2 hvref.out`

# WE CALCULATE THE METRICS WITH THE COMMON REFERENCE FOR ALL DATA (ALL nds OF ALL ALGORITHMS)
for eop in EOP1 EOP2 EOP3
    do
    	mkdir tmp_zdt3_${eop}
        for n in 40 80 100
            do
            	g=$(( 4000/$n ))
            	mkdir tmp_zdt3_${eop}/N${n}_G${g}
            	for i in {1..9} 99
		    do
			 cat ../MOEA_D_${eop}/ZDT3/EVAL4000/N${n}_G${g}_T$((15*$n/100))/outputs/s${i}_nds.out > processData.out
			 lines=`wc -l < processData.out`
			 echo -e "1\n0\n2\nprocessData.out\n$lines\n1\n0\n$hvrefx\n$hvrefy" > processData.in
			 ./metrics  < processData.in
			 hvi=`cut -f2 hypervol.out`
			 spci=`cut -f2 spacing.out`
			 echo -e "$hvi\t$spci" >> tmp_zdt3_${eop}/N${n}_G${g}/metric_NDS.out
		    done
            done
    done

# WE CALL TO PYTHON SCRIPT TO ANALYSE THIS METRICS
python ../NDSMETRICSPROCESS_4000EV.py


