#!/bin/bash
set -e

if [[ -z "${TEST}" ]]; then
    flask run --host=0.0.0.0;
else
    pytest tests/;
fi
