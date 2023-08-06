#!python3
import io
import os
import re
import sys
import base64
import binascii
import struct
import secrets
import typing
from typing import Union, Dict, List, Optional, Set, Iterator

from . import nodes
from .lineinfo import LineInfo, dummy_line_info

#import binascii
# raise Excpetion("""
# TODO:
    # Let parser find comment/empty lines directly, mark them. Also find line-spanning things (mainly triple-quotes now)
    # For indenter, maybe try to group blocks? Maybe class which represents blocks. Another class which represents LineWithContent.
    # """)





#######################################################################################################################


class FileLexAndParse:
    matchInclude = re.compile("!include[ ]+\"([^\"]+)\"")

    def __init__(self, filename, parser, initialContext, filecontent=None):
        """filecontent should normally be None. If not, the file is not read from fs"""
        self.filename = filename
        if filecontent is None:
            self.absFilename = os.path.abspath(filename)
            self.myDir = os.path.abspath(os.path.join(filename, ".."))
        else:
            self.absFilename = None
            self.myDir = None

        self.parser = parser
        self.lines = []

        self.parser._add_file_obj(self)    # add me to the parser

        self._lex(initialContext, filecontent)  # don't need the object, data is filled into self.

        # needed for parsing:
        self.currentLineIdx = 0
        self.nodes = []
        self.la = None

        self.parseFile()


    def _next_line(self) -> Optional[str]:
        if self._fh:
            r = self._fh.readline()
            if not r:
                return None
        else:
            assert (self._content)
            if self._content_idx >= len(self._content):
                return None
            r = self._content[self._content_idx]
            self._content_idx += 1
        self._line_nr += 1
        return r

    def _lex(self, initial_context, filecontent) -> None:
        self._fh: Optional[typing.IO] = None
        self._content: Optional[List[str]] = None
        self._content_idx = 0

        if self.absFilename:
            with open(self.absFilename, "rt") as fh:
                self._fh = fh
                self._lex2(initial_context)
        else:
            self._content = filecontent.split("\n")
            self._lex2(initial_context)
            del self._content  # no need to keep this in memory

    def _lex2(self, initial_context: str) -> None:
        context = initial_context
        indentStack = [(0, dummy_line_info)]      # a stack of (indent pos, line reference to first line of indent pos)
        prev_line = None
        self._line_nr = 0

        while 1:
            raw_line = self._next_line()
            if raw_line is None:
                break

            li = LineInfo(raw_line, self._line_nr, indentStack, prev_line, self._next_line)
            if li.typ == "[":
                context = li.value_str
            li.context = context

            if li.typ == "!":   # preproc:
                if li.key_or_type == "include":
                    if li.value_str[0] != '"' or li.value_str[-1] != '"':
                        raise Exception("Include should have quoted str")
                    fn = li.value_str[1:-1]
                    FileLexAndParse(os.path.join(self.myDir, fn), self.parser, context)
                else:
                    raise Exception("unknown preproc dir")

            else:
                if li.typ != "#":
                    prev_line = li
