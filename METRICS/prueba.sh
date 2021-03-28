#!/bin/bash
#WE CALCULATE THE HVREF FOR ALL DATA (ALL FINAL GENERATIONS OF ALL ALGORITHMS)
rm zdt3_all_seeds_finalgen.out
for eop in EOP1 EOP2 EOP3
    do
        for n in 100 40 200
            do
            	g=$(( 10000/$n ))
            	for i in {1..9} 99
		    do
			 cat ../MOEA_D_${eop}/ZDT3/EVAL10000/N${n}_G${g}_T$((15*$n/100))/outputs/s${i}_gen$(($g-1)).out >> zdt3_all_seeds_finalgen.out
		    done
            done
    done
for n in 100 40 200
    do
    	g=$(( 10000/$n ))
    	for i in {1..9} 99
	    do
		 tail -${n} ../NSGAII/ZDT3/EVAL10000/P${n}G${g}/zdt3_all_popmp${n}g${g}_seed0${i}.out >> zdt3_all_seeds_finalgen.out
	    done
    done
    
lines=`wc -l < zdt3_all_seeds_finalgen.out`
    
echo -e "1\n0\n2\nzdt3_all_seeds_finalgen.out\n${lines}\n1\n1" > getReferencePoint10000EV.in
./metrics < getReferencePoint10000EV.in

hvrefx=`cut -f1 hvref.out`
hvrefy=`cut -f2 hvref.out`

# WE CALCULATE THE METRICS WITH THE COMMON REFERENCE FOR ALL DATA (ALL FINAL GENERATIONS OF ALL ALGORITHMS)
for eop in EOP1 EOP2 EOP3
    do
    	mkdir tmp_zdt3_${eop}
        for n in 100 40 200
            do
            	g=$(( 10000/$n ))
            	mkdir tmp_zdt3_${eop}/N${n}_G${g}
            	for i in {1..9} 99
		    do
			 cat ../MOEA_D_${eop}/ZDT3/EVAL10000/N${n}_G${g}_T$((15*$n/100))/outputs/s${i}_gen$(($g-1)).out > processData.out
			 echo -e "1\n0\n2\nprocessData.out\n${n}\n1\n0\n$hvrefx\n$hvrefy" > processData.in
			 ./metrics  < processData.in
			 hvi=`cut -f2 hypervol.out`
			 spci=`cut -f2 spacing.out`
			 echo -e "$hvi\t$spci" >> tmp_zdt3_${eop}/N${n}_G${g}/metric_FGEN.out
		    done
            done
    done
    
mkdir tmp_zdt3_NSGAII
for n in 100 40 200
    do
    	g=$(( 10000/$n ))
    	mkdir tmp_zdt3_NSGAII/N${n}_G${g}
    	for i in {1..9} 99
	    do
		 tail -$n ../NSGAII/ZDT3/EVAL10000/P${n}G${g}/zdt3_all_popmp${n}g${g}_seed0${i}.out > processData.out
		 echo -e "1\n0\n2\nprocessData.out\n${n}\n1\n0\n$hvrefx\n$hvrefy" > processData.in
		 ./metrics  < processData.in
		 hvi=`cut -f2 hypervol.out`
		 spci=`cut -f2 spacing.out`
		 echo -e "$hvi\t$spci" >> tmp_zdt3_NSGAII/N${n}_G${g}/metric_FGEN.out
	    done
    done

# WE CALL TO PYTHON SCRIPT TO ANALYSE THIS METRICS
python ../FGENMETRICSPROCESS_10000EV.py


