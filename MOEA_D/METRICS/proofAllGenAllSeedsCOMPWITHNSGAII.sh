#!/bin/bash
cat ../MOEA_D_$3/ZDT3/EVAL$(($1*$2))/N$1_G$2_T$((15*$1/100))/outputs/s1_allGen.out > zdt3_$3_all_seeds_allgen_n$1g$2.out
cat ../NSGAII/ZDT3/EVAL$(($1*$2))/P$1G$2/zdt3_all_popmp$1g$2_seed01.out > zdt3_NSGAII_all_seeds_allgen_n$1g$2.out
for i in {2..9}
    do
        cat ../MOEA_D_$3/ZDT3/EVAL$(($1*$2))/N$1_G$2_T$((15*$1/100))/outputs/s${i}_allGen.out >> zdt3_$3_all_seeds_allgen_n$1g$2.out
        cat ../NSGAII/ZDT3/EVAL$(($1*$2))/P$1G$2/zdt3_all_popmp$1g$2_seed0${i}.out >> zdt3_NSGAII_all_seeds_allgen_n$1g$2.out
    done
cat ../MOEA_D_$3/ZDT3/EVAL$(($1*$2))/N$1_G$2_T$((15*$1/100))/outputs/s99_allGen.out >> zdt3_$3_all_seeds_allgen_n$1g$2.out
cat ../NSGAII/ZDT3/EVAL$(($1*$2))/P$1G$2/zdt3_all_popmp$1g$2_seed099.out >> zdt3_NSGAII_all_seeds_allgen_n$1g$2.out
echo -e "2\n1\n2\nzdt3_$3_all_seeds_allgen_n$1g$2.out\n$1\n$((10*$2))\nzdt3_NSGAII_all_seeds_allgen_n$1g$2.out\n$1\n$((10*$2))\n1" > zdt3_$3_all_seeds_allgen_comp_n$1g$2.in
./metrics < zdt3_$3_all_seeds_allgen_comp_n$1g$2.in
python ../PLOTHYPERVOLCOMP.py $1 $2 $3 'hypervol.out' $1 $2 NSGAII 'hypervol2.out' && python ../PLOTSPACINGCOMP.py $1 $2 $3 'spacing.out' $1 $2 NSGAII 'spacing2.out'  && python ../PLOTCOVERSETCOMP.py $1 $2 $3 'cs.out' $1 $2 NSGAII 'cs2.out'
