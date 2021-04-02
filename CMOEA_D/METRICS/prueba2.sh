#!/bin/bash
hvrefx=`cut -f1 hvref.out`
hvrefy=`cut -f2 hvref.out`
    
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

