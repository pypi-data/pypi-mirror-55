# -*- coding: utf-8 -*-


"""
This module was written by Carsten Knoll, see

https://github.com/cknoll/ipydex

This code is licensed under GPLv3


https://www.gnu.org/licenses/gpl-3.0.en.html


------------------------------------------------------------------------------

This module is an experimental ipython extension.

Background: insert some logic to display the 'result' of an assignment



# load it with %reload_ext ipydex.displaytools

usage:

`my_random_variable =  np.random.rand() ##`

inserts the source line `display(my_random_variable)` to the source code,
that is actually executed.

That way, the notebook is more comprehensible beacause the reader knows
the content of `my_random_variable`. It saves the typing effort and the code
duplication of manually adding `display(my_random_variable)`.
"""

# Issues: SyntaxError points to the wrong line (due to display insertion)
# Note: this extension does not work properly with keywordargs: x = func(a, b=2)


# todo maybe use sp.Eq(sp.Symbol('Z1'), theta, evaluate=False) to get better formatting

import types
import collections
import ast

import tokenize as tk

import IPython
from IPython.display import display
# noinspection PyUnresolvedReferences
from .core import Container, IPS, line_to_token_list


class FC(Container):
    """
    FlagContainer
    """

    def __init__(self, **kwargs):
        self.empty_comment = False
        self.sc = True  # just indicate that we have a special comment (default true servers as abbreviation)
        self.lhs = False  # relates to the comment
        self.assignment = None  # relates to the actual line (will be set later)
        self.transpose = False
        self.shape = False
        self.comment_only = None  # this refers to the whole line
        self.info = None  # this refers to the whole line
        self.multi_match = []

        kwargs["_allow_overwrite"] = True

        # TODO: when python2 support is dropped: change this to super().__init__(...)
        super(FC, self).__init__(**kwargs)


# generate Special Comment Container

def def_special_comments():
    # _base = "##"
    plain = Container(c="##;", flags=FC())
    transpose = Container(c="##T", flags=FC(transpose=True))
    lhs_transpose = Container(c="##:T", flags=FC(lhs=True, transpose=True))
    lhs_shape = Container(c="##:S", flags=FC(lhs=True, shape=True))
    lhs_info = Container(c="##:i", flags=FC(lhs=True, info=True))
    lhs = Container(c="##:", flags=FC(lhs=True))  # this must be the last one in the list

    SCC = Container(cargs=(plain, transpose, lhs_transpose, lhs_shape, lhs_info, lhs))
    return SCC


SCC = def_special_comments()

sc_list = SCC.value_list()


def get_line_segments(line):
    """
    Split up a line into (indent, lhs, rhs, comment)

    lhs ist defined as the leftmost assignment

    (line does not need to be an assignment)

    :param line:
    :return: lhs, rhs, comment
    """

    tokens = line_to_token_list(line)
    equality_signs = []
    comment_tuple = None, ""
    indent = ""

    for i, t in enumerate(tokens):
        if t.type == tk.INDENT:
            indent = t.string
        if t.type == tk.COMMENT:
            # store string_index and comment string
            comment_tuple = t.start[1], t.string
        if t.type == tk.OP and t.string == "=":
            equality_signs.append(t.start[1])
    try:
        myast = ast.parse(line.strip()).body[0]
    except (IndexError, SyntaxError):
        myast = None

    if isinstance(myast, ast.Assign):
        left_most_assignment = myast.targets[-1]
        # note that indent was stripped away
        lhs_start_idx = left_most_assignment.col_offset + len(indent)

        for eqs_idx in equality_signs:
            if eqs_idx > lhs_start_idx:
                # take the first equality sign which comes after the beginning of the last assignment
                # as delimiter
                lhs_end_idx = eqs_idx-1
                break
        else:
            # no break
            msg = "unexpected locations of equality signs in the line `{}`".format(line)
            raise ValueError(msg)
        lhs = line[lhs_start_idx:lhs_end_idx].strip()
        rhs_start_idx = lhs_end_idx + 2
    else:
        lhs = None
        rhs_start_idx = 0

    # from the last `=` until the beginning of the comment
    rhs = line[rhs_start_idx:comment_tuple[0]].strip()
    if rhs == "":
        rhs = None
    comment = comment_tuple[1].strip()

    return indent, lhs, rhs, comment


