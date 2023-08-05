#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import re
from flatten_json import flatten
from moz_sql_parser import parse

def remove_comments(sql):
    ## remove the /* */ comments
    sql2 = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql)

    # remove whole line -- and # comments
    lines = [line for line in sql2.splitlines() if not re.match("^\s*(--|#)", line)]
    # remove trailing -- and # comments
    return " ".join([re.split("--|#", line)[0] for line in lines]).strip()
    
def extract_tables_from_select(sql):
    """extract tables and views from a select statement"""
    pattern = "from(_\d+)?(.*join)?$"
    sql_dict = flatten(parse(sql))
    return [value for key, value in sql_dict.items() if re.search(pattern, key)]
