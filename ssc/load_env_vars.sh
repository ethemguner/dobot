# run this file on parent folder via 'source'
# Eg: source ssc/load_env_vars.sh
FOLDER=$(pwd)
set -a
source "${FOLDER}/.localsecrets"
set +a
