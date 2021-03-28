#!/bin/bash
cat ../MOEA_D_$3/ZDT3/EVAL$(($1*$2))/N$1_G$2_T$((15*$1/100))/outputs/s1_allGen.out > zdt3_$3_all_seeds_allgen_n$1g$2.out
for i in {2..9}
    do
        cat ../MOEA_D_$3/ZDT3/EVAL$(($1*$2))/N$1_G$2_T$((15*$1/100))/outputs/s${i}_allGen.out >> zdt3_$3_all_seeds_allgen_n$1g$2.out
    done
cat ../MOEA_D_$3/ZDT3/EVAL$(($1*$2))/N$1_G$2_T$((15*$1/100))/outputs/s99_allGen.out >> zdt3_$3_all_seeds_allgen_n$1g$2.out
echo -e "1\n1\n2\nzdt3_$3_all_seeds_allgen_n$1g$2.out\n$1\n$((10*$2))\n1" > zdt3_$3_all_seeds_allgen_n$1g$2.in
./metrics < zdt3_$3_all_seeds_allgen_n$1g$2.in
python ../PLOTHYPERVOLALLSEEDS.py $1 $2 $3 'hypervol.out' && python ../PLOTSPACINGALLSEEDS.py $1 $2 $3 'spacing.out'
