### Shim - A vim inspired text editor
![movement gif](https://raw.github.com/swong15/shim/master/src/images/demo.gif)


See http://swong15.github.io/shim/ for overview

To install dependencies:

In the shim root directory
```
pip install -r requirements.txt
```

To run:

To add shim.py to your path in your .bashrc (~/.bashrc to edit) or .zshrc if you're using zsh etc
```
export PATH="[path-to-shim-folder-goes-here]/shim/src:$PATH"
```
If you are unsure as to what the path should look like:
From the shim/src folder enter in your terminal
```
pwd
```
Suppose the output of that command was /Users/sebastianwong/Desktop/shim/src then add the following line to your .bashrc file (typically located at ~/.bashrc)
```
export PATH="/Users/sebastianwong/Desktop/shim/src:$PATH"
```
Now run
```
source ~/.bashrc
```
You should then be able to edit files with shim by typing
```
shim.py filename
```