def classify_comment(cmt):

    if cmt == "":
        return FC(empty_comment=True, sc=False)

    assert cmt.startswith("#")

    res = None
    matchflag = False
    for sc in sc_list:
        if sc.c in cmt:
            if matchflag:
                # we have a multi match situation
                # ignore this for now
                res.multi_match.append(sc)
                continue
            matchflag = True

            res = sc.flags

    if res is None:
        res = FC(sc=False)

    return res


def is_single_name(expr):
    """
    Return whether an expression consists of a single name

    :param expr:
    :return:
    """

    tokens = line_to_token_list(expr)

    type_counter = collections.defaultdict(int)

    for t in tokens:
        type_counter[t.type] += 1

    # this is absent in Python2
    type_counter.pop(tk.NEWLINE, 0)

    res = type_counter[tk.NAME] == 1 and type_counter[tk.ENDMARKER] == 1 and len(type_counter) == 2

    return res


def process_line(line, line_flags, expr_to_disp, indent):
    """

    :param line:
    :param line_flags:
    :param expr_to_disp:     this is the expression which will be displayed ("x" or "x1, x2" or "a + b")
    :param indent:
    :return:
    """

    delim = "---"
    if line_flags.assignment and is_single_name(expr_to_disp):
        brace_str = "{}"
    else:
        brace_str = "({})"

    expr_to_disp = brace_str.format(expr_to_disp)

     # !! try ... eval(...) except SyntaxError ?
    if line_flags.transpose:
        expr_to_disp = "{}.T".format(expr_to_disp)

    if line_flags.lhs:
        if line_flags.shape:
            new_line = '{}custom_display("{}.shape", {}.shape); print("{}")'
            new_line = new_line.format(indent, expr_to_disp, expr_to_disp, delim)
        elif line_flags.info:
            new_line = '{}custom_display("info({})", _ipydex__info({})); print("{}")'
            new_line = new_line.format(indent, expr_to_disp, expr_to_disp, delim)
        else:
            new_line = '{}custom_display("{}", {}); print("{}")'.format(indent, expr_to_disp, expr_to_disp, delim)
    else:
        new_line = '{}display({}); print("{}")'.format(indent, expr_to_disp, delim)


    return new_line


def insert_disp_lines(raw_cell):
    lines = raw_cell.split('\n')
    N = len(lines)

    # iterate from behind -> insert does not change the lower indices
    for i in range(N-1, -1, -1):
        line = lines[i]

        indent, lhs, rhs, cmt = sgm = get_line_segments(line)
        cmt_flags = classify_comment(cmt)

        if rhs is None or not cmt_flags.sc:
            # no actual statement on that line or
            # no special comment
            continue

        # we have a special comment

        if lhs is not None:

            # situation
            # lhs = rhs ##: sc

            cmt_flags.assignment = True
            new_line = process_line(line, cmt_flags, lhs, indent)
            lines.insert(i+1, new_line)
        else:
            # situation
            # rhs ##: sc

            # this line is not an assignment
            # -> it is replaced by `display(line)`
            # in practise this case is not so important
            cmt_flags.assignment = False
            new_line = process_line(line, cmt_flags, rhs, indent)
            lines[i] = new_line

    new_raw_cell = "\n".join(lines)

    return new_raw_cell


