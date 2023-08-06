#!/bin/bash

if [[ "$(curl -o -I -L -s -w '%{http_code}'  'http://169.254.169.254/latest/meta-data/public-hostname')" -ne 200 ]] ; then
    export DORA_HOST=$(curl -sL "http://169.254.169.254/latest/meta-data/local-ipv4")
else
    export DORA_HOST=$(curl -sL "http://169.254.169.254/latest/meta-data/public-hostname")
fi

export DORA_INSTANCE=$(curl -sL "http://169.254.169.254/latest/meta-data/instance-id")

if [[ -z "$DORA_HOST" ]]; then
   export DORA_HOST=localhost
fi

export SPARK_MASTER_PORT=7077

export DORA_SPARK="spark://`hostname`:$SPARK_MASTER_PORT"

$SPARK_HOME/sbin/start-master.sh 1> ${DORA_LOG}/master.log 2> ${DORA_LOG}/master.error
$SPARK_HOME/sbin/start-slave.sh --memory "${DORA_MEM}" $DORA_SPARK 1> ${DORA_LOG}/slave.log 2> ${DORA_LOG}/slave.error
spark-submit --executor-memory "${DORA_MEM}" --driver-memory "${DORA_MEM}" --conf spark.sql.catalogImplementation=hive --master ${DORA_SPARK} /etc/ml/score/init.py "$@" 2> ${DORA_LOG}/score.log