import ast, sys

from skriddie_vars import unique_names

def skriddie():
    x = 0
    while True:
        x += 1
        yield "_" + str(x)

names = {}
gen_func = unique_names("func")
gen_obj = unique_names("var_obj")
gen_short = unique_names("var_short")
gen_class = unique_names("class")

def make_name(name, gen=gen_obj):
    if not name in names:
        names[name] = next(gen)

def make_var_name(name):
    if len(name) < 4:
        make_name(name, gen_short)
    else:
        make_name(name, gen_obj)

def error_type(x):
    raise NotImplementedError("%s with body: %s" % (str(type(x)), ast.dump(x)))

stmt_types = { ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Return, ast.Delete, ast.Assign, ast.AugAssign, ast.AnnAssign, ast.For, ast.AsyncFor, ast.While, ast.If, ast.With, ast.AsyncWith, ast.Raise, ast.Try, ast.Assert, ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.Expr, ast.Pass, ast.Break, ast.Continue }

expr_types = { ast.BoolOp, ast.NamedExpr, ast.BinOp, ast.UnaryOp, ast.Lambda, ast.IfExp, ast.Dict, ast.Set, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Await, ast.Yield, ast.YieldFrom, ast.Compare, ast.Call, ast.FormattedValue, ast.JoinedStr, ast.Constant, ast.Attribute, ast.Subscript, ast.Starred, ast.Name, ast.List, ast.Tuple, ast.Slice }

def parse_expr(x):
    if type(x) in { ast.Constant, type(None) }:
        pass

    elif type(x) == ast.Expr:
        parse_expr(x.value)

    elif type(x) == ast.Name:
        make_var_name(x.id)
        x.id = names[x.id]

    else:
        error_type(x)

def parse_alias(x):
    if x.asname == None:
        x.asname = x.name

    make_name(x.name, gen_obj)
    x.asname = names[x.name]

def parse_stmt(x):
    if type(x) in { ast.Pass, type(None) }:
        pass

    elif type(x) == ast.Expr:
        parse_expr(x.value)

    elif type(x) == ast.Assign:
        for t in x.targets:
            parse_expr(t)

        parse_expr(x.value)

    elif type(x) == ast.AnnAssign:
        error_type(x)

    elif type(x) == ast.AugAssign:
        make_var_name(x.target.id)
        x.target.id = names[x.target.id]

    elif type(x) == ast.Raise:
        parse_expr(x.exc)
        parse_expr(x.cause)

    elif type(x) == ast.Assert:
        parse_expr(x.test)
        parse_expr(x.msg)

    elif type(x) == ast.Delete:
        for t in x.targets:
            parse_expr(t)

    elif type(x) in { ast.Import, ast.ImportFrom }:
        for a in x.names:
            parse_alias(a)

    else:
        error_type(x)

def parse_thing(x):
    if type(x) in stmt_types:
        parse_stmt(x)

    elif type(x) in expr_types: # is this even needed??
        parse_expr(x)

    else:
        error_type(x)

def parse_body(body):
    for x in p.body:
        parse_thing(x)

def check_implemented(s):
    for x in s:
        try:
            parse_thing(x())
    
        except NotImplementedError as e:
            print(e)
    
        except Exception:
            pass

print("Statements not yet implemented:")
check_implemented(stmt_types)
print()
print("Expressions not yet implemented:")
check_implemented(expr_types)
print()

if __name__ == "__main__":
    try:
        p = ast.parse(open(sys.argv[1]).read())
    
    except Exception as e:
        print("Error during parsing:", str(e))
        sys.exit(1)
    
    parse_body(p.body)
    
    print(ast.unparse(p))
