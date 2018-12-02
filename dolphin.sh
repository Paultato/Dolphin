#! /bin/sh
for i in $(seq 1.17 0.001 1.2);
  do python3 src/SharpTree.py $i;
done