def custom_display(lhs, rhs):
    """
    lhs: left hand side
    rhs: right hand side

    This function serves to inject the string for the left hand side
    of an assignment
    """

    # This code is mainly copied from IPython/display.py
    # (IPython version 2.3.0)
    kwargs = {}
    raw = kwargs.get('raw', False)
    include = kwargs.get('include')
    exclude = kwargs.get('exclude')
    metadata = kwargs.get('metadata')

    from IPython.core.interactiveshell import InteractiveShell
    from IPython.core.displaypub import publish_display_data

    format = InteractiveShell.instance().display_formatter.format
    format_dict, md_dict = format(rhs, include=include, exclude=exclude)

    # example format_dict (for a sympy expression):
    # {u'image/png': '\x89PNG\r\n\x1a\n\x00 ...\x00\x00IEND\xaeB`\x82',
    #  u'text/latex': '$$- 2 \\pi \\sin{\\left (2 \\pi t \\right )}$$',
    # u'text/plain': u'-2\u22c5\u03c0\u22c5sin(2\u22c5\u03c0\u22c5t)'}

    # it is up to IPython which item value is finally used

    # now merge the lhs into the dict:

    if not isinstance(lhs, str):
        raise TypeError('unexpexted Type for lhs object: %s' %type(lhs))

    new_format_dict = {}
    for key, value in list(format_dict.item_list()):
        if 'text/plain' in key:
            prefix = "{} := ".format(lhs)
            if value.startswith("array") or value.startswith("matrix"):
                value = format_np_array(value, len(prefix))

            new_value = prefix + value
            new_format_dict[key] = new_value

        elif 'text/latex' in key:
            if value.startswith("$$"):
                # this is the expected case
                new_value = r"$$\verb|%s| := %s" % (lhs, value[2:])
                new_format_dict[key] = new_value
            else:
                # this is unexpected but raising an exceptions seems
                # not necessary; handle like plain text (see above)
                new_value = lhs+' := '+value
                new_format_dict[key] = new_value
        else:
            # this happens e.g. for mime-type (i.e. key) 'image/png'
            new_format_dict[key] = value

    # legacy IPython 2.x support
    if IPython.__version__.startswith('2.'):
        # noinspection PyTypeChecker
        publish_display_data('display', new_format_dict, md_dict)
    else:
        # indeed, I dont know with which version the api changed
        # but it does not really matter (for me)
        publish_display_data(data=new_format_dict, metadata=md_dict)


def info(arg):
    """
    Print some short and usefull information about arg
    :param arg:
    :return:
    """

    C = Container()
    C.type = type(arg)
    C.shape = getattr(arg, "shape", None)
    C.len = getattr(arg, "__len__", None)

    try:
        tmp = float(arg)
        C.is_number = tmp == arg
    except TypeError:

        C.is_number = False

    res = "{} with {}: {}"
    if C.is_number:
        final = res.format(C.type, "value", arg)
    elif C.shape is not None:
        final = res.format(C.type, "shape", C.shape)
    elif C.len is not None:
        final = res.format(C.type, "length", len(arg))
    else:
        final = res.format(C.type, "str repr", str(arg))

    return final





def get_np_linewidth():
    try:
        # noinspection PyPackageRequirements
        import numpy as np
    except ImportError:
        # numpy not available
        # unexpected situation but not critical
        # return the default

        # noinspection PyUnusedLocal
        np = None  # make pycharm happy
        return 75
    return np.get_printoptions().get('linewidth', 75)


def format_np_array(value, prefixlen):
    lw = get_np_linewidth()
    rows = value.split("\n")
    if len(rows[0]) + prefixlen > lw:
        # inserting prefix will cause linebreaks (or they will occur anyway)
        # start the array at a new line
        rows.insert(0, "")# + [r.strip() for r in rows]
        separation = "\n"
    else:
        # there is enough space to insert the prefix and
        # shift every row to the right appropriately
        separation = "\n" + " "*prefixlen

    return separation.join(rows)


def load_ipython_extension(ip):

    def new_run_cell(self, raw_cell, *args, **kwargs):

        new_raw_cell = insert_disp_lines(raw_cell)

        if 0:
            #debug
            print("cell:")
            print(raw_cell)
            print("new_cell:")
            print(new_raw_cell)
            print('-'*5)
            #print("args", args)
            #print("kwargs", kwargs)

        return ip.old_run_cell(new_raw_cell, *args, **kwargs)

    # prevent unwanted overwriting when the extension is reloaded
    if 'new_run_cell' not in str(ip.run_cell):
        ip.old_run_cell = ip.run_cell

    ip.run_cell = types.MethodType(new_run_cell, ip)
    ip.user_ns['display'] = display
    ip.user_ns['custom_display'] = custom_display
    ip.user_ns['_ipydex__info'] = info

