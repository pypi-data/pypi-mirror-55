# defines nodes from datafiles

import re

from typing import Union, Dict, List, Optional, Tuple, Iterator, ItemsView, TYPE_CHECKING, Set

from .lineinfo import LineInfo

if TYPE_CHECKING:
    from . import parser        # need parser.TDBParser for typechecking

class NodeBlock:
    wbIndentStep = 2        # default recommended indent step for write-back
    wbRecordNameWidth = 20  # default width for record name - will make ID at same column. Set to 0 to not adjust?

    def __init__(self, indent: int):
        self.indent = indent       # TODO: do I need this?
        self.lastLineIdx: Optional[int] = None
        self.children: Optional[Union[List, Dict]] = None        # if has children. None means no children. Can be a list or dict also.

    def prettyPrint(self, indent):
        print(" "*indent + str(self))
        for c in self.children:
            c.prettyPrint(indent+1)

    def dumpToFile(self, fh, indent):
        fh.write(self.dump_to_str(indent))

    def dump_to_str(self, unused_indent, unused_sort_attribs) -> str:
        raise Exception("Need to be implemented in derived class for class %s" % self.__class__.__name__)


class NodePreproc(NodeBlock):
    def __init__(self, li):
        super().__init__(0)
        self.li = li

    def __str__(self):
        return "<Preproc at %d: %s" % (self.li.lineNr, self.li.rawFirst)

    def dump_to_str(self, unused_indent, unused_sort_attribs):
        # TODO: should not use _raw_line
        return self.li._raw_line.rstrip() + "\n"
#        return "%s%s\n" % (self.li._raw_line, self.li.getCommentStr())
    # def dumpToFile(self, fh, unused_indent):
        # fh.write("%s%s\n" % (self.li.first, self.li.getCommentStr()))

class NodeContext(NodeBlock):
    def __init__(self, li):
        super().__init__(0)
        self.li = li

    def __str__(self) -> str:
        return "<Context at %d: %s" % (self.li.lineNr, self.li.rawFirst)

    def dump_to_str(self, unused_indent, unused_sort_attribs) -> str:
        return "[%s]%s\n" % (self.li.value_str, self.li.getCommentStr(len(self.li.value_str)+2))
    # def dumpToFile(self, fh, unused_indent):
        # fh.write("%s%s\n" % (self.li.first, self.li.getCommentStr()))

class NodeComments(NodeBlock):
    def __init__(self):
        super().__init__(None)      # don't know. Should probably inherit from last indent?
        self.lis = []

    def __str__(self):
        return "<Comments %d lines %d-%d" % (len(self.lis), self.lis[0].lineNr, self.lis[-1].lineNr)
    # def dumpToFile(self, fh, indent):
    def dump_to_str(self, indent, unused_sort_attribs) -> str:
        indent = " " * indent
        ret = []
        for c in self.lis:
            if c.comment:
                ret.append(indent + "#" + c.comment + "\n")
            else:
                ret.append("\n")
            #ret.append("%s\n" % (c.getCommentStr(0)))
        return "".join(ret)

# TODO: move to top, and rename
class AccessWrapperBase:
    def _get_owning_accessor(self, k):
        if isinstance(k, (int,str)):  # convenience - access to top attr can be done as str directly
            k = (k,)
        acc = self
        for subk in k[:-1]:  # get the mapp/wrapper for containing obj
            if acc.has_key(subk):
                acc = acc[subk].accessor
            else:
                raise Exception("Need to create a dict or list")
        return acc, k[-1]

    def __setitem__(self, k: str, v:Union[str,int,Tuple[Union[str,int]]]):
        accessor, key = self._get_owning_accessor(k)

        if isinstance(v, int):
            v = str(v)  # TODO: store real types?

        if accessor.has_key(key):
            if isinstance(v, str):
                accessor[key].value = v
                return
            else:
                raise Exception("Not done")

        # create new value
        if isinstance(v, str):
            if isinstance(key, str):
                v = NodeAttrib.create(key, v)
            else:
                raise Exception("not done")
        else:
            raise Exception("not done")

        accessor.add_attrib(key, v)



    def __getitem__(self, k):
        accessor, key = self._get_owning_accessor(k)
        return accessor._getitem(key)

    def __contains__(self, item):
        accessor, key = self._get_owning_accessor(item)
        return accessor.has_key(key)


    def _getitem(self, k):
        raise Exception("Need to be implemented in inherited class")
    def has_key(self, k):
        raise Exception("Need to be implemented in inherited class")
    def add_attrib(self, k: str, v: "NodeAttrib"):
        raise Exception("Need to be implemented in inherited class")

    def __delitem__(self, v):
        raise Exception("Not done")


