# userscripts
My personal automation repo for daily computing tasks

# Standouts
## [markman](./markman)
-------
retrieve, add, or remove bookmarks using a [plain text file](./static/marks.txt)

Usage: markman [-m]
    -m Use dmenu instead of fzf
    -a Add bookmark
    -r Remove bookmark
    -h Show this usage page
## [sep](./sep)
-------
browse and retrieve entries from the [stanford encyclopedia of philosophy](https://plato.stanford.edu/index.html)

Usage: sep [-q]
    -q query pattern
    -r random entry
    -l list alphabetically
    -h show this usage page
## [shortcutman](./shortcutman)
shortcut manager reads a list of shortcuts with names and paths from a [plain
text file](./scripts/shortcuts) and updates the .bashrc and yazi config to set matching keybindings
for directory shortctuts
## [clip](./clip)
universal clipboard history revtrieval menu
