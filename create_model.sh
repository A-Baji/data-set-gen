#!/bin/bash
# sh create_model.sh <discord-logs.json> <"discord_user#id"> <base_model=ada|babbage|curie|davinci>

python3.11 data_set_gen.py $1 "$2"

rm "$1_$2_data_set_prepared.jsonl"
openai tools fine_tunes.prepare_data -f "$1_$2_data_set.jsonl"
if [ $3 == "davinci" ] || [ $3 == "curie" ] || [ $3 == "babbage" ] || [ $3 == "ada" ]
then
    openai api fine_tunes.create -t "$1_$2_data_set_prepared.jsonl" -m $3 --suffix "$2"
fi

if [ $4 == "clean" ]
then
    rm "$1_$2_data_set.jsonl"
    rm "$1_$2_data_set_prepared.jsonl"
fi