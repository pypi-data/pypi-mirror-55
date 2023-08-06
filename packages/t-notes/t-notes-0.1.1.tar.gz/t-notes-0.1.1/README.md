# TNotes
Program for quick terminal-based notes.

## Usage

After installing with `$ pip install t-notes` create/choose a note with `$ tnotes note [note name]` (default is firstnote, and folders are accepted).

To see the current note, `$ tnotes current`

To create a note entry, simply `$ t [your note]`

To modify it, just `$ tt [index]` where the index starts from 0 (last entry). If no index is entered, default is 0.

To save it to a file, `$ tnotes save [filename]`

To change any of the settings, `$ tnotes config [config name] [new value]` (config file in .tnotes)

Note: Every entry is saved with a timestamp, and modifications do not delete the old version, which can be accessed in the tnotes folder (in home)
