#!/usr/bin/env bash

set -e
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

allow_warnings=${ALLOW_WARNINGS:-"0"}
if [ "$allow_warnings" = "1" ]
then
    warn_arg=""
else
    # NOTE: Open WebUI has some warnings that we can't control
    allowed_warnings=(
        sqlalchemy.exc.MovedIn20Warning
        DeprecationWarning
        RuntimeWarning
        FutureWarning
    )
    warn_arg="-W error"
    for warning in "${allowed_warnings[@]}"
    do
        warn_arg="$warn_arg -W ignore::$warning"
    done
fi

FAILURE_THRESHOLD=${FAILURE_THRESHOLD:-"100"}
PYTHONPATH="${BASE_DIR}:$PYTHONPATH" python3 -m pytest \
    --cov-config=.coveragerc \
    --cov=ollama_bar \
    --cov-report=term \
    --cov-report=html \
    --cov-fail-under=$FAILURE_THRESHOLD \
    $warn_arg "$@"
