#!/bin/bash

for eop in CMOEAD_ADAPT CMOEAD_THRES
    do
        for n in 100 40 200
            do
                ./proofAllGenAllSeedsCOMPWITHNSGAII.sh $n $(( 10000/$n )) $(((10*$n)/100)) $eop CF6_4D
            done
    done
for eop in CMOEAD_ADAPT CMOEAD_THRES
    do
        for n in 40 80 100
            do
                ./proofAllGenAllSeedsCOMPWITHNSGAII.sh $n $(( 4000/$n )) $(((10*$n)/100)) $eop CF6_4D
            done
    done
    
rm ./CF6_4D*

for eop in CMOEAD_ADAPT CMOEAD_THRES
    do
        for n in 100 40 200
            do
                ./proofAllGenAllSeedsCOMPWITHNSGAII.sh $n $(( 10000/$n )) $(((12*$n)/100)) $eop CF6_16D
            done
    done

for eop in CMOEAD_ADAPT CMOEAD_THRES
    do
        for n in 40 80 100
            do
                ./proofAllGenAllSeedsCOMPWITHNSGAII.sh $n $(( 4000/$n )) $(((12*$n)/100)) $eop CF6_16D
            done
    done

rm ./CF6_16D*
