#!/bin/sh
#
# Source this to define a shell function called mscenv that when run
# will set up the user's environment
#
# mscenv env.txt

mscenv () {
    tosource=$(mktemp)
    # fixme: how to locate
    python metasconsenv.py -s sh $@ > $tosource
    if [ "$?" != "0" ] ; then
	echo "Failed to setup, see $tosource"
    else
	. $tosource
	rm $tosource
    fi
}
