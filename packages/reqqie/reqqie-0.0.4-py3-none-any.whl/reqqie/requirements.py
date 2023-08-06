import os
import sys
from typing import List, Optional, TYPE_CHECKING

import reportlab  # type: ignore
import pygit2  # type: ignore


if 1:
    for upper in ["..", "../.."]:
        test_dir = os.path.join(sys.path[0], upper, "tdbase_git", "tdbase")
        test_dir = os.path.abspath(test_dir)
        #print (test_dir)
        if os.path.exists(test_dir):
            print ("!!!!!!!!!")
            print ("Developing: adding tdbase path:", test_dir)
            print ("!!!!!!!!!")
            sys.path.insert(0, os.path.split(test_dir)[0])
            break

import tdbase

# should be handled by requirements too
pygit2_req_ver = "0.28.2"
if pygit2.__version__ < pygit2_req_ver:
    raise Exception("old pygit2 %s, please update to at least %s" % (pygit2.__version__, pygit2_req_ver))



class WarningError:
    SEVERITY_INFO = 10
    SEVERITY_WARNING = 50
    SEVERITY_ERROR = 100
    SEVERITY_FATAL = 200

    def __init__(self, msg: str, severity: int):
        self.msg = msg
        self.severity: int = severity

    def long_msg(self) -> str:
        severity_str: str
        if self.severity >= WarningError.SEVERITY_FATAL:
            severity_str = "Fatal Error: "
        elif self.severity >= WarningError.SEVERITY_ERROR:
            severity_str = "Error: "
        elif self.severity >= WarningError.SEVERITY_WARNING:
            severity_str = "Warning: "
        elif self.severity >= WarningError.SEVERITY_INFO:
            severity_str = "Info: "
        else:
            severity_str = ""
        return "%s%s" % (severity_str, self.msg)


class Requirements:
    def __init__(self, fn: str):
        self.msgs: List[WarningError] = []

        self._parsed_data = tdbase.read_file(
            fn,
            schemas={
                "config": {
                    ("paths", "A"): [str],
                    ("tags", "A"): [str],
                    ("top_category", "A"): "-> category",
                    ("top_requirement", "A"): "-> req",
                    ("main_levels", "A"): [str],
                    ("req_lifecycle", "A"): [str],
                    ("releases", ""): None,
                },
                "category": {
                    ("name", "A"): str,
                    ("descr", "A"): str,
                    ("next", ""): [],           # TODO: cannot have A yet!
                },
                "release": {
                    ("descr", "A"): str,
                    ("status", "A"): str,
                    ("date", "A"): str,         # TODO: date datatype
                    ("next", ""): None,         # TODO: cannot have A yet!
                    ("", ""): None
                },
                "req": {
                    ("descr", "A"): str,
                    ("def", "A"): str,
                    ("test-spec", "A"): str,
                    ("test", ""): None,
                    ("stage", ""): None,
                    ("depends", ""): ["-> req"],
                },
            },
            assign_record_uids=True,
            check_schema=True,
        )

        self.config_record: Optional[tdbase.nodes.NodeRecord] = None
        self.categories: List[tdbase.nodes.NodeRecord] = []
        self.releases: List[tdbase.nodes.NodeRecord] = []

#        for req in self._parsed_data.iter_all_records("config"):
#            if self.config_record:
#                raise Exception("Can only have one config!")
        self.config_record = self._parsed_data.get_singleton_record("config")
        self.categories = [r for r in self._parsed_data.iter_all_records("category")]
        self.releases = [r for r in self._parsed_data.iter_all_records("release")]

        self.graph_categories: Optional[tdbase.nodes.DirectedGraph] = None
        self.graph_requirements: Optional[tdbase.nodes.DirectedGraph] = None
        self.max_severity: int = 0

        # DAG_of_Records(self.config_record.attr["top_category"])

    def _add_msg(self, msg, severity):
        self.msgs.append(WarningError(msg, severity))

    def analyze(self) -> None:
        try:
            if self.config_record is None:
                self._add_msg("No config record", WarningError.SEVERITY_FATAL)
                return

            top_cat = self.config_record.attr["top_category"]
            top_req = self.config_record.attr["top_requirement"]

            if top_cat.pointer.record:
                self.graph_categories = tdbase.nodes.DirectedGraph(top_cat.pointer.record, "next", allow_cyclic=False)

                missing = set(self._parsed_data.iter_all_records("category")) - self.graph_categories.records_in_graph
                for m in missing:
                    self._add_msg("unreachable category: %s" % m.record_name, WarningError.SEVERITY_ERROR)
            else:
                self._add_msg("No top category", WarningError.SEVERITY_ERROR)

            if top_req.pointer.record:
                self.graph_requirements = tdbase.nodes.DirectedGraph(top_req.pointer.record, "depends", allow_cyclic=False)
                missing = set(self._parsed_data.iter_all_records("req")) - self.graph_requirements .records_in_graph
                for m in missing:
                    self._add_msg("unreachable requirement: %s" % m.record_name, WarningError.SEVERITY_ERROR)
            else:
                self._add_msg("No top requirement", WarningError.SEVERITY_FATAL)
        finally:
            for msg in self.msgs:
                if msg.severity > self.max_severity:
                    self.max_severity = msg.severity


    def report_txt(self) -> None:
        for msg in self.msgs:
            print (msg.long_msg())
        print ("max severity of msg:", self.max_severity)

        if self.graph_categories:
            print ("Categories:")
            def x(n, lvl):
                print (" " * 2 * lvl + n.record.record_name + " (%d)" % n.level)
                for child in sorted(n.nexts):
                    x(child.graph_info, lvl + 1)
            x(self.graph_categories.first, 1)
            print()

        if self.graph_requirements:
            print ("Requirements:")
            def x(n, lvl):
                print (" " * 2 * lvl + n.record.record_name + " (%d)" % n.level)
                for child in sorted(n.nexts):
                    x(child.graph_info, lvl + 1)
            x(self.graph_requirements.first, 1)
            print()

        print ("* all records:")
        for req in self._parsed_data.iter_all_records("req"):
            print (req.record_type, req.record_name)

    def write_back(self) -> None:
        self._parsed_data.write_back()
