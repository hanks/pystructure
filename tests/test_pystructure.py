#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pystructure.pystructure import PYStructureVisitor


class TestPYStructureVisitor(object):
    def setup_class(self):
        self.visitor = PYStructureVisitor()

    def test_build_func_structure(self):
        func_name = "foo"
        args_list = []
        default_list = []
        kwarg = None
        vararg = None

        result = self.visitor._build_func_signature(
            func_name,
            args_list,
            default_list,
            kwarg,
            vararg
        )
        expected = "foo()"

        assert result == expected

        func_name = "foo"
        args_list = ["a", "b"]
        default_list = []
        kwarg = None
        vararg = None

        result = self.visitor._build_func_signature(
            func_name,
            args_list,
            default_list,
            kwarg,
            vararg
        )
        expected = "foo(a, b)"

        assert result == expected

        func_name = "foo"
        args_list = ["a", "b"]
        default_list = [3]
        kwarg = None
        vararg = None

        result = self.visitor._build_func_signature(
            func_name,
            args_list,
            default_list,
            kwarg,
            vararg
        )
        expected = "foo(a, b=3)"

        assert result == expected

        func_name = "foo"
        args_list = ["a", "b"]
        default_list = [3]
        kwarg = "kw"
        vararg = None

        result = self.visitor._build_func_signature(
            func_name,
            args_list,
            default_list,
            kwarg,
            vararg
        )
        expected = "foo(a, b=3, **kw)"

        assert result == expected

        func_name = "foo"
        args_list = ["a", "b"]
        default_list = [3, True]
        kwarg = "kw"
        vararg = "v"

        result = self.visitor._build_func_signature(
            func_name,
            args_list,
            default_list,
            kwarg,
            vararg
        )
        expected = "foo(a=3, b=True, *v, **kw)"

        assert result == expected

        func_name = "foo"
        args_list = ["a", "b", "c"]
        default_list = [3, True]
        kwarg = None
        vararg = "v"

        result = self.visitor._build_func_signature(
            func_name,
            args_list,
            default_list,
            kwarg,
            vararg
        )
        expected = "foo(a, b=3, c=True, *v)"

        assert result == expected

        func_name = "foo"
        args_list = ["a", "b", "c"]
        default_list = [3, "foo"]
        kwarg = None
        vararg = "v"

        result = self.visitor._build_func_signature(
            func_name,
            args_list,
            default_list,
            kwarg,
            vararg
        )
        expected = 'foo(a, b=3, c="foo", *v)'

        assert result == expected