#                if li.rawFirst:
#                    prevLine = li

            self.lines.append(li)

        # always remove last lines that are empty
        while len(self.lines) and self.lines[-1].is_empty():
            self.lines = self.lines[:-1]












    def _dump_recs(self, record_nodes: List[nodes.NodeRecord]) -> List[str]:
        """internal helper, returns strs in sorted order according to self"""
        ret = []
        for rec in record_nodes:
            ret.append(rec.dump_to_str(0, self.parser.sort_attribs))
        return ret

    def write_back(self):
        if not self.absFilename:
            raise Exception("file %s not from read file" % self.filename)
        with open(self.absFilename, "wt", newline="\n") as fh:
            fh.write(self.write_back_to_str())

    def write_back_to_str(self) -> str:
        ret: List[str] = []
        if self.parser.sort_records:
            recs = []
            for n in self.nodes:
                if isinstance(n, nodes.NodeRecord):
                    recs.append(n)
                else:
                    sort_recs = [(r._get_sort_str(self.parser.sort_records), r) for r in recs]
                    sort_recs.sort()
                    recs = [r for s, r in sort_recs]
                    ret += self._dump_recs(recs)
                    recs = []
                    ret.append(n.dump_to_str(0, self.parser.sort_attribs))
            sort_recs = [(r._get_sort_str(self.parser.sort_records), r) for r in recs]
            sort_recs.sort()
            recs = [r for s, r in sort_recs]
            ret += self._dump_recs(recs)
        else:
            for n in self.nodes:
                ret.append(n.dump_to_str(0, self.parser.sort_attribs))
        return "".join(ret)

    def _collect_records(self, records: List[nodes.NodeRecord]):
        for n in self.nodes:
            if isinstance(n, nodes.NodeRecord):
                records.append(n)
                for emb in n.embedded_records:
                    records.append(emb)



    ###################################
    # parse functions:

    def lookaheadType(self):
        """sets self.la to the type we're curently looking at"""
        if self.currentLineIdx >= len(self.lines):
            self.la = None
        else:
            self.la = self.lines[self.currentLineIdx].typ

    def parseFile(self):
        self.nodes = []
        while 1:
            self.lookaheadType()

            # matcher = MatcherParser(lineIdx, self.lines)
            if self.la is None:
                break   # EOF

            if self.matchPreproc():
                pass
            elif self.matchContext():
                pass
            elif self.matchRecord():
                pass
            elif self.matchComments():
                pass
            else:
                raise Exception("Parse error at line %d" % (self.currentLineIdx+1))

            self.nodes.append(self.match)
            # print ("Found block", self.match)

    def matchComments(self):
        if self.la != "#":
            return False

        self.match = nodes.NodeComments()
        while self.la == "#":
            self.match.lis.append(self.lines[self.currentLineIdx])
            self.currentLineIdx += 1
            self.lookaheadType()
        self.match.lastLineIdx = self.currentLineIdx - 1
        return True

    def matchPreproc(self):
        if self.la!="!":
            return False
        self.match = nodes.NodePreproc(self.lines[self.currentLineIdx])
        self.match.lastLineIdx = self.currentLineIdx
        self.currentLineIdx += 1
        return True

    def matchContext(self):
        if self.la!="[":
            return False
        self.match = nodes.NodeContext(self.lines[self.currentLineIdx])
        self.match.lastLineIdx = self.currentLineIdx
        self.currentLineIdx += 1
        return True

    def matchRecord(self):
        tb = self.getTraceback()

        if self.matchComments():
            preComments = self.match
            self.lookaheadType()
        else:
            preComments = None

        if self.la!=".":        # record
            self.setTraceback(tb)
            return False

        record = nodes.NodeRecord(preComments, self.lines[self.currentLineIdx], self.parser)
        self.currentLineIdx += 1
        attribIndent = -1  # which indent all attribs should have. set to -1 first, to allow both non-indented and indented, and also be able to differentiate indent 0 from non-set
        while 1:
            self.lookaheadType()
            if not self.matchAttribOptionalPreComment(attribIndent, record):    # allow both non-indented and indented first attrib
                break
            if attribIndent<0:
                attribIndent = self.match.indent
                # print ("First indent:", attribIndent)
            if self.match.indent != attribIndent:
                raise Exception("Internal error %d!=%d in %s@%d" % (self.match.indent, attribIndent, self.filename, self.currentLineIdx))
            assert(isinstance(self.match, nodes.NodeAttrib))
            record.children[self.match.key] = self.match
            self.currentLineIdx = self.match.lastLineIdx+1
        record.lastLineIdx = self.currentLineIdx-1
        self.match = record

        return True

    def matchEmbeddedRecord(self, minMatchIndex, record_ptr) -> Optional[nodes.NodeRecord]:
        tb = self.getTraceback()

        # might not be a valid record, if no attribs following. However, use the constructor to decode the type, name, ID
        # record = nodes.NodeRecord.create_embedded(record_ptr.def_str, record_ptr.firstRealLineInfo, self.parser)
        record = nodes.NodeRecord.create_embedded(record_ptr, self.parser)
        while 1:
            self.lookaheadType()
            if not self.matchAttribOptionalPreComment(minMatchIndex, record):
                break
            assert(isinstance(self.match, nodes.NodeAttrib))
            assert(isinstance(self.match.key, str))
            assert(isinstance(self.match.lastLineIdx, int))
            record.children[self.match.key] = self.match
            self.currentLineIdx = self.match.lastLineIdx+1
        record.lastLineIdx = self.currentLineIdx - 1

        if record.children:
            self.match = record
            return record
        else:
            self.setTraceback(tb)
            return None


    def matchAttribOptionalPreComment(self, minMatchIndex: int, parent_record: nodes.NodeRecord):
        tb = self.getTraceback()

        if self.matchComments():
            preComments = self.match
            self.lookaheadType()
        else:
            preComments = None

        if self.la != "A":      # Attrib or list element
            self.setTraceback(tb)
            return False

        if self.lines[self.currentLineIdx].indent < minMatchIndex:
            self.setTraceback(tb)
            return False

        n = nodes.NodeAttrib(preComments, self.lines[self.currentLineIdx], parser=self.parser)
        assert(n.children is None)  # at creation, we don't know what the children are (if any).
        self.currentLineIdx += 1

        if n.pointer:
            # is a pointer
            if self.matchEmbeddedRecord(n.indent + 1, n.pointer):
                assert(isinstance(self.match, nodes.NodeRecord))
                n.pointer.record = self.match
                n.pointer.embedded = True
                parent_record.embedded_records.append(n.pointer.record)
        elif n.xref:
            pass  # do nothing, is just an xref
        elif n.value is None:
            # TODO should check that we're not a xref too
            # so we're optionally a list or sub-dict
            while 1:
                self.lookaheadType()
                if self.matchAttribOptionalPreComment(n.indent + 1, parent_record):
                    assert (self.match.firstRealLineInfo.typ == "A")
                    # got embedded attrib
                    if self.match.firstRealLineInfo.is_list_element:   # children is a list.
                        if n.children is None:
                            n.children = []  # first item in list
                        elif not isinstance(n.children, list):
                            raise Exception("Parsing error, all items should be list items")
                        n.children.append(self.match)
                    else:
                        if n.children is None:
                            n.children = {}  # first item in dict
                        elif not isinstance(n.children, dict):
                            raise Exception("Parsing error, all items should be key/value, ie cannot start with -")
                        if self.match.key in n.children:
                            raise Exception("Duplicate key!")
                        n.children[self.match.key] = self.match
                else:
                    break

        # TODO: improve parsing here! Embedded records in lists etc.
        if 0:
            if n.value:
                if n.firstRealLineInfo.val_type == "S":         # normal data (str). Convert to float if possible?
                    raise Exception("Not done")
                elif n.firstRealLineInfo.val_type == "P":         # pointer to other record. Could be inline definition too
                    raise Exception("Not done")
                elif n.firstRealLineInfo.val_type == "X":       # reference to external file
                    raise Exception("Not done")
                else:
                    raise Exception("Unkown type %s" % n.firstRealLineInfo.val_type)


            else:  # doesn't have a value, must be NULL, dict or list
                raise Exception("Not done")

        n.lastLineIdx = self.currentLineIdx - 1
        self.match = n
        return True

        ##############################
        # OLD



        if not n.value:  # attrib without value, then is list or dict.
            # if n.firstRealLineInfo.is_pointer:
            if n.firstRealLineInfo.typ == "P":
                raise Exception("Pointer to empty data?")
            while 1:
                self.lookaheadType()
                if self.matchAttribOptionalPreComment(n.indent + 1, parent_record):
                    if self.match.firstRealLineInfo.is_list_element:   # children is a list.
                    #if self.match.firstRealLineInfo.rawFirst[0]=="-":   # children is a list.
                        if n.children is None:
                            n.children = []  # first item in list
                        if not isinstance(n.children, list):
                            raise Exception("Parsing error, all items should start with -")
                        n.children.append(self.match)
                    elif self.match.firstRealLineInfo.typ in "PX":
                        raise Exception("TODO?")
                    else:
                        # if child doesn't start with "-" or "->" or "=>", then it is a dict
                        assert (self.match.firstRealLineInfo.typ == "A")
                        if n.children is None:
                            n.children = {}  # first item in dict
                        if not isinstance(n.children, dict):
                            raise Exception("Parsing error, all items should be key/value, ie cannot start with -")
                        if self.match.key in n.children:
                            raise Exception("Duplicate key!")
                        n.children[self.match.key] = self.match
                else:
                    break
        elif n.firstRealLineInfo.val_type=="P":    # attribute to pointer?
            n.pointer = nodes.RecordPointer(n.value, n.firstRealLineInfo, self.parser)
            # record = nodes.NodeRecord.create_embedded(n.pointer)      # might be dummy record
            #n.pointer.record = record
            if self.matchEmbeddedRecord(n.indent + 1, n.pointer):
                assert(isinstance(self.match, nodes.NodeRecord))
                n.pointer.record = self.match
                n.pointer.embedded = True
                parent_record.embedded_records.append(n.pointer.record)
            n.value = None
        elif n.firstRealLineInfo.val_type == "X":    # external file reference
            raise Exception("Not done")
        else:
            # attribute with normal data.
            assert (n.firstRealLineInfo.val_type == "S")

        if n.children is None and n.value is None:
            n.children = {}  # empty if no value
        # remove special format for empty list
