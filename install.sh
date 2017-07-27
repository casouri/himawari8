#!/bin/bash
cp himawari8.py ~/.himawari8/himawari8.py
cp cowboy.jpg ~/.himawari8/cowboy.jpg

first='<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.yuan.himawari8</string>

        <key>Program</key>
        <string>script_p</string>

        <key>RunAtLoad</key>
        <true/>

        <key>StartInterval</key>
        <integer>600</integer>
    </dict>
</plist>
'
second=$HOME/.himawari8/himawari8.py
plist=${first/script_p/$second}

rm $HOME/Library/LaunchAgents/com.yuan.himawari8.plist
echo $plist >> $HOME/Library/LaunchAgents/com.yuan.himawari8.plist

launchctl unload $HOME/Library/LaunchAgents/com.yuan.himawari8.plist
launchctl load $HOME/Library/LaunchAgents/com.yuan.himawari8.plist
chmod 744 ~/.himawari8/himawari8.py