#!/bin/bash
#WE CALCULATE THE HVREF FOR ALL DATA (ALL FINAL GENERATIONS OF ALL ALGORITHMS)
rm cf616d_all_seeds_finalgen.out

for eop in CMOEAD_ADAPT CMOEAD_THRES
    do
        for n in 40 80 100
            do
            	g=$(( 4000/$n ))
            	for i in {1..9} 99
		    do
			 cat ../${eop}/CF6_16D/EVAL4000/N${n}_G${g}_T$((12*$n/100))/outputs/s${i}_gen$(($g-1)).out >> cf616d_all_seeds_finalgen.out
		    done
            done
    done

for n in 40 80 100
    do
    	g=$(( 4000/$n ))
    	for i in {1..9} 99
	    do
		 tail -${n} ../NSGAII/CF6_16D/EVAL4000/P${n}G${g}/cf6_16d_all_popmp${n}g${g}_seed0${i}.out >> cf616d_all_seeds_finalgen.out
	    done
    done
    
lines=`wc -l < cf616d_all_seeds_finalgen.out`
    
echo -e "1\n0\n2\ncf616d_all_seeds_finalgen.out\n${lines}\n1\n1" > getReferencePoint4000EV.in
./metrics < getReferencePoint4000EV.in

hvrefx=`cut -f1 hvref.out`
hvrefy=`cut -f2 hvref.out`

# WE CALCULATE THE METRICS WITH THE COMMON REFERENCE FOR ALL DATA (ALL FINAL GENERATIONS OF ALL ALGORITHMS)
for eop in CMOEAD_ADAPT CMOEAD_THRES
    do
    	mkdir tmp_cf616d_${eop}
        for n in 40 80 100
            do
            	g=$(( 4000/$n ))
            	mkdir tmp_cf616d_${eop}/N${n}_G${g}
            	for i in {1..9} 99
		    do
			 cat ../${eop}/CF6_16D/EVAL4000/N${n}_G${g}_T$((12*$n/100))/outputs/s${i}_gen$(($g-1)).out > processData.out
			 echo -e "1\n0\n2\nprocessData.out\n${n}\n1\n0\n$hvrefx\n$hvrefy" > processData.in
			 ./metrics  < processData.in
			 hvi=`cut -f2 hypervol.out`
			 spci=`cut -f2 spacing.out`
			 echo -e "$hvi\t$spci" >> tmp_cf616d_${eop}/N${n}_G${g}/metric_FGEN.out
		    done
            done
    done

mkdir tmp_cf616d_NSGAII
for n in 40 80 100
    do
    	g=$(( 4000/$n ))
    	mkdir tmp_cf616d_NSGAII/N${n}_G${g}
    	for i in {1..9} 99
	    do
		 tail -${n} ../NSGAII/CF6_16D/EVAL4000/P${n}G${g}/cf6_16d_all_popmp${n}g${g}_seed0${i}.out > processData.out
		 echo -e "1\n0\n2\nprocessData.out\n${n}\n1\n0\n$hvrefx\n$hvrefy" > processData.in
		 ./metrics  < processData.in
		 hvi=`cut -f2 hypervol.out`
		 spci=`cut -f2 spacing.out`
		 echo -e "$hvi\t$spci" >> tmp_cf616d_NSGAII/N${n}_G${g}/metric_FGEN.out
	    done
    done
    
    
# WE CALL TO PYTHON SCRIPT TO ANALYSE THIS METRICS
python ../FGENMETRICSPROCESS_HV_SPC_4000EV_CF6_16D.py