class AccessWrapperRecord(AccessWrapperBase):
    def __init__(self, record: "NodeRecord"):
        self.node: NodeRecord = record
    def _getitem(self, k):
        return self.node.children[k]
    def has_key(self, k):
        return k in self.node.children
    def add_attrib(self, k: str, v: "NodeAttrib"):
        self.node.children[k] = v

class AccessWrapperAttrib(AccessWrapperBase):
    def __init__(self, node: "NodeAttrib"):
        self.node: NodeAttrib = node
    def _getitem(self, k):
        return self.node.children[k]
    def has_key(self, k):
        if isinstance(k, str):
            return k in self.node.children
        if isinstance(k, int):
            return k >= 0 and k < len(self.node.children)
        raise Exception("errir")
    def add_attrib(self, k: str, v: "NodeAttrib"):
        if isinstance(self.node.children, dict):
            self.node.children[k] = v
        else:
            raise Exception("Cannot add attributes to non-dict, use other functions to append to list")

class DirectedGraph:
    class NodeInfo:
        def __init__(self, record: "NodeRecord", graph: "DirectedGraph"):
            graph.infos.append(self)
            self.record = record
            self.graph = graph
            self.level: int = -1    # -1 means not inited. 0 means under follow_back (to detect loops), >0 means a set value
            self.nexts: Set[NodeRecord] = set()
            self.prevs: Set[NodeRecord] = set()
            if self.record.graph_info:
                raise Exception("cannot replace graph_info")
            self.record.graph_info = self

        def link_nodes(self, ptr_attrib_name, allow_cyclic):
            self.graph.records_in_graph.add(self.record)
            if not ptr_attrib_name in self.record.attr:
                return
            attr = self.record.attr[ptr_attrib_name]
            if attr.children:
                assert(isinstance(attr.children, list))
                for child in attr.children:
                    assert(child.pointer)
                    self.nexts.add(child.pointer.record)
            elif attr.pointer:
                self.nexts.add(attr.pointer.record)
            elif attr.value:
                raise Exception("not a pointer")

            for r in self.nexts:
                if not r.graph_info:
                    ni = DirectedGraph.NodeInfo(r, self.graph)
                    ni.link_nodes(ptr_attrib_name, allow_cyclic)

                r.graph_info.prevs.add(self.record)

        def follow_back(self, allow_cyclic):
            if self.level > 0:
                return  # nothing to do - we have already set our level
            max_prev = 0
            self.level = 0
            for r in self.prevs:
                if r.graph_info.level < 0:
                    r.graph_info.follow_back(allow_cyclic)
                if r.graph_info.level == 0:
                    # the node referring to us are under calculation - means this is cyclic.
                    if not allow_cyclic:
                        raise Exception("Cyclic")
                if r.graph_info.level > max_prev:
                    max_prev = r.graph_info.level
            self.level = max_prev + 1

    # TODO: option to add many records, if we don't know who is "first"?
    def __init__(self, first_record_or_iterator: Union["NodeRecord", Iterator], ptr_attrib_name, allow_cyclic=False):
        #raise Exception()
        self.infos: List[DirectedGraph.NodeInfo] = []
        self.first = None
        self.records_in_graph:Set[NodeRecord] = set()

        if isinstance(first_record_or_iterator, NodeRecord):
            self.first = DirectedGraph.NodeInfo(first_record_or_iterator, self)
            self.first.link_nodes(ptr_attrib_name, allow_cyclic)
        else:
            for r in first_record_or_iterator:
                ni = DirectedGraph.NodeInfo(r, self)
                if self.first is None:
                    self.first = ni
                print (r)
            for ni in self.infos:
                ni.link_nodes(ptr_attrib_name, allow_cyclic)

        for ni in self.infos:
            ni.follow_back(allow_cyclic)


