#!/bin/bash
for filename in logs/*; do
	tail -1 "$filename"
done
