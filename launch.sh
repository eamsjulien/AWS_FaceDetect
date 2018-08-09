#!/bin/bash

CLIENT=0

POSITIONAL=()
while [[ $# -gt 0 ]]
do

  key="$1"

  case $key in
    -m|--mode)
      MODE="$2"
      shift
      shift
      ;;
    -f|--frames)
      FRAMES="$2"
      shift
      shift
      ;;
    -a|--address)
      ADDRESS="$2"
      shift
      shift
      ;;
    -s|--sleep)
      SLEEP="$2"
      shift
      shift
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

set -- "${POSITIONAL[@]}"

source setup_env.sh

if [[ "${MODE}" = "server" ]]; then
  python3 main.py
else
  CLIENT=1
fi

if [[ "${CLIENT}" = 1 ]]; then
  python main_client.py -f $FRAMES -a $ADDRESS -s $SLEEP
fi