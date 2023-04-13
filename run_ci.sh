#!/bin/bash
set -e

message_help="""
Deploy and test https://github.com/virtualdata-cloud-i2i/myapp on a remote server. Run with

./run_ci.sh --branch <branch name>
"""

# Show help if no arguments is given
if [[ $1 == "" ]]; then
  echo -e $message_help
  exit 1
fi

# Grab the command line arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --branch)
      BRANCH="$2"
      shift 2
      ;;
    -*)
        echo "unknown option: $1" >&2
        exit 1
        ;;
    *)
        echo "unknown argument: $1" >&2
        exit 1
        ;;
  esac
done

# set up
mkdir -p static
cd static
git clone git@github.com:virtualdata-cloud-i2i/myapp.git
cd myapp

git checkout $BRANCH

# run tests
pytest --doctest-modules --cov=. --cov-report=html:$BRANCH

# expose
if [ -d "../$BRANCH" ]; then
  echo "../$BRANCH does exist."
  rm -rf ../$BRANCH
fi

mv $BRANCH ../

# clean
cd ../
rm -rf myapp
