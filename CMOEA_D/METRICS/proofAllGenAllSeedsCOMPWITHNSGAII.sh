#!/bin/bash
lowerprob=$(echo "$5" | tr '[:upper:]' '[:lower:]')

cat ../$4/$5/EVAL$(($1*$2))/N$1_G$2_T$3/outputs/s1_allGen.out > $5_$4_all_seeds_allgen_n$1g$2.out
cat ../NSGAII/$5/EVAL$(($1*$2))/P$1G$2/${lowerprob}_all_popmp$1g$2_seed01.out > $5_NSGAII_all_seeds_allgen_n$1g$2.out
for i in {2..9} 99
    do
        cat ../$4/$5/EVAL$(($1*$2))/N$1_G$2_T$3/outputs/s${i}_allGen.out >> $5_$4_all_seeds_allgen_n$1g$2.out
        cat ../NSGAII/$5/EVAL$(($1*$2))/P$1G$2/${lowerprob}_all_popmp$1g$2_seed0${i}.out >> $5_NSGAII_all_seeds_allgen_n$1g$2.out
    done
echo -e "2\n1\n2\n$5_$4_all_seeds_allgen_n$1g$2.out\n$1\n$((10*$2))\n$5_NSGAII_all_seeds_allgen_n$1g$2.out\n$1\n$((10*$2))\n1" > $5_$4_all_seeds_allgen_comp_n$1g$2.in
./metrics < $5_$4_all_seeds_allgen_comp_n$1g$2.in
python ../PLOTHYPERVOLCOMP.py $1 $2 $4 'hypervol.out' $1 $2 NSGAII 'hypervol2.out' $5 & python ../PLOTSPACINGCOMP.py $1 $2 $4 'spacing.out' $1 $2 NSGAII 'spacing2.out' $5 & python ../PLOTCOVERSETCOMP.py $1 $2 $4 'cs.out' $1 $2 NSGAII 'cs2.out' $5
