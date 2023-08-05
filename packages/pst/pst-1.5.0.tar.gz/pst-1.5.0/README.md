<a href="https://travis-ci.org/mixedconnections/pst">
    <img src="https://api.travis-ci.org/mixedconnections/pst.svg?branch=master" alt="travis build status" />
</a>
<a href="https://codecov.io/gh/mixedconnections/pst">
    <img src="https://codecov.io/github/mixedconnections/pst/coverage.svg?branch=master" alt="coverage" />
</a>

# pst: a reproduction of pstree

pst is a command-line utility that creates visual trees of your running processes on Unix-like systems. 

![this link](images/pstexample.png)

pst is a reproduction of [pstree](https://en.wikipedia.org/wiki/Pstree), written in Python.

# Installation

pst currently supports Python 2.x-3.x.

#### PyPI

    $ sudo pip install pst

#### Manual

First clone the pst repository and go into the directory.

    $ git clone git://github.com/mixedconnections/pst.git
    $ cd pst

Then run the command below.

    $ sudo python setup.py install

If you don't have root permission (or don't want to install pst with sudo), try:

    $ python setup.py install --prefix=~/.local
    $ export PATH=~/.local/bin:$PATH

# Usage

 __pst__ shows running processes as a tree.  The tree is rooted at
 either _pid_ or __init__ if _pid_ is omitted.  If a user name is specified,
 all process trees rooted at processes owned by that user are shown
 
#### Command Line Options

##### -h, --help

Display a help message

##### -v, --version

Display the version of pst

##### -o, --output `string`
    
Directs the output to a file name of your choice

##### -w, --write

When specified, pst writes to stdout. By default, pst uses less to page the output. 

##### -u, --user `string`
    
Show only trees rooted at processes of this user

##### -p, --pid `integer`
    
Start at this pid; default is 1 (init)

# Demo
Demos speak more than a thousand words! Here's me running pst on ubuntu. As you can see, you can select a pid and see its child processes:

![this link](images/pst-demo.gif)

#### More Examples

    shell> 
    shell> pst
    shell> pst --help
    shell> pst -o trees.txt 
    shell> pst --user postgres
    shell> pst --pid 393    
