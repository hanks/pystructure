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
    """Symbol definitions for source code
    """
    GLOBAL_VAR = "v"
    FUNCTION = "f"
    CLASS = "c"
    METHOD = "m"
    ATTRIBUTE = "a"
    PRIVATE_METHOD = "_m"


class PYStructureVisitor(object):
    """Use visitor pattern here, and define visitor method to each
    node in source code
    """
    PREFIX = "visit_"
    LITERAL_VALUE_PREFIX = "visit_literal_"

    def __init__(self):
        self.structure = OrderedDict()

    def visit(self, node_list):
        """Entry visitor method for all nodes, a delegate to call other concrete visitor implementation

        Args:
            node_list: list, ast node object list

        Returns:
            OrderedDict, result from visitor methods
        """
        for node in node_list:
            result = self._get_visit_result(node)

            if result:
                self.structure.update(result)

        return self.structure

    def visit_Assign(self, node):
        """Visitor method for the Assign node

        Args:
            node: object, ast Assign node

        Returns:
            dict, result from parsing the Assign node
        """
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
        """Visitor method for the ClassDef node

        Args:
            node: object, ast ClassDef node

        Returns:
            dict, result from parsing the ClassDef node
        """
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
        """Visitor method for the FunctionDef node

        Args:
            node: object, ast FunctionDef node

        Returns:
            dict, result from parsing the FunctionDef node
        """
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
        """Visitor method for the literal Num node

        Args:
            node: object, ast literal Num node

        Returns:
            dict, result from parsing the literal Num node
        """
        return node.n

    def visit_literal_Name(self, node):
        """Visitor method for the literal Name node

        Args:
            node: object, ast literal Name node

        Returns:
            dict, result from parsing the literal Name node
        """
        result = node.id

        try:
            result = literal_eval(node.id)
        except ValueError:
            pass

        return result

    def visit_literal_Str(self, node):
        """Visitor method for the literal Str node

        Args:
            node: object, ast literal Str node

        Returns:
            dict, result from parsing the literal Str node
        """
        return node.s

    def visit_literal_List(self, node):
        """Visitor method for the literal List node

        Args:
            node: object, ast literal List node

        Returns:
            dict, result from parsing the literal List node
        """
        return self._get_literal_value_list(node.elts)

    def visit_literal_Tuple(self, node):
        """Visitor method for the literal Tuple node

        Args:
            node: object, ast literal Tuple node

        Returns:
            dict, result from parsing the literal Tuple node
        """
        return self._get_literal_value_list(node.elts)

    def visit_literal_Dict(self, node):
        """Visitor method for the literal Dict node

        Args:
            node: object, ast literal Dict node

        Returns:
            dict, result from parsing the literal Dict node
        """
        keys = self._get_literal_value_list(node.keys)
        values = self._get_literal_value_list(node.values)

        return dict(zip(keys, values))

    def _get_visit_result(self, node, prefix=PREFIX):
        """Delegation to get result from parsing node, to call according visitor method

        Args:
            node: object, ast node
            prefix: str, prefix to generate visitor method

        Returns:
            dict, result from each visitor method
        """
        node_class_name = node.__class__.__name__
        func_name = "{}{}".format(prefix, node_class_name)
        result = None

        if func_name in self.method_dict:
            func = self.method_dict[func_name]
            result = func(self, node)

        return result

    def _get_literal_value_list(self, node_list):
        """Delegation to get result from parsing node list, to call according visitor method

        Args:
            node_list: list, ast node list

        Returns:
            list, result list from each visitor method
        """
        literal_value_list = []

        for node in node_list:
            result = self._get_visit_result(node, prefix=self.LITERAL_VALUE_PREFIX)
            literal_value_list.append(result)

        return literal_value_list

    def _build_func_signature(self, func_name, args_list, default_list, kwarg, vararg):
        """Func signature builder for FunctionDef node

        Args:
            func_name: str, function name
            args_list: list, function args list
            default_list: list, function default parameter list
            kwarg: dict, function kwarg, a=1, b=1
            vararg: list, function vararg, a, b

        Returns:

        """
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
        """Dict to store method name and method func key-value pair, like a cache

        Returns:
            func object, visitor function object
        """
        visitor_func_dict = {}
        d = self.__class__.__dict__

        for key in d:
            if key.startswith(self.PREFIX) and callable(d[key]):
                visitor_func_dict[key] = d[key]

        return visitor_func_dict


class StructureParser(object):
    """Parser for the source code
    """
    def __init__(self):
        self.body = None
        self.structure = None

    def accept(self, visitor):
        """Set up visitor for parser

        Args:
            visitor: object, visitor object

        Returns:
            None

        Side Effects:
            Setup parse result for self.structure
        """
        self.structure = visitor.visit(self.body)

    def load(self, src):
        """Prepare source code for parsing

        Args:
            src: str, source code from file

        Returns:
            None

        Side Effects:
            Setup load result for self.body
        """
        try:
            root = parse(src)
            self.body = root.body
        except Exception as e:
            exit("parse error, please check, {}".format(str(e)))

    def export(self):
        """Export structure information to a formatted output

        Returns:
            str, formatted structure str
        """
        output = []
        self._format_structure(self.structure, 0, output)

        return "\n".join(output)

    def _format_structure(self, root, level=0, output=None):
        """Format structure to a desired version

        Args:
            root: dict, structure object
            level: int, using to control space using in each hierarchy level
            output: list, result str list

        Returns:
            None

        Side Effects:
            set final result to output object
        """
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
