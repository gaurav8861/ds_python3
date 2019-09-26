#!/bin/bash
# Copyright 2019, Cray Inc. All Rights Reserved.

# Wait for brindexer pod.
echo "Waiting for brindexer pod to start..."
while :
do
  br_line=$(kubectl get pods -n cds | grep cds-brindexer-)
  echo "$br_line" | grep -q ' Running '
  # shellcheck disable=SC2181
  if (( $? == 0 ))
  then
    break
  fi
  sleep 1
done

# Get name of brindexer pod.
br_pod=$(kubectl get pods -n cds | grep Running | \
    grep cds-brindexer- | awk '{print $1}')

echo $br_pod

echo "Get a shell to the running Container"
while :
do
  kubectl exec -n cds $br_pod bash
  if (( $? == 0 ))
  then
    break
  fi
  sleep 1
done


echo "Checking go installation and version"
go_version=$(kubectl exec -n cds $br_pod -- bash -c "go version" | wc -l)
if (( $? != 0 || $go_version == 0 ))
then
  echo "Go lang not installed"
  exit 1
fi


echo "Testing scan and indexing of directory"
br_line=$(kubectl exec -n cds $br_pod -- bash -c "go/bin/index /app/")
echo "$br_line" | grep -q 'Commited db records'
if [[ $? -ne 0 ]]
    then
      echo "Failed to Commit db records"
      exit 1
fi
sleep 1

