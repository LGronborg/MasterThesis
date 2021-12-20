#!/usr/bin/env bash
set -euo pipefail

. common_v2.sh

#This is a handout from P3KI with slight modifications

PERSON1=$1 #alice
PERSON2=$2 #bob
RELATION=$3 #action
function person1() {
    $BASE/trinity $(storage_arg $PERSON1) "$@"
}

function person2() {
    $BASE/trinity $(storage_arg $PERSON2) "$@"
}


show_quiet handshake person1 person2 $RELATION
