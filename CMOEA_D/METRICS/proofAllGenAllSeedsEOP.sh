#!/bin/bash
cat ../$4/$5/EVAL$(($1*$2))/N$1_G$2_T$3/outputs/s1_allGen.out > $5_$4_all_seeds_allgen_n$1g$2.out
for i in {2..9} 99
    do
        cat ../$4/$5/EVAL$(($1*$2))/N$1_G$2_T$3/outputs/s${i}_allGen.out >> $5_$4_all_seeds_allgen_n$1g$2.out
    done

echo -e "1\n1\n2\n$5_$4_all_seeds_allgen_n$1g$2.out\n$1\n$((10*$2))\n1" > $5_$4_all_seeds_allgen_n$1g$2.in
./metrics < $5_$4_all_seeds_allgen_n$1g$2.in

python ../PLOTHYPERVOLALLSEEDS.py $1 $2 $3 $4 $5 'hypervol.out' & python ../PLOTSPACINGALLSEEDS.py $1 $2 $3 $4 $5 'spacing.out'