# defines a pointer to a record.
class RecordPointer:
    def __init__(self,
                 def_str: str,
                 firstRealLineInfo,
                 parser=None):
        if def_str:
            assert(parser)
        self.def_str = def_str
        self.firstRealLineInfo = firstRealLineInfo
        self.parser = parser  # only used to get UID->str function (!). Should have some other context variable.
        self.record = None  # record  # reference to record. If not mapped records and not embedded records, this is a "dummy" record
        self.embedded = False  # is the record actually defined here?

        # same definition as in record
        self.record_id: bytes = b""  # ID for the record, or unknown
        self.record_type: str = ""  # undefined
        self.record_name: str = ""  # name for this record
        self.inherit = None

        if def_str:
            m = NodeRecord.match_record_ptr.match(def_str)
            if not m:
                raise Exception("Internal error")
            #rec_typ, n, rid, inh_n, inh_rid = m.groups()
            rec_typ, n, rid, inh_n, inh_rid = m.groups()
            if rec_typ:
                self.record_type = rec_typ
            if inh_n or inh_rid:
                self.inherit = (inh_n,inh_rid)      # TODO: later on, redefine this as reference to inherited object - then use this for get_dict (read-only).
                raise Exception("TODO")
            if n:
                self.record_name = n
            assert(isinstance(self.record_name, str))
            if rid:
                self.record_id = parser.decode_record_uid(rid)  # remove <>.

    def emb_head_to_str(self):
        if self.record:
            return self.record.emb_head_to_str()
        elif self.def_str:
            return NodeRecord.gen_header_str(self.record_type, self.record_name, self.record_id, self.parser)
        else:
            return "<TODO should return encoding for empty pointer>"

    def get_uid_as_str(self):
        if not self.record:
            raise Exception("No record")
        if self.parser:
            return self.parser.encode_record_uid(self.record.record_id)
        else:
            raise Exception("don't have parser pointer")


empty_record_pointer = RecordPointer("", None)


