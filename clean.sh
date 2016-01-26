#!/bin/bash
# Delete all temporary files
# if the first parameter is 'full' then delete compiled version of mercury6
echo $'\n'

echo "Delete all temporary files"
rm *.dmp *.clo *.out *.tmp *.aei eo.txt elapsed_time.txt

echo "Deleting compiled files."
need_delete='yes'
#read need_delete

if [ $need_delete = 'yes' ]; then
  echo "Compiled files are deleted"
  if [ -e 'close6' ]; then
    rm close6
  fi
  if [ -e 'element6' ]; then
    rm element6
  fi
  if [ -e 'mercury6' ]; then
    rm mercury6
  fi
fi

echo $'\n'
