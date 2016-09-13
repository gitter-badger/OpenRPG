#!/bin/bash
TEST_FILES=./test/*

for f in $TEST_FILES
do
	python $f
done
