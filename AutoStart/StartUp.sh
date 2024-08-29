#!/bin/bash
source /home/pi/Desktop/main_env/bin/activate
python /home/pi/MagicMirror/modules/MMM-Face-Recognition-SMAI/MMM-Face-Recognition-SMAI.py | tee -a /home/pi/MagicMirror/MMM-Face-Recognition-output.log
