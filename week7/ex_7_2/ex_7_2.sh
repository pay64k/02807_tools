#!/usr/bin/env bash

for i in $(ls graphs); do
#    echo item: $i
    python count_connections.py < graphs/$i > out/degrees/degrees_$i
done

for i in $(ls out/degrees); do
#    echo item: $i
    python determine.py < out/degrees/$i > out/euler_result_from_$i
done