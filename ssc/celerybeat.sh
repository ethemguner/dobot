#!/bin/sh
set -e
FOLDER=$(pwd)
cd "$FOLDER"
export PATH=$FOLDER:$PATH
# Checking environment setup
IN_ENVIRONMENT=$(python -c "import sys;print(hasattr(sys, 'real_prefix'))")
if [ "${IN_ENVIRONMENT}" != "True" ]; then
  set -a
  export DJANGO_SETTINGS_MODULE=dobot.settings
  set +a
  IN_ENVIRONMENT=$(python -c "import sys;print(hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)") || $(python -c "import sys;print(hasattr(sys, 'real_prefix'))")
  [ "${IN_ENVIRONMENT}" != "True" ] && echo "Activate the enviroment first!" && exit 1
fi
celery -A dobot worker -Q price_update,celery --autoscale=2,5 -l INFO

