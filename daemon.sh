#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/clipboard_monitor/


PROCESS_NAME='clipboard_monitor.py'
PID=`pgrep -f ${PROCESS_NAME}`

if [ "$PID" ]
 then
  echo "Clipboard monitor is already running. Pid $PID";
  exit 1;
else
  echo "Starting Clipboard monitor..."
  screen -S clipboardmonitor -X &>/dev/null
  cmd="$DIR/$PROCESS_NAME"
  screen -d -m -S 'clipboardmonitor'  "$cmd"
  echo $cmd
fi


