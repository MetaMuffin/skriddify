import random
from enum import Enum


def read_keyword_file(fn):
    with open(fn, "r") as f:
        return f.read().strip().split("\n")


db_var_short = read_keyword_file("kw/var_short")
db_var_obj = read_keyword_file("kw/var_obj")
db_var_suffix = read_keyword_file("kw/var_suffix")
db_fn_op = read_keyword_file("kw/fn_op")


def random_element(db):
    return db[random.randint(0, len(db)-1)]


syntax = {
    "func": [
        [0.4, db_fn_op],
        [1, "var_obj"]
    ],
    "var_obj": [
        [1, db_var_obj],
        [0.4, db_var_suffix]
    ],
    "var_short": [
        [1, db_var_short],
        [0.4, db_var_short]
    ],
    "class": [
        [1, db_var_obj],
        [1, db_var_obj]
    ],
    "duplicate": [
        [1, None, "of"],
        [1, "var_obj"]
    ]
}

# generator function for unique name, so you dont need to track used ones.
def unique_names(ty):
    used = {}
    while True:
        yield single_unique_name(used,ty)

def single_unique_name(used,ty):
    # TODO make this code more efficient
    name = single_name(ty)
    while name in used: name = single_name(ty)
    return name

# generate parts of a variable name as a list
def parts_for(ty):
    st = syntax[ty]
    parts = []
    for ps in st:
        if random.random() < ps[0]:
            if type(ps[1]) == type(None):
                parts.append(ps[2])
            elif type(ps[1]) == type(""):
                parts.extend(parts_for(ps[1]))
            else:
                parts.append(random_element(ps[1]))
    return parts

# remove duplicates from the variable parts
def post_processs_parts(parts):
    seen = {}
    parts_post = []
    for p in parts:
        if p in seen:
            parts_post.extend(parts_for("duplicate"))
        else:
            seen[p] = 1
            parts_post.append(p)
    return parts_post

# create a single random variable name
def single_name(ty):
    parts = []
    for x in parts_for(ty):
        parts.extend(x.split("_"))

    parts = post_processs_parts(parts)
    if ty == "class":
        return camelCase(parts)
    return "_".join(parts)

# converts parts to camel case
def camelCase(parts):
    o = ""
    for p in parts:
        o += p[0].upper() + (p[1:] if len(p) > 0 else "")
    return o
