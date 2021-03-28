#!/bin/bash
for eop in EOP1 EOP2 EOP3
    do
        for n in 100 40 200
            do
                ./proofAllGenAllSeedsEOP.sh $n $(( 10000/$n )) $eop
            done
    done

for eop in EOP1 EOP2 EOP3
    do
        for n in 40 80 100
            do
                ./proofAllGenAllSeedsEOP.sh $n $(( 4000/$n )) $eop
            done
    done

rm zdt3_EOP*