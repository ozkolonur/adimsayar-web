#!/bin/sh

echo "Cleaning project..."
find -type f -name '*.pyc' -exec rm -f {} ';'
find -type f -name '.*.swp' -exec rm -f {} ';'
find -type f -name '*.py~' -exec rm -f {} ';'
find -type f -name '*.html~' -exec rm -f {} ';'
find -type f -name '*.css~' -exec rm -f {} ';'


