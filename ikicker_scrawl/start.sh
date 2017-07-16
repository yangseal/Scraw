#!/bin/sh
PY_EXEC=python3
$PY_EXEC auto_add_mp.py
$PY_EXEC updatemp.py 1>>logs/stdout.log 2>>logs/stderr.log &
echo "Start......."
