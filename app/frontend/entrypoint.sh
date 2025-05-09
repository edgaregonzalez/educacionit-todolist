#!/bin/sh
set -e
while [[ $# -gt 0 ]]; do
    case "$1" in
        --saludo)
        shift
        MESSAGE="$1"
        echo "Mensaje recibido: $MESSAGE"
        exit 0
        ;;
        *)
        break
        ;;
    esac
    shift
done