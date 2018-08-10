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
  if [[ `ls -1 ../AWS_Flask/aws/static/client_img/*.jpg 2>/dev/null | wc -l` -gt 0 ]]; then
    rm ../AWS_Flask/aws/static/client_img/*.jpg 
  fi
  python3 main.py ; export FLASK_APP=aws ;
  cd ../AWS_Flask/ ; flask run --host=0.0.0.0 --port=8080
else
  CLIENT=1
fi

if [[ "${CLIENT}" = 1 ]]; then
  CAPTURE_DIR="client/capture/"
  if [[ ! -d "$CAPTURE_DIR" ]]; then
    mkdir "$CAPTURE_DIR"
  fi
  python3 main_client.py -f $FRAMES -a $ADDRESS -s $SLEEP
fi