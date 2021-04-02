#!/bin/bash
for eop1 in EOP1 EOP2 EOP3
    do
	for eop2 in EOP1 EOP2 EOP3
	    do
	    	mkdir tmp_zdt3_${eop1}
		for n in 40 80 100
		    do
		    	g=$(( 4000/$n ))
		    	mkdir tmp_zdt3_${eop1}/N${n}_G${g}
		    	rm tmp_zdt3_${eop1}/N${n}_G${g}/metric_CS_${eop2}_NDS.out
		    	for i in {1..9} 99
			    do
				 cat ../MOEA_D_${eop1}/ZDT3/EVAL4000/N${n}_G${g}_T$((15*$n/100))/outputs/s${i}_nds.out > processData1.out
				 lines1=`wc -l < processData1.out`
				 cat ../MOEA_D_${eop2}/ZDT3/EVAL4000/N${n}_G${g}_T$((15*$n/100))/outputs/s${i}_nds.out > processData2.out
				 lines2=`wc -l < processData2.out`
				 echo -e "2\n0\n2\nprocessData1.out\n$lines1\n1\nprocessData2.out\n$lines2\n1\n1" > processData.in
				 ./metrics  < processData.in
				 csi=`cut -f2 cs.out`
				 csi2=`cut -f2 cs2.out`
				 echo -e "$csi\t$csi2"
				 echo -e "$csi\t$csi2" >> tmp_zdt3_${eop1}/N${n}_G${g}/metric_CS_${eop2}_NDS.out
			    done
		    done
	    done
    done

#WE CALL TO PYTHON SCRIPT TO ANALYSE THIS METRICS
python ../NDSMETRICSPROCESS_4000EV.py
