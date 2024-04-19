#!/bin/bash

# Usage: ./genTest.sh <file> <number_of_articles>

if [ "$#" -ne 2 ]; then
  echo "Usage: ./genTest.sh <file> <number_of_articles>"
  exit 1
elif [[ ! $2 =~ ^[0-9]*[1-9][0-9]*$ ]]; then
  echo "Error: <number_of_articles> must be a positive integer"
  exit 1
fi

file=$1
n_articles=$2
page_width=500
page_height=500

mkdir -p "$(dirname "$file")" # Create directories in the file path if they don't exist

echo "$n_articles $page_width $page_height" > "$file" # Write block header to file truncating it

for (( i=0; i<$n_articles; i++ ))
do
  w=$((RANDOM % 100 + 1)) # Random width between 1 and 100
  h=$((RANDOM % 100 + 1)) # Random height between 1 and 100
  x=$((RANDOM % (page_width - w + 1))) # Random x-coordinate, ensuring the article fits within the page width
  y=$((RANDOM % (page_height - h + 1))) # Random y-coordinate, ensuring the article fits within the page height
  echo "$w $h $x $y" >> "$file"
done
