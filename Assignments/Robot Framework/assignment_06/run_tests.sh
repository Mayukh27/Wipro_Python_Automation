#!/bin/bash
set -e
robot --include smoke --outputdir results/smoke .
robot --exclude smoke --outputdir results/regression_only .
pabot --testlevelsplit --processes 2 --outputdir results/parallel .
