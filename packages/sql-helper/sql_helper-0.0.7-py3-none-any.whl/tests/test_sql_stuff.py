import pytest
import bg_helper as bh
from sql_helper import SQL

# - check if docker exists on system
# - start test container for postgres 9.6
# - make sure the test table(s) don't exist (skip if non-empty)
# - create test table(s)
# - insert some items
#   - try bulk (with params)
#   - try from sql file (may need to add to manifest.in)
# - do some queries
