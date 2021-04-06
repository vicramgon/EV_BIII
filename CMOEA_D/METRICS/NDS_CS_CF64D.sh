#!/bin/bash
for eop1 in CMOEAD_ADAPT
    do
	for eop2 in CMOEAD_THRES
	    do
	    	mkdir tmp_cf64d_${eop1}
		for n in 40 80 100
		    do
		    	g=$(( 4000/$n ))
		    	mkdir tmp_cf64d_${eop1}/N${n}_G${g}
		    	rm tmp_cf64d_${eop1}/N${n}_G${g}/metric_CS_${eop2}_NDS.out
		    	for i in {1..9} 99
			    do
				cat ../${eop1}/CF6_4D/EVAL4000/N${n}_G${g}_T$((10*$n/100))/outputs/s${i}_nds.out > processData1.out
				 lines1=`wc -l < processData1.out`
				 cat ../${eop2}/CF6_4D/EVAL4000/N${n}_G${g}_T$((10*$n/100))/outputs/s${i}_nds.out > processData2.out
				 lines2=`wc -l < processData2.out`
				 echo -e "2\n0\n2\nprocessData1.out\n$lines1\n1\nprocessData2.out\n$lines2\n1\n1" > processData.in
				 ./metrics  < processData.in
				 csi=`cut -f2 cs.out`
				 csi2=`cut -f2 cs2.out`
				 echo -e "$csi\t$csi2"
				 echo -e "$csi\t$csi2" >> tmp_cf64d_${eop1}/N${n}_G${g}/metric_CS_${eop2}_NDS.out
			    done
		    done
		
		for n in 40 100 200
		    do
		    	g=$(( 10000/$n ))
		    	mkdir tmp_cf64d_${eop1}/N${n}_G${g}
		    	rm tmp_cf64d_${eop1}/N${n}_G${g}/metric_CS_${eop2}_NDS.out
		    	for i in {1..9} 99
			    do
				cat ../${eop1}/CF6_4D/EVAL10000/N${n}_G${g}_T$((10*$n/100))/outputs/s${i}_nds.out > processData1.out
				 lines1=`wc -l < processData1.out`
				 cat ../${eop2}/CF6_4D/EVAL10000/N${n}_G${g}_T$((10*$n/100))/outputs/s${i}_nds.out > processData2.out
				 lines2=`wc -l < processData2.out`
				 echo -e "2\n0\n2\nprocessData1.out\n$lines1\n1\nprocessData2.out\n$lines2\n1\n1" > processData.in
				 ./metrics  < processData.in
				 csi=`cut -f2 cs.out`
				 csi2=`cut -f2 cs2.out`
				 echo -e "$csi\t$csi2"
				 echo -e "$csi\t$csi2" >> tmp_cf64d_${eop1}/N${n}_G${g}/metric_CS_${eop2}_NDS.out
			    done
		    done

	    done
    done

#WE CALL TO PYTHON SCRIPT TO ANALYSE THIS METRICS
python ../NDS_METRICSPROCESS_CS_CF6_4D.py
