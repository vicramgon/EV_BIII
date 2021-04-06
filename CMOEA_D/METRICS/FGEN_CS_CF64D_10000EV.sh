#!/bin/bash
for eop1 in CMOEAD_ADAPT CMOEAD_THRES
    do
    	mkdir tmp_cf64d_${eop1}
	for eop2 in CMOEAD_ADAPT CMOEAD_THRES
	    do
		for n in 40 100 200
		    do
		    	g=$(( 10000/$n ))
		    	mkdir tmp_cf64d_${eop1}/N${n}_G${g}
		    	rm tmp_cf64d_${eop1}/N${n}_G${g}/metric_CS_${eop2}_FGEN.out
		    	for i in {1..9} 99
			    do
				 cat ../${eop1}/CF6_4D/EVAL10000/N${n}_G${g}_T$((10*$n/100))/outputs/s${i}_gen$(($g-1)).out > processData1.out
				 lines1=`wc -l < processData1.out`
				 cat ../${eop2}/CF6_4D/EVAL10000/N${n}_G${g}_T$((10*$n/100))/outputs/s${i}_gen$(($g-1)).out > processData2.out
				 lines2=`wc -l < processData2.out`
				 echo -e "2\n0\n2\nprocessData1.out\n$lines1\n1\nprocessData2.out\n$lines2\n1\n1" > processData.in
				 ./metrics  < processData.in
				 csi=`cut -f2 cs.out`
				 csi2=`cut -f2 cs2.out`
				 echo -e "$csi\t$csi2"
				 echo -e "$csi\t$csi2" >> tmp_cf64d_${eop1}/N${n}_G${g}/metric_CS_${eop2}_FGEN.out
			    done
		    done
	    done
	    
	for n in 40 100 200
	    do
	        g=$(( 10000/$n ))
		rm tmp_cf64d_${eop1}/N${n}_G${g}/metric_CS_NSGAII_FGEN.out
		for i in {1..9} 99
		    do
		        cat ../${eop1}/CF6_4D/EVAL10000/N${n}_G${g}_T$((10*$n/100))/outputs/s${i}_gen$(($g-1)).out > processData1.out
			lines1=`wc -l < processData1.out`
			tail -${n} ../NSGAII/CF6_4D/EVAL10000/P${n}G${g}/cf6_4d_all_popmp${n}g${g}_seed0${i}.out > processData2.out
			lines2=`wc -l < processData2.out`
			echo -e "2\n0\n2\nprocessData1.out\n$lines1\n1\nprocessData2.out\n$lines2\n1\n1" > processData.in
			./metrics  < processData.in
		  	csi=`cut -f2 cs.out`
			csi2=`cut -f2 cs2.out`
			echo -e "$csi\t$csi2"
			echo -e "$csi\t$csi2" >> tmp_cf64d_${eop1}/N${n}_G${g}/metric_CS_NSGAII_FGEN.out
		    done
	    done
    done

#WE CALL TO PYTHON SCRIPT TO ANALYSE THIS METRICS
python ../FGENMETRICSPROCESS_CS_10000EV_CF6_4D.py