class NodeRecord(NodeBlock):
    rec_type_pattern = r"(?:\.(" + LineInfo._rec_name_pattern + r"))"
    rec_name_pattern = r"(?:(" + LineInfo._rec_name_pattern + "))?"
    rec_id_pattern = r"(?:<([^ \t<>]+)>)?"
    opt_space = r"\s*"
    inherit_pattern = r"(?:\(" + opt_space + rec_name_pattern + opt_space + rec_id_pattern + opt_space + r"\)" + opt_space + r")?"
    match_record = re.compile(rec_name_pattern + opt_space + rec_id_pattern + opt_space + inherit_pattern + r":?")
    match_record_ptr = re.compile(rec_type_pattern + r"?" + opt_space + rec_name_pattern + opt_space + rec_id_pattern + opt_space + inherit_pattern + r":?")

    def __init__(self, preComments, firstRealLineInfo:LineInfo, parser, ptr:Optional[RecordPointer]=None):
        super().__init__(firstRealLineInfo.indent)
        self.preComments = preComments
        self.firstRealLineInfo = firstRealLineInfo
        self.parser = parser
        self.children: Dict[str,NodeAttrib] = {}  # a record always have dict as children (attributes with key/value)
        # self.children: AccessWrapperBase = AccessWrapperBase()  # a record always have dict as children (attributes with key/value)

        self.record_id: bytes = b""  # ID for the record, or unknown
        self.record_name: str = ""  # name for this record
        self.record_type: str = ""  # undefined
        self.inherit: Optional[Tuple[str, str]] = None
        self.accessor = AccessWrapperRecord(self)

        self.graph_info: Optional[DirectedGraph.NodeInfo] = None   # filled with ref to obj to calculate directed graph structure

        if not ptr:
            if self.firstRealLineInfo.key_or_type:
                self.record_type = self.firstRealLineInfo.key_or_type
            m = NodeRecord.match_record.fullmatch(self.firstRealLineInfo.value_str)
            if not m:
                raise Exception("Record bad format in line %d: %s" % (self.firstRealLineInfo.line_nr, self.firstRealLineInfo.value_str))
            # print (m.groups())
            n, rid, inh_n, inh_rid = m.groups()
            if inh_n or inh_rid:
                self.inherit = (inh_n, inh_rid)      # TODO: later on, redefine this as reference to inherited object - then use this for get_dict (read-only).
            if rid:
                self.record_id = parser.decode_record_uid(rid)  # remove <>.
        else:
            self.record_type, n, self.record_id, self.inherit = ptr.record_type, ptr.record_name, ptr.record_id, ptr.inherit

        if n:
            self.record_name = n
        assert(isinstance(self.record_name,str))

        self.embedded_records: List["NodeRecord"] = []   # if this is an outer record, this is a list of all embedded defined records.

    def __lt__(self, other):
        return self.record_name < other.record_name

    @classmethod
    def create_embedded(cls, record_ptr: RecordPointer, parser) -> "NodeRecord":
        return cls(None, record_ptr.firstRealLineInfo, parser, ptr=record_ptr)

    def check_rec_references(self, name_map, id_map):
        for attr in self.children.values():
            attr.check_rec_references(name_map, id_map)

    def set_record_name(self, new_name: str):
        self.record_name = new_name

    def get_uid_as_str(self) -> str:
        return self.parser.encode_record_uid(self.record_id)

    def iter_attribs(self) -> ItemsView[str, 'NodeAttrib']:
        return self.children.items()

    def get_attrib_map_copy(self) -> dict:
        """returns a python dict which is a copy of the records attributes. Ie, changes there are not reflected in the record object"""
        ret = {}
        for k, c in self.children.items():
            ret[k] = c._get_as_std_copy()
        return ret

    @property
    def attr(self):
#    def attr(self) -> Dict[str, 'NodeAttrib']:
        return self.accessor
        # return self.children

    @attr.setter
    def attr(self):
        raise Exception("Cannot overwrite whole dict of Record")

    def _get_sort_str(self, sort_order: str) -> Tuple[str, str, Union[str,bytes]]:
        if sort_order is None:
            return "", "", ""
        if sort_order == "TN":  # type, then name, finally id
            return self.record_type, self.record_name, self.record_id
        raise Exception("Not done %s" % sort_order)


    def __str__(self):
        return "<Record from %d, %d attribs>" % (self.firstRealLineInfo.line_nr, len(self.children))

    def dump_to_str(self, indent, sort_attribs, skip_header=False) -> str:
        ret = []
        if self.preComments:
            ret.append(self.preComments.dump_to_str(indent, sort_attribs))

        if not skip_header:
            s = self.emb_head_to_str()
            s = s.strip() + ":"
            ret.append("%s%s\n" % (s, self.firstRealLineInfo.getCommentStr(len(s))))

        keys = sort_attrib_keys(self.children, sort_attribs)
        for k in keys:
            a = self.children[k]
            ret.append(a.dump_to_str(indent + NodeBlock.wbIndentStep, sort_attribs))

        return "".join(ret)

    @classmethod
    def gen_header_str(cls, typ, name, rid, parser):
        if name:
            n = "%-*s" % (NodeBlock.wbRecordNameWidth, name)
        else:
            n = " " * NodeBlock.wbRecordNameWidth
        if rid:
            i = " <%s>" % parser.encode_record_uid(rid)
        else:
            i = ""
        if typ:
            return "." + typ + " " + n + i
        else:
            return n + i    # note that for embedded records that have not been mapped/linked, the type can be ""


    def emb_head_to_str(self):
        return NodeRecord.gen_header_str(self.record_type, self.record_name, self.record_id, self.parser)

        # OLD
        if self.record_name:
            n = "%-*s" % (NodeBlock.wbRecordNameWidth, self.record_name)
        else:
            n = " " * NodeBlock.wbRecordNameWidth
        if self.record_id:
            i = " <%s>" % self.get_uid_as_str()
        else:
            i = ""
        if self.record_type:
            return "." + self.record_type + " " + n + i
        else:
            return n + i    # note that for embedded records that have not been mapped/linked, the type can be ""



