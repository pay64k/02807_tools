#!/usr/bin/env bash

for i in $(ls graphs); do
#    echo item: $i
    python count_connections.py < graphs/$i > out/con_$i
done

