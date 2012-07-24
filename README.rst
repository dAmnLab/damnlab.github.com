-----------------
dAmnLab Home Page
-----------------

This is just a repo for a home page for dAmnLab on the internets. People with
access to this repository should manipulate the page using the `dlab` script.

=====
dlab
=====

Using this script is pretty easy. The script has several commands, which can be
invoked by running the script from the terminal. The different commands allow
you to change the different links displayed in different parts of the pages.

+++++
link
+++++
The `link` command allows you to manage the links shown in the "Quick Links"
section of the page.

~~~~~~
add
~~~~~~
Add a link to this section. For these links, we only need a url, title, and
description. As a brief example::
    
    ./dlab link add --url http://google.com --title Search --description "Use google.com to search the web or something."

~~~~~~
remove
~~~~~~
Remove a link based on its id number or title. For example, to remove the
link added in the above example, use the following::
    
    ./dlab link remove "search"

~~~~~~
list
~~~~~~
List the links currently in the links section. Takes no arguments. Displays the
links by their id and title.

~~~~
up
~~~~
Move a link up the list::
    
    ./dlab link up search

~~~~
down
~~~~
Move a link down the list::
    
    ./dlab link down search

++++++++
project
++++++++

Pretty much involves the same commands as for the link command.

+++++++++
developer
+++++++++
Manages links that may be useful for developers.
