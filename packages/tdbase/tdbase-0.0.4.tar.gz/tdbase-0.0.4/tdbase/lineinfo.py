# lineinfo implementation

import re
from typing import Union, Dict, List, Generator, Tuple, Optional


class LineInfo:
    _rec_name_pattern = r"[a-zA-Z_](?:[-./]?[a-zA-Z0-9_])*"       # TODO: allow quoted names? Note that we allow "-./" inside name, but not at ending or beginning. : cannot be allowed (unless if we support quotes)

    _re_str = r"(?:\"(?:\\\"|[^\"])*\")"
    _re_longstr = r"((?<!\\)\"\"\".*)"
    _re_nostr = r"(?:[^\"#]+)"
    _re_combine = r"((?:" + _re_nostr + r"|" + _re_str + r"|" + _re_longstr + r")*)"
    _pattern1 = re.compile(_re_combine + r"(#.*)?\n?")

    _re_first_or_indent = r"(\.|\[|!|\s*)"
    _re_rec_name_or_key = r"("+_rec_name_pattern+r")?"
    _re_spaces = r"(\s*)"
    _re_rest = r"(.*)"
    _re_data = _re_first_or_indent + _re_rec_name_or_key + _re_spaces + _re_rest
    _pattern2 = re.compile(_re_data)

    _re_value = r"(->|=>|-)?" + r"(\A:)?" + r"(?:\s*)" + "(.*)"
    _pattern3 = re.compile(_re_value)

    _pattern4 = re.compile(r"(?<!\\)\"\"\"")

    _pattern5 = re.compile(r"(\s*)#(.*)")

    def __init__(self, raw_line: str,
                 line_nr: int,
                 indentStack: List[Tuple[int, "LineInfo"]],
                 prev_real_line: Optional["LineInfo"],
                 nextline_func):
        # indentstack is a stack with (indent-levels, ref to first line with that pos)
        # prevRealLine is a reference to the "real" line before this one.

        self._raw_line = raw_line   # just for reference, should not be used
        inp_data: str           # the input line without comment/trailing space (space removed further down after calc comment col)
        long_str_start: str     # has data if unterminated long-str in line
        comment: str            # if there is a comment
        #print ("*", repr(raw_line))
        m = LineInfo._pattern1.fullmatch(raw_line)
        if not m:
            raise Exception("internal error - should always match")
        inp_data, long_str_start, comment = m.groups()  # should match everything!

   #     self.prev_real_line = prev_real_line
        self.typ: str = "#"                 # either # for empty or only comment, or '!':preproc, '.':record, '['=context, 'A'=attrib or list item
       # self.rawFirst = None                # TODO!
        self.indent = -1                    # assume invalid indent
        self.key_or_type: Optional[str] = None      # either record type (without .), or key for attribute. None for comment/empty lines, and list elements
        self.val_type: str = ""             # unknown. For typ==A: "S":str, "P":pointer, "X":external
        self.value_str: str = ""            # str for value. Also content of preproc, context, record data. Also if attribute w/ pointer, use this.
        # self.attr_value: Optional[Union[str, float]] = None  # parsed item value. None if not simple value
        self.is_list_element = False        # whether this is a list element.
        self.comment: Optional[str] = None  # if None, no comment. If str, this is the comment without "#"
        self.comment_col = 0                # which column the comment is on.
        self.line_nr = line_nr              # remember which line this is (or first line for multi-line strs)
        self.indentChange = 0
        self.context: str = ""
        self.extra_long_str:List[str] = []
        self.long_str: str = ""             # will get the long string if available.

        if long_str_start:
            assert (comment is None)
            m2 = LineInfo._pattern4.search(raw_line)
            self.long_str = raw_line[m2.end():].rstrip() + "\n"
            lstr_indent = m2.end()
            while 1:
                l = nextline_func().rstrip()
                m2 = LineInfo._pattern4.search(l)
                if m2:
                    len_for_comment_col = m2.end()
                    after = l[m2.end():]
                    l = l[:m2.start()]
                    if len(l) < lstr_indent:
                        l = ""
                        if l != " " * len(l):
                            raise Exception("long string indent should only be spaces:%s" % l)
                    elif l[:lstr_indent] != " " * lstr_indent:
                        raise Exception("long string indent should only be spaces:%s" % l[:lstr_indent])
                    # found last line
                    self.long_str += l
                    # TODO:special case terminate """ without and data before?
                    if after:
                        m3 = LineInfo._pattern5.fullmatch(after)
                        if not m3:
                            raise Exception("Must be empty or comment after long-str:%s" % after)
                        before,after = m3.groups()
                        self.comment = after
                        self.comment_col = len_for_comment_col + len(before)
                    break

                if len(l) < lstr_indent:
                    l = ""
                    if l != " " * len(l):
                        raise Exception("long string indent should only be spaces:%s" % l)
                else:
                    if l[:lstr_indent] != " " * lstr_indent:
                        raise Exception("long string indent should only be spaces:%s" % l[:lstr_indent])
                    l = l[lstr_indent:]
                self.long_str += l + "\n"
        else:
            # TODO: parse normal strings, escape chars?
            if comment:
                self.comment = comment.rstrip()[1:]     # remove trailing space/LF. Also remove starting #
                self.comment_col = len(inp_data)        # which column the comment is on.

        inp_data = inp_data.rstrip()  # remove trailing space of real data

        if not inp_data:
            return          # empty line (might have comment)

        m = LineInfo._pattern2.fullmatch(inp_data)
        if not m:
            raise Exception("internal error - should always match")

        a, b, c, d = m.groups()
        if b:
            self.key_or_type = b   # either attribute key or record type.
        if len(a) == 1 and a in ".[!":    # record, context or preproc
            self.typ = a[0]
            if a == "[":
                if d != "]":
                    raise Exception("Syntax error %s" % d)
                self.value_str = b
            else:
                self.value_str = d
            self.indent = 0
        else:
            # attribute or list element or similar
            self.indent = len(a)
            m = LineInfo._pattern3.fullmatch(d)
            if not m:
                raise Exception("internal error - should always match")
            pre_val, optional_colon, self.value_str = m.groups()

            self.typ = "A"                 # attrib
            if pre_val is None:  # normal value
                if not self.key_or_type:
                    raise Exception("Must have key")
                self.val_type = "S"
            elif pre_val == "-":
                if self.key_or_type:
                    raise Exception("cannot have key")
                self.val_type = "S"
                self.is_list_element = True
            elif pre_val == "->":
                self.val_type = "P"
                if not self.key_or_type:
                    self.is_list_element = True
            elif pre_val == "=>":
                self.val_type = "X"
                if not self.key_or_type:
                    self.is_list_element = True
            else:
                raise Exception("Internal error")


        assert(self.indent >= 0 and self.typ != "#")
        topIndent: int
        topRef: LineInfo
        topIndent, topRef = indentStack[-1]
        if self.indent == topIndent:
            pass  # do nothing
        elif self.indent > topIndent:
            indentStack.append((self.indent, self))
            topIndent, topRef = indentStack[-1]
            self.indentChange = 1
        else:
        #    prevLine = self.prevRealLine
            while self.indent < topIndent:
                # remobed lastInBlock - think it is not used
                #topRef.lastInBlock = prev_real_line
                indentStack.pop()
                topIndent, topRef = indentStack[-1]
                self.indentChange -= 1
            if self.indent != topIndent:
                raise Exception("Indent lexer error")
        self.firstInBlock = topRef


    def is_empty(self):
        return self.typ == "#" and self.comment is None

    def isAttrib(self):
        """returns true if a line can be part of an attrib. Embedded record defs are all part of an attrib"""
        raise Exception("Check this!")
        if self.indent:
            assert self.rawFirst != ""
            return True
        if self.rawFirst == "" or self.rawFirst[0] in "[!":
            return False
        else:
            return True

    def old_____str__(self):
        if self.firstInBlock:
            fib = "%d" % self.firstInBlock.lineNr
        else:
            fib = "-"

        if self.prevRealLine:
            pv = "%d" % self.prevRealLine.lineNr
        else:
            pv = "-"

        if self.lastInBlock:
            lib = "%d" % self.lastInBlock.lineNr
        else:
            lib = "-"

        f = "%+2d=>%d (L %3d, fib %2s, prev=%2s, lib=%2s):" % (self.indentChange, self.indent, self.lineNr, fib, pv, lib) + " " * self.indent + self.rawFirst
        if self.commentCol:
            c = " "*(self.commentCol-len(f)-1) + "#"+self.comment
            return f+c
        else:
            return f

    def __repr__(self):
        return "<LineInfo L%d>" % self.lineNr


    def getCommentStr(self, length_before_comment: int):
        if self.comment:
            if self.comment_col > length_before_comment:
                pre = " " * (self.comment_col - length_before_comment) + "#"
            else:
                pre = " #"
            if self.comment[0] != " ":
                pre += " "
            return pre+self.comment
        else:
            return ""


dummy_line_info = LineInfo("", -1, [], None, None)
