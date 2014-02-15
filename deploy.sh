#!/bin/bash
HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 "$HERE/sus/deploy.py" $@
