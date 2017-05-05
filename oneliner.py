import argparse
import re

__VERSION__ = '0.0.1'

COMMA_OUTSIDE_BRACKET_RE = re.compile(r'\s*,\s*(?![^\[]*?\])')
COMMA_RE = re.compile(r'\s*,\s*')
DOT_BEHIND_LBRACKET_RE = re.compile(r'\s*\.\s*(?=\s*\[)')
EQUAL_RE = re.compile(r'\s*=\s*')
SEMI_RE = re.compile(r'\s*;\s*')


def main():
    # Evaluated code environment variables
    code_globals = {}
    code_locals = {}

    #
    # Command line options
    #
    
    parser = argparse.ArgumentParser(description='Execute Python expressions and statements')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(__VERSION__))
    parser.add_argument('-m', dest='mods', help='comma-separated list of modules to load (os,re,sys always available)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', dest='expr', help='expression to be evaluated')
    group.add_argument('-s', dest='stmt', help='statement to be executed')
    args = parser.parse_args()

    #
    # Modules
    # http://stackoverflow.com/a/2725668/1521064
    #

    # always available modules
    for m in 'os', 're', 'sys':
        code_globals[m] = __import__(m)

    if args.mods:
        # split: 'os.path.[abspath,join],datetime.[timedelta]' -> ['os.path.[abspath,join=j]', 'datetime.[timedelta']
        for candidate_module in COMMA_OUTSIDE_BRACKET_RE.split(args.mods):
            # print('candidate_module=', repr(candidate_module))
            if '[' in candidate_module:
                # split: 'os.path.[abspath,join=j]' -> 'os.path', '[abspath,join=j]'
                pkg, subpkgs = DOT_BEHIND_LBRACKET_RE.split(candidate_module)
                # split: '[abspath,join=j]' -> '[abspath', 'join=j]'
                subpkgs = COMMA_RE.split(subpkgs)
                for subpkg in subpkgs:
                    # clean: ' [ abspath = a ' -> 'abspath=a'
                    subpkg = alias = re.sub(r'[\s\[\]]', '', subpkg)
                    if '=' in subpkg:
                        # 'join=j' -> subpkg='join', alias='j'
                        subpkg, alias = EQUAL_RE.split(subpkg)

                    # print('__import__({}, fromlist=[{}])'.format(pkg, subpkg))
                    # It's just necessary to populate fromlist with some value
                    # to let __import__ return the *rightmost* module
                    i = __import__(pkg, fromlist=['foo'])
                    code_globals[alias] = getattr(i, subpkg)
            elif '=' in candidate_module:
                pkg, alias = EQUAL_RE.split(candidate_module)
                # It's just necessary to populate fromlist with some value
                # to let __import__ return the *rightmost* module
                i = __import__(pkg, fromlist=['foo'])
                code_globals[alias] = i
            else:
                # Just import. The absence of a fromlist will return the
                # leftmost module.
                # 'os.path' -> 'os'
                i = __import__(candidate_module)
                code_globals[candidate_module] = i



    #
    # Expressions
    #
    
    if args.expr:
        for e in SEMI_RE.split(args.expr):
            print(eval(e, code_globals, code_locals))
    
    #
    # Statements
    #
    
    if args.stmt:
        exec(args.stmt, code_globals, code_locals)

# `python -m oneliner` has name '__main__'
if __name__ == '__main__':
    main()

