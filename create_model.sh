#!/bin/bash

# Usage:
# export DISCORD_TOKEN=<your discord bot token>
# export OPENAI_API_KEY=<your openAI api key>
# bash create_model.sh <channel id> <"discord_user#id"> <dataset entry count=1000> <reduce_mode:first|last|middle|even=even> <ada|babbage|curie|davinci|none <- skips model building> <clean|dirty <- keeps generated files>

if [ ! -f "$1_$2_logs.json" ]
then
    echo "INFO: Exporting chat logs using DiscordChatExporter..."
    echo "INFO: This may take a few minutes to hours depending on the size of the discord channel"
    echo "INFO: Progress will NOT be saved if canceled"
    ./DiscordChatExporter/DiscordChatExporter.Cli.exe export -c $1 -t $DISCORD_TOKEN -o "$1_$2_logs.json" -f Json --filter "from:'$2'"
else
    echo "INFO: Chat logs detected locally... Skipping download."
fi

if [ ! -f "$1_$2_data_set.jsonl" ]
then
    echo "INFO: Parsing chat logs into a openAI compatible dataset..."
    python3.11 data_set_gen.py "$1_$2_logs.json" "$2" $3 $4
    rm "$1_$2_data_set_prepared.jsonl"
else
    echo "INFO: Dataset detected locally... Skipping parsing."
fi

if [ ! -f "$1_$2_data_set_prepared.jsonl" ]
then
    echo "INFO: Cleaning up generated dataset..."
    openai tools fine_tunes.prepare_data -f "$1_$2_data_set.jsonl" -q
    if [ -f "$1_$2_data_set_prepared.jsonl" ]
    then
        python3.11 reduce_dataset.py "$1_$2_data_set_prepared.jsonl" $3 $4
    else
        python3.11 reduce_dataset.py "$1_$2_data_set.jsonl" $3 $4
    fi
else
    echo "INFO: Prepared dataset detected locally... Skipping clean up."
fi

if [ $5 == "davinci" ] || [ $5 == "curie" ] || [ $5 == "babbage" ] || [ $5 == "ada" ]
then
    echo "INFO: Training customized openAI model..."
    echo "INFO: This may take a few minutes to hours depending on the size of the dataset and the selected base model"
    if [ -f "$1_$2_data_set_prepared.jsonl" ]
    then
        openai api fine_tunes.create -t "$1_$2_data_set_prepared.jsonl" -m $5 --suffix "$2"
    else
        openai api fine_tunes.create -t "$1_$2_data_set.jsonl" -m $5 --suffix "$2"
    fi
else
    echo "INFO: No base model selected... Skipping training."
fi

if [ $6 == "clean" ]
then
    rm "$1_$2_data_set.jsonl"
    rm "$1_$2_data_set_prepared.jsonl"
fi