#        if isinstance(n.children, list) and len(n.children) == 1 and n.children[0].firstRealLineInfo.rawFirst == "-":
#            n.emptyListNode = n.children[0]
#            n.children = [] # special format for empty list. Ie, the only element is a "-" without data.
#            # print ("XXXXX", n.key)
        if not n.children is None:
            assert(not n.value) # can be both None or "", as it initially is copied from LineInfo which doesn't have context
            n.value = None
        # print (n)
        n.lastLineIdx = self.currentLineIdx-1
        self.match = n
        return True

    def getTraceback(self):
        return self.currentLineIdx

    def setTraceback(self, tb):
        self.currentLineIdx = tb
        self.lookaheadType()


########################################################################################################################################

class TDBParser:
    def __init__(self, filename=None, filecontent=None):
        # TODO: options for writeback: sort records (within file/context). Sort attribs? Add mandatory attribs?
        self.set_uid_funcs(self.default_encode_record_uid, self.default_decode_record_uid, 0)

        self.files: List[FileLexAndParse] = []
        self.mapFiles = {}
        nodes.NodeBlock.wbIndentStep = 2      # recommended indent step
        self._records_all: [nodes.NodeRecord] = []      # list of all records from all files.
        self.records_id_map: Optional[Dict[str, Dict[bytes, nodes.NodeRecord]]] = None    # record-type, then a dict with uid=>record
        self.records_name_map: Optional[Dict[str, Dict[str, nodes.NodeRecord]]] = None    # record-type, then a dict with name=>record.
        self.uid_len: int = 18        # default
        self.validRecordTypes = set()

        self.assign_continuous_id = 0     # if 0, then disabled. Set to nr > 0 to assign continuous IDs

        self.mainFile = None
        self.schemas = {}   # keys are record types, value is the schema-map

        self.sort_records = None
        self.sort_attribs = None

        if filename:
            self.parse(filename, filecontent)

    def set_assign_id_continuous(self, val: int):
        """if val is 0, then normal op(random vals). if > 0, then use that nr, then increment, for automatic testing"""
        self.assign_continuous_id = val

    def set_sort(self, sort_records=None, sort_attribs=None):
        """sort_records defines how to sort the records. sort_attribs defines how to sort attributes inside records.
        Records: None: no sorting. "TN": first on type, then name. "TI" first type, then index.
        attribs: "K" is for keyname, "S" for schema order, "SK" first schema, then keyname.
        """
        if not sort_records is None:
            sort_records = sort_records.upper()
            if sort_records not in ("TN", "TI"):
                raise Exception("Invalid record sort def")
        self.sort_records = sort_records

        if not sort_attribs is None:
            sort_attribs = sort_attribs.upper()
            if sort_attribs not in ("K", "S", "SK"):
                raise Exception("invalid sort_Attribs")

        self.sort_attribs = sort_attribs

    def parse(self, filename: str, filecontent: str = None):
        """if filecontent, then file is not opened from file system"""
        self.mainFile = FileLexAndParse(filename, self, None, filecontent)
        # collect records, ie, go through the parsed data nodes, and map record Data structures to them.
        for f in self.files:
            f._collect_records(self._records_all)

    def iter_all_records(self, record_typ=None) -> Iterator[nodes.NodeRecord]:
        for r in self._records_all:
            if record_typ and record_typ != r.record_type:
                continue  # skip this one
            yield r

    def get_singleton_record(self, record_typ: str) -> nodes.NodeRecord:
        recs = list(self.iter_all_records(record_typ))
        if len(recs) != 1:
            raise Exception("Not singleton")
        return recs[0]

    def get_record(self, record_typ: str, name: Optional[str] = None, uid: Optional[bytes] = None) -> nodes.NodeRecord:
        if name and uid:
            raise Exception("Either one")
        if name:
            if not self.records_name_map:
                raise Exception()
            return self.records_name_map[record_typ][name]
        elif uid:
            if not self.records_id_map:
                raise Exception()
            return self.records_id_map[record_typ][uid]
        else:
            raise Exception("need name or uid")

    def record_by_idx(self, idx: int) -> nodes.NodeRecord:
        return self._records_all[idx]

    def add_valid_record_types(self, types: Union[str, Set[str], List[str]]):
        if isinstance(types, str):
            types = [types]
        self.validRecordTypes |= set(types)

    def set_uid_funcs(self, encodeFunc, decodeFunc, uid_len: int):
        self.encode_record_uid = encodeFunc
        self.decode_record_uid = decodeFunc
        self.uid_len = uid_len

    def add_record_schema(self, record_type: str, schema: dict, add_to_valid_types=False):
        if add_to_valid_types:
            self.add_valid_record_types(record_type)
        if self.validRecordTypes and record_type not in self.validRecordTypes:
            raise Exception("Cannot add schema for non-allowed record type. Add it with add_valid_record_types() first")
        self.schemas[record_type] = schema
        # print (record_type)
        # for k,v in schema.items():
            # print (" ",k,v)

    def check_schema(self):
        if self.validRecordTypes:
            for r in self.iter_all_records():
                if r.record_type not in self.validRecordTypes:
                    raise Exception("Invalid record type %s" % r.record_type)

        def create_default(key, schema_typ: Union[Dict, List, type]) -> nodes.NodeAttrib:
            if isinstance(schema_typ, dict):
                ret = nodes.NodeAttrib.create(key, children={})
                # t.val = ""   # empty str
                for (k, option), typ in schema_typ.items():
                    if "A" in option:
                        ret.children[k] = create_default(k, schema_typ[(k, option)])
                    # print (k, option, typ)
                    # TODO check?
            elif isinstance(schema_typ, list):
                if len(schema_typ) != 1:
                    raise Exception("Type of all members should be the same, ie only/exactly one type in the list. Use [None] to indicate list of anything")
                ret = nodes.NodeAttrib.create(key, children=[])
                # return DataAttrib(None, key, [])
            elif isinstance(schema_typ, str) and schema_typ[:2] == "->":
                ret = nodes.NodeAttrib.create(key, pointer=nodes.empty_record_pointer)
            elif issubclass(schema_typ, (str, int)):
                ret = nodes.NodeAttrib.create(key, "")
            else:
                print (repr(schema_typ))
                raise Exception()
            return ret

        def check_schema_item(attr: nodes.NodeAttrib, typ):
            if attr.value is None and (attr.children is None or attr.children == {}) and attr.pointer is None:
                return create_default("", typ)
            elif isinstance(typ, str) and typ[:2] == "->":
                record_typ = typ[2:].strip()
                if not attr.pointer:
                    raise Exception("Should point to record, but is value '%s'" % attr.value)
                if attr.pointer.record_type:
                    if attr.pointer.record_type != record_typ:
                        raise Exception("Bad record pointer")
                else:
                    attr.pointer.record_type = record_typ
            elif isinstance(attr.value, typ):
                pass
            else:
                raise Exception("Not Done")

            return attr

        def check_schema_dict(attrs: Dict[str, nodes.NodeAttrib], schema):
            # this can be optimized by pre-calculating the schema
            # print ("Got map", schema, attrs)
            typ: Union[type, List, Dict]   # valid types for typ
            schema_keys = {}

            for (k, option), typ in schema.items():
                schema_keys[k] = (option, typ)
                if "R" in option and k not in attrs:
                    raise Exception("Missing required key %s" % k)
                if "A" in option:
                    if k not in attrs:    # add mandatory option:
                        attrs[k] = create_default(k, typ)
                        #print ("XXX", k)
                    elif attrs[k].value is None and attrs[k].pointer is None and (attrs[k].children is None or attrs[k].children == {}):
                        # note that before schema, empty value means empty dict. Thus, gets an empty dict here.
                        attrs[k] = create_default(k, typ)
            for k, attrib_obj in attrs.items():
                if k in schema_keys:
                    option, typ = schema_keys[k]
                elif "" in schema_keys:
                    option, typ = schema_keys[""]
                else:
                    raise Exception("bad attribute key %s" % k)

                if attrib_obj.value is None and attrib_obj.children is None and attrib_obj.pointer is None:
                    if isinstance(typ, (list, dict, str)):
                        dummy_node = create_default("", typ)
                        attrib_obj.children = dummy_node.children
                    elif typ:
                        attrib_obj.value = typ()

                if typ is None: # allow anything:
                    continue
                elif isinstance(typ, tuple):    # list of allowed types
                    raise Exception("Not done")
                elif isinstance(typ, list):
                    if not isinstance(attrib_obj.children, list):
                        raise Exception()
                    if len(typ) == 0:
                        pass  # allow any items in the list
                    elif len(typ) == 1:
                        attrib_obj.children = [check_schema_item(child, typ[0]) for child in attrib_obj.children]
                    else:
                        raise Exception("type list must be of length 0 or 1")
                elif isinstance(typ, dict):
                    if None in typ and attrib_obj.children is None:
                        # OK: if None key in dict, it means we allow empty dicts.
                        # TODO: add a dict. How to represent empty dict in file format?
                        # attrib_obj.children = {}  # however, make an empty dict as children
                        # print (typ, attrib_obj)
                        attrib_obj.children = {}
                        pass
                    elif not isinstance(attrib_obj.children, dict):
                        raise Exception("%s:%s" % (k, attrib_obj.children))
                    check_schema_dict(attrib_obj.children, typ)
                elif isinstance(typ, str) and typ[:2] == "->":
                    record_typ = typ[2:].strip()
                    #TODO:check correct data type of record
                    if not attrib_obj.pointer:
                        raise Exception("Bad pointer")
                elif isinstance(attrib_obj.value, typ):  # typ is a real typ, check that we matches it.
                    pass
                else:
                    raise Exception("bad attribute %s has bad key %s, wanted type %s" % (k,attrib_obj.value,typ))

        for r in self.iter_all_records():
            if r.record_type in self.schemas:
                check_schema_dict(r.children, self.schemas[r.record_type])
                # check_schema_dict(r.get_attrib_map(), self.schemas[r.recordType])



    def default_encode_record_uid(unused_self, uid: bytes) -> str:
        """takes an id, returns str"""
        # default implementation: encode as base64
        if uid is None:
            return ""
        else:
            return base64.urlsafe_b64encode(uid).decode("ascii")


    def default_decode_record_uid(unused_self, txt: str) -> bytes:
        """takes a str, returns id"""
        # default implementation: encode as base64
        assert(isinstance(txt, str))
        try:
            return base64.urlsafe_b64decode(txt)
        except binascii.Error:
            raise Exception("decode error of %s" % txt)

    def assign_record_uids(self):
        """assign IDs to records that do not have one"""
        for r in self._records_all:
            if r.record_id == b"":
                if self.assign_continuous_id==0:
                    r.record_id = secrets.token_bytes(self.uid_len)
                else:
                    b = struct.pack("<L", self.assign_continuous_id)
                    self.assign_continuous_id += 1
                    r.record_id = b + b"\x00" * (self.uid_len - len(b))
                assert(r.record_id not in self.records_id_map[r.record_type])
                self.records_id_map[r.record_type][r.record_id] = r

    def map_records(self):
        """put all records in a map based on ID (if they have ID). If duplicate records, raises error"""
        self.records_id_map = {}
        self.records_name_map = {}
        for r in self._records_all:
            assert(r.record_type[0] != ".")
            if r.record_type not in self.records_id_map:
                self.records_id_map[r.record_type] = {}
                assert (r.record_type not in self.records_name_map)
                self.records_name_map[r.record_type] = {}
            if r.record_id == b"":
                pass        # TODO: option to not allow no ID
            else:
                if r.record_id in self.records_id_map[r.record_type]:
                    raise Exception("Duplicate record ID %s" % self.encode_record_uid(r.record_id))
                self.records_id_map[r.record_type][r.record_id] = r
            if r.record_name == "":
                pass        # TODO: option to not allow no ID
            else:
    #            if r.record_name.strip() == "Name":
    #                print ("record name", r.record_type, repr(r.record_name))
                if r.record_name in self.records_name_map[r.record_type]:
                    raise Exception("Duplicate record name %s" % r.record_name)
                self.records_name_map[r.record_type][r.record_name] = r

        for rec in self._records_all:
            rec.check_rec_references(self.records_name_map, self.records_id_map)


    def section_records(self):
        """put all records in a map based on context"""
        pass

    def dbg_print_recs(self):
        print ("found %d records" % len(self._records_all))
        for r in self._records_all:
            print (r)

    def _add_file_obj(self, obj):
        # internal use (called from FileLexAndParse)
        if obj.absFilename in self.mapFiles:
            raise Exception("circular inclusion")
        self.files.append(obj)
        self.mapFiles[obj.absFilename] = obj

    def write_back_to_dict(self) -> dict:
        """returns a dict with filenames as keys, and new file content as data"""
        ret = {}
        for f in self.files:
            ret[f.filename] = f.write_back_to_str()
        return ret

    def write_back(self):
        """write backs data to the files they're were read from. Ie, overwrites data"""
        for f in self.files:
            f.write_back()


def read_file(file_name: str,
              file_content: Optional[Union[str, io.TextIOBase]] = None,
              start_id: Optional[int] = None,
              schemas: Optional[dict] = None,
              assign_record_uids: bool = False,
              section_records: bool = False,
              check_schema: bool = False,
              ) -> TDBParser:
    if isinstance(file_content, io.TextIOBase):
        raise Exception("Not implemented")

    p = TDBParser(file_name, file_content)
    if not start_id is None:
        p.set_assign_id_continuous(start_id)

    if schemas:
        for record_type, schema in schemas.items():
            p.add_record_schema(record_type, schema)

    p.map_records()

    if assign_record_uids:
        p.assign_record_uids()

    if section_records:
        p.section_records()

    if check_schema:
        p.check_schema()

    return p




def main():
    # LineInfo.testRegExp()
    # return
    p = TDBParser("../examples/testFile.tdb")

    for f in p.files:
        f.writeBack(f.filename+".out")

#        print (li)
#        print (li.rawLine.rstrip())

if __name__=="__main__":
    main()
