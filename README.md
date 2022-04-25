# ReleaseScript for Rimworld's mods
Script uses default mod structure and reads `LoadFolder.xml` directories and copy them to Rimworld local mod directory.
Files are copied to a new directory named as mod (taken from `About.xml`) without white spaces.
Used with specific flag will create zip archive for GitHub releases.

Written in Python 3.10

## Usage
`python main.py -start_dir "ModSourceDir" -target_dir "RimworldLocalModDirectory" -zip_tool "7zipPath" -r`

For help:

`python main.py -h`