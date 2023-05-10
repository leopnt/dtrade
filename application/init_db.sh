#!/bin/bash

cat schema.sql | sqlite3 predictions.db
