#! /bin/bash
GREP_COLOR='1;32' grep --color=always -nri "$1" * | grep -v "selenium_tests" | grep -v tmp | grep -v migrations 
