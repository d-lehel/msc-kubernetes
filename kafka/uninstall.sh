#!/bin/bash
helm uninstall lehel-kafka

for s in $(seq 0 2); do
  kubectl delete pvc/data-lehel-kafka-controller-${s}
done
