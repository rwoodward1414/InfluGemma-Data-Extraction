#!/bin/bash

state=$1
search=$2
output="0"

# State Population
if [ "$search" == "0" ]
then
    output=$(curl -s 'https://api.census.gov/data/2023/acs/acs1?get=NAME,B01003_001E&for=state:*' | grep "$state" )
    output=$(echo "$output" | grep -o "[0-9]\{3,\}" )
    echo "$output"
fi

# Median Age
if [ "$search" == "1" ]
then
    output=$(curl -s 'https://api.census.gov/data/2023/acs/acs1?get=NAME,B01002_001E&for=state:*' | grep "$state" )
    output=$(echo "$output" | grep -o "[0-9][0-9]\.[0-9]" )
    echo "$output"
fi

# Median Annual Wage
if [ "$search" == "2" ]
then
    output=$(curl -s 'https://api.census.gov/data/2023/acs/acs1?get=NAME,B06011_001E&for=state:*' | grep "$state" )
    output=$(echo "$output" | grep -o "[0-9]\{3,\}" )
    echo "$output"
fi