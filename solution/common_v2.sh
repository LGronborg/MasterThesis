#!/usr/bin/env bash
show_hs="${SHOW_HS:-0}"
show_actual="${SHOW_ACTUAL:-0}"
use_trinityd="${USE_TRINITYD:-0}"

#This is a handout from P3KI with a slight modification to the location for trinity

#echo "Variable IS: $use_trinityd"

BASE_SEARCH=". ../bin ../../bin ../target/release ../../../target/debug"
BASE="."
for base in $BASE_SEARCH; do
	if [ -x "$base/trinity" ]; then
		echo "Located trinity in $base" >&2
		if [ -n "$BASE" -o "$base/trinity" -nt "$BASE/trinity" ]; then
			BASE=$base
		fi
	fi
done

if [ -n "$BASE" ]; then
	echo "Found trinity in $BASE" >&2
fi

function show_quiet() {
	echo -e "\e[1m$ $@\e[0m" >&2
	$@
}

function show_actual() {
	if [ $show_actual -eq 1 ]; then
	    echo -e "\e[32m$ $@\e[0m" >&2
	fi
	$@
}

function show_hs() {
	if [ $show_hs -eq 0 ]; then
		echo $1
	else
		echo $2
	fi
}

function storage_arg() {
	if [ $use_trinityd -eq 1 ]; then
                if [ "$(type -t trinityd_addr)" == "function" ]; then
                    ADDR="$(trinityd_addr $1)"
		else
		    ADDR="http://127.0.0.1:4711"
		fi
		echo "-u $ADDR -i $1"
	else
		echo "-s ./storage-$1"
	fi
}

function trinityd_addr() {
    if [ $1 != alice ]; then
        echo "http://127.0.0.1:4714"
    else
        echo "http://127.0.0.1:4711"
    fi
}

function show() {
	echo -e "\e[1m$ $@\e[0m" >&2
	res="$("$@")"
	echo "$res" >&2
	echo "$res"
}

function section() {
	echo -e "\n\e[7m$@\e[0m"
}


function handshake() {
	a=$1
	b=$2
	pol=$3
	pol_rev="${4:-"nope"}"

	msg=$($a hs2 -S state-$a.bin initiate --challenge-min-policy $pol)
	echo "$a >> $b: $(show_hs Initiate $msg)"

	if [ $pol_rev == 'nope' ]; then
	    msg=$($b hs2 -S state-$b.bin respond  -- "$msg")
	    echo "$a << $b: $(show_hs Respond $msg)"
	else
	    msg=$($b hs2 -S state-$b.bin respond --challenge-min-policy $pol_rev -- "$msg")
	    echo "$a << $b: $(show_hs Respond/Challenge $msg)"
	fi

	while ! $a hs2 -S state-$a.bin check-complete ; do
	    msg=$($a hs2 -S state-$a.bin step -- $msg)
	    if [ ! -z $msg ]; then echo "$a >> $b: $(show_hs Step $msg)"; fi

	    if $b hs2 -S state-$b.bin check-complete; then break; fi  

	    msg=$($b hs2 -S state-$b.bin step -- $msg)
	    if [ ! -z $msg ]; then echo "$a << $b: $(show_hs Step $msg)"; fi
	done

	echo; echo "$a <> $b: Initiator status ($a):"
	$b hs2 -S state-$a.bin status
	echo; echo "$a <> $b: Responder status ($b):"
	$b hs2 -S state-$b.bin status
}

function bootstrap_env() {
	name=$1
	if [ $use_trinityd -eq 1 ]; then
		true
	else
		[[ -d "storage-$name" ]] && rm -rf "storage-$name"
		mkdir "storage-$name"
	fi
}


