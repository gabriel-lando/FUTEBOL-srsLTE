#!/bin/bash
for i in {90..10..-2}; do
	for j in {50..10..-2}; do
		echo "Tx gain = $i"
		echo "Rx gain = $j"
  		curl http://143.54.12.244:9080/gain/$i/$j
  		sleep 20
	done;
done