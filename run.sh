#!/bin/bash
fuser -n tcp -k 8000
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 &
disown