def sort_attrib_keys(mapp, sort_def):
    if sort_def is None:
        return mapp.keys()
    ret = list(mapp.keys())
    if sort_def == "K":
        ret.sort()
    elif sort_def == "k":
        ret.sort(reverse=True)
    else:
        raise Exception()
    return ret

class NodeAttrib(NodeBlock):
    def __init__(self,
                 preComments: Union[None, NodeComments],           # if there are any pre-comments
                 firstRealLineInfo: Optional[LineInfo],          # optional first line info. If available, some variables will be updated.
                 parser: Optional["parser.TDBParser"] = None,
                 ):
        if firstRealLineInfo:
            super().__init__(firstRealLineInfo.indent)
        else:
            super().__init__(0)

        self.preComments = preComments
        self.firstRealLineInfo = firstRealLineInfo

        self.key: Optional[str] = None  # TODO: remove key here. Better to point to parent if needed?
        self.value: Optional[Union[float, str]] = None  # either the data/value, or None if empty. Note that for pointer or xref, this is None
        self.accessor = AccessWrapperAttrib(self)

        self.todo_remove_emptyListNode = None   # empty list is just a "-", but there might be comments (before and on same line).
        self.pointer: Optional[RecordPointer] = None   # pointer to record if this attribute is a pointer. Note that it points to the same as below if an embedded record definition
        self.xref: Optional[str] = None

        if self.firstRealLineInfo:
            # note that key will be None if list element
            if self.firstRealLineInfo.key_or_type:
                self.key=self.firstRealLineInfo.key_or_type
                assert(self.key[-1] != ":")
                assert(self.key[0] != "-")

            if self.firstRealLineInfo.val_type == "S":
                if self.firstRealLineInfo.value_str:
                    self.value = self.firstRealLineInfo.value_str
                    # TODO: check if float, convert? If option enabled.
            elif self.firstRealLineInfo.val_type == "P":
                self.pointer = RecordPointer(self.firstRealLineInfo.value_str, self.firstRealLineInfo, parser)
            elif self.firstRealLineInfo.val_type == "X":
                # TODO: parse filename and content ID!
                self.xref = self.firstRealLineInfo.value_str
            else:
                raise Exception("Unknown type")


    @classmethod
    def create(cls,
               key: Optional[str],      # key for attribute, or None?
               val: Optional[str] = None,
               children: Optional[Union[List, Dict]] = None,
               pointer: Optional[RecordPointer] = None):
        if not val is None:
            assert(children == None and pointer == None)
        elif not children is None:
            assert(val == None and pointer == None)
        elif not pointer is None:
            assert(val == None and children == None)
        else:
            raise Exception("Maybe OK to create an attrib with no data?")

        ret = NodeAttrib(None, None)
        ret.key = key
        ret.value = val
        ret.children = children
        ret.pointer = pointer

        return ret

    def check_rec_references(self, name_map, id_map):
        if self.pointer and not self.pointer.embedded:  # embedded_record:
            assert (isinstance(self.pointer, RecordPointer))
            if self.pointer.record_id:
                if self.pointer.record_type:
                    self.pointer.record = id_map[self.pointer.record_type][self.pointer.record_id]
                else:
                    for m in id_map.values():
                        if self.pointer.record_id in m:
                            self.pointer.record = m[self.pointer.record_id]
                            break
                    else:
                        raise Exception("Cannot find reference to record id %s" % self.pointer.get_uid_as_str())
            elif self.pointer.record_name:
                if self.pointer.record_type:
                    self.pointer.record = name_map[self.pointer.record_type][self.pointer.record_name]
                else:
                    for m in name_map.values():
                        if self.pointer.record_name in m:
                            self.pointer.record = m[self.pointer.record_name]
                            break
                    else:
                        raise Exception("Cannot find reference to record id %s" % self.pointer.get_uid_as_str())
            else:
                raise Exception("reference must either have name or id")
            assert(not self.children)   # a pure reference cannot have children
            assert (isinstance(self.pointer, RecordPointer))
            return
        elif isinstance(self.children, list):
            for attr in self.children:
                attr.check_rec_references(name_map, id_map)
        elif isinstance(self.children, dict):
            for attr in self.children.values():
                attr.check_rec_references(name_map, id_map)
        else:
            assert(self.children is None)

    def _get_as_std_copy(self):
        if not self.children:
            return self.value

        if isinstance(self.children, dict):
            ret = {}
            for k, v in self.children.items():
                ret[k] = v._get_as_std_copy()
            return ret
        elif isinstance(self.children, list):
            return [c._get_as_std_copy() for c in self.children]
        else:
            raise Exception()


    def __str__(self):
        return "<Attrib from %d (comment before: %s): %s>" % (self.firstRealLineInfo.line_nr, self.preComments, self.firstRealLineInfo._raw_line)

    def get_comment_str_lf(self, pre_comment_len: int):
        if self.firstRealLineInfo:
            return self.firstRealLineInfo.getCommentStr(pre_comment_len) + "\n"
        else:
            return "\n"

    def dump_to_str(self, indent, sort_attribs) -> str:
        # TODO: should check if children, pointer or xref first, then handle normal str/data. Also, remove dependency on key.

        assert(self.pointer is None or isinstance(self.pointer, RecordPointer))
        ret = []
        if self.preComments:
            ret.append(self.preComments.dump_to_str(indent, sort_attribs))
        indentStr = " " * indent
        if self.value is None or self.value == "":
            v = ""
        else:
            v = " "+str(self.value)
        if self.key is None:
            # we're a list element:
            if self.pointer:  # list element is a ptr to another record
                pre_comment = "%s-> %s" % (indentStr, self.pointer.emb_head_to_str().rstrip())
                # ret.append("%s-> %s%s\n" % (indentStr, self.pointer.emb_head_to_str().rstrip(), self.firstRealLineInfo.getCommentStr()))
            else:
                pre_comment = "%s-%s" % (indentStr, v)
          #      ret.append("%s-%s%s\n" % (indentStr, v, self.firstRealLineInfo.getCommentStr()))
            ret.append(pre_comment + self.get_comment_str_lf(len(pre_comment)))
        else:
            if self.pointer:
                colon_or_ptr = " ->"
                v = " " + self.pointer.emb_head_to_str().rstrip()
                if self.pointer.embedded:
                    v += ":"
            else:
                colon_or_ptr = ":"
            pre_comment = "%s%s%s%s" % (indentStr, self.key, colon_or_ptr, v)
            ret.append(pre_comment + self.get_comment_str_lf(len(pre_comment)))

        if self.pointer and self.pointer.embedded:
            assert(self.pointer.record)
            assert(not self.children)
            assert(self.value is None)
            assert(self.pointer.record_type == self.pointer.record.record_type)
            assert(self.pointer.record_name == self.pointer.record.record_name)
            assert(not self.pointer.record_id or self.pointer.record_id == self.pointer.record.record_id)
            ret.append(self.pointer.record.dump_to_str(indent, sort_attribs, skip_header=True))
        elif self.children is None or not self.children:
            # essentially do nothing, note that value can be None now
            # the last check is a hack to handle empty list/dict
            pass
        else:
            assert(self.value is None)
            #assert(self.embedded_record is None)
            if isinstance(self.children, dict):
                assert(self.children)  # should not be an empty dict (should be saved as None)
                keys = sort_attrib_keys(self.children, sort_attribs)
                for k in keys:
                    c = self.children[k]
                    ret.append(c.dump_to_str(indent + NodeBlock.wbIndentStep, sort_attribs))
            elif isinstance(self.children, list):
                assert(self.children)  # should not be an empty list (should be saved as None)
                for c in self.children:
                    ret.append(c.dump_to_str(indent + NodeBlock.wbIndentStep, sort_attribs))
            else:
                raise Exception("Internal error")

        return "".join(ret)


