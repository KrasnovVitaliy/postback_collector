#!/usr/bin/env bash

celery -A tasks worker --loglevel=debug