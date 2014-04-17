#!/usr/bin/env bash
# USAGE:
# MS_API_KP="MyKey:MySecret" bash ms_api.sh echo a=b

function ms_api_call {
  curl -s --digest -u "$MS_API_KP" "$MS_API_EP/$1" ${@:2}
}

MS_API_EP="http://api.moodstocks.com/v2"
function ms_api {
  case $1 in
    add)    ms_api_call "ref/$3" --form image_file=@"$2" -X PUT ;;
    del)    ms_api_call "ref/$2" -X DELETE ;;
    echo)   ms_api_call "echo/?$2" ;;
    info)   ms_api_call "/ref/$2" ;;
    mkoff)  ms_api_call "/ref/$2/offline" -d "x" -X POST ;;
    rmoff)  ms_api_call "/ref/$2/offline" -X DELETE ;;
    search) ms_api_call "search" --form image_file=@"$2" ;;
    stats)  ms_api_call "stats/$2" ;;
  esac; echo
}

ms_api $*
