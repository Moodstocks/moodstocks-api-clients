#!/usr/bin/env bash
# Encode to / decode from Base64-URL without padding.

# USAGE:
# bash base64url.sh encode 'Hello!'
# bash base64url.sh decode SGVsbG8h

function encode {
  echo -n "$1" | openssl enc -a -A | tr -d '=' | tr '/+' '_-'
}

function decode {
  _l=$((${#1} % 4))
  if [ $_l -eq 2 ]; then _s="$1"'=='
  elif [ $_l -eq 3 ]; then _s="$1"'='
  else _s="$1" ; fi
  echo "$_s" | tr '_-' '/+' | openssl enc -d -a -A
}

case $1 in
  encode) encode "$2" ;;
  decode) decode $2 ;;
  e) encode "$2" ;;
  d) decode $2 ;;
esac
