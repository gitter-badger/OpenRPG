#!/bin/bash
TEST_FILES=./tests/*

for f in $TEST_FILES
do
	python $f
done
