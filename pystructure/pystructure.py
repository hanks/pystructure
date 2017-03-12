#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PYStructure

Usage:
    pystructure.py SRC_PATH [-o FILE | --output=FILE]

Options:
    -o FILE --output=FILE       Save result to output file.
    -h --help                   Show help information.
    --version                   Show version.
"""

import os
from collections import OrderedDict
from ast import parse, literal_eval, Tuple

import six
from docopt import docopt


__VERSION__ = "PYStructure 1.1.0"

class PYSymbol(object):
    GLOBAL_VAR = "v"
    FUNCTION = "f"
    CLASS = "c"
    METHOD = "m"
    ATTRIBUTE = "a"
    PRIVATE_METHOD = "_m"


class PYStructureVisitor(object):
    PREFIX = "visit_"
    LITERAL_VALUE_PREFIX = "visit_literal_"

    def __init__(self):
        self.structure = OrderedDict()

    def visit(self, node_list):
        for node in node_list:
            result = self._get_visit_result(node)

            if result:
                self.structure.update(result)

        return self.structure

    def visit_Assign(self, node):
        result = {
            node.lineno: {
                "type": PYSymbol.GLOBAL_VAR,
                "content": []
            }
        }

        for target in node.targets:
            if isinstance(target, Tuple):
                element = self._get_literal_value_list(target.elts)
                result[node.lineno]["content"].extend(element)
            else:
                element = target.id
                result[node.lineno]["content"].append(element)

        return result

    def visit_ClassDef(self, node):
        result = {
            node.lineno: {
                "type": PYSymbol.CLASS,
                "content": {
                    "name": None,
                    "body": OrderedDict(),
                }
            }
        }

        class_name = node.name
        base_value_list = self._get_literal_value_list(node.bases)
        class_signature = "{}({})".format(class_name, ", ".join(base_value_list))
        result[node.lineno]["content"]["name"] = class_signature

        for item in node.body:
            value = self._get_visit_result(item)
            if value:
                result[node.lineno]["content"]["body"].update(value)

        return result

    def visit_FunctionDef(self, node):
        result = {
            node.lineno: {
                "type": PYSymbol.FUNCTION,
                "content": []
            }
        }

        func_name = node.name
        args_list = [item.id for item in node.args.args] if node.args.args else []
        default_list = self._get_literal_value_list(node.args.defaults)
        kwarg = node.args.kwarg
        vararg = node.args.vararg

        result[node.lineno]["content"] = self._build_func_signature(
            func_name,
            args_list,
            default_list,
            kwarg,
            vararg
        )

        return result

    def visit_literal_Num(self, node):
        return node.n

    def visit_literal_Name(self, node):
        result = node.id

        try:
            result = literal_eval(node.id)
        except ValueError:
            pass

        return result

    def visit_literal_Str(self, node):
        return node.s

    def visit_literal_List(self, node):
        return self._get_literal_value_list(node.elts)

    def visit_literal_Tuple(self, node):
        return self._get_literal_value_list(node.elts)

    def visit_literal_Dict(self, node):
        keys = self._get_literal_value_list(node.keys)
        values = self._get_literal_value_list(node.values)

        return dict(zip(keys, values))

    def _get_visit_result(self, node, prefix=PREFIX):
        node_class_name = node.__class__.__name__
        func_name = "{}{}".format(prefix, node_class_name)
        result = None

        if func_name in self.method_dict:
            func = self.method_dict[func_name]
            result = func(self, node)

        return result

    def _get_literal_value_list(self, node_list):
        literal_value_list = []

        for node in node_list:
            result = self._get_visit_result(node, prefix=self.LITERAL_VALUE_PREFIX)
            literal_value_list.append(result)

        return literal_value_list

    def _build_func_signature(self, func_name, args_list, default_list, kwarg, vararg):
        formatted_args_list = args_list[:]

        if not args_list and not default_list and not kwarg and not vararg:
            # foo()
            pass
        elif default_list is None and kwarg is None and vararg is None:
            # foo(a, b)
            pass
        else:
            # foo(a, b=True)
            args_list_len = len(args_list)
            default_list_len = len(default_list)

            # mapping (a, b) and (4,) to (a, b=4)
            for i in range(default_list_len):
                index = args_list_len - default_list_len + i
                arg = formatted_args_list[index]
                value = default_list[i]
                if isinstance(value, six.string_types):
                    template = '{}="{}"'
                else:
                    template = "{}={}"

                formatted_args_list[index] = template.format(arg, value)

            if vararg:
                formatted_args_list.append("*{}".format(vararg))

            if kwarg:
                formatted_args_list.append("**{}".format(kwarg))

        result = "{}({})".format(func_name, ", ".join(formatted_args_list))

        return result

    @property
    def method_dict(self):
        visitor_func_dict = {}
        d = self.__class__.__dict__

        for key in d:
            if key.startswith(self.PREFIX) and callable(d[key]):
                visitor_func_dict[key] = d[key]

        return visitor_func_dict


class StructureParser(object):
    def __init__(self):
        self.body = None
        self.structure = None

    def accept(self, visitor):
        self.structure = visitor.visit(self.body)

    def load(self, src):
        try:
            root = parse(src)
            self.body = root.body
        except Exception as e:
            exit("parse error, please check, {}".format(str(e)))

    def export(self):
        output = []
        self._format_structure(self.structure, 0, output)

        return "\n".join(output)

    def _format_structure(self, root, level=0, output=None):
        if output is None:
            output = []

        space = " " * level * 2

        for value in root.itervalues():
            content = value["content"]
            type_ = value["type"]

            if "body" in content:
                name = content["name"]
                line = "{}{} {}".format(space, type_, name)
                output.append(line)

                sub_root = content["body"]
                self._format_structure(sub_root, level + 1, output)
            else:
                if isinstance(content, list):
                    # global variable, like a, b = 1, 2
                    content = ", ".join(content)

                line = "{}{} {}".format(space, type_, content)
                output.append(line)


def main():
    args = docopt(__doc__, version=__VERSION__)
    src_path = args["SRC_PATH"]
    output_path = args["--output"]

    if not os.path.exists(src_path):
        exit("src path {} is not existed, please check it".format(src_path))

    with open(src_path) as f:
        src = f.read()
        parser = StructureParser()
        parser.load(src)
        visitor = PYStructureVisitor()
        parser.accept(visitor)
        result = parser.export()

        if output_path:
            with open(output_path, "w+") as o:
                o.write(result)
        else:
            print(result)


if __name__ == "__main__":
    main()
