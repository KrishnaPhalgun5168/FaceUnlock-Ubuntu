#!/bin/bash

dbus-monitor --session "type='signal',interface='org.gnome.ScreenSaver'" | \
(
	while read x; do
		if [ "$x" == "boolean true" ]; then
			python3 detector.py
			break
		fi
	done
)