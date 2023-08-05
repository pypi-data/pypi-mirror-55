# Copyright (c) 2019 by Enrique Pérez Arnaud <enrique@cazalla.net>
#
# This file is part of the syntreenet project.
# https://syntree.net
#
# The syntreenet project is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The syntreenet project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with any part of the terms project.
# If not, see <http://www.gnu.org/licenses/>.

from .grammar import Segment, Matching
from .logging import logger


class ec_handlers:
    '''
    Extra conditions handlers.
    These return False, True, or a new matching dict
    '''

    @staticmethod
    def logic(text, matching, kb, extra=None):
        tree = kb.parse(text)
        ec = kb.from_parse_tree(tree)
        new_ec = ec.substitute(matching, kb)
        return kb.ask(new_ec)

    @staticmethod
    def unknown(text, matching, kb, extra=None):
        tree = kb.parse(text)
        ec = kb.from_parse_tree(tree)
        new_ec = ec.substitute(matching, kb)
        return not kb.ask(new_ec)

    @staticmethod
    def python(text, matching, kb, extra=None):
        exec_globals = extra or {}
        pre_exec_locals = matching.to_dict()
        exec_locals = {}
        for k,v in pre_exec_locals.items():
            try:
                exec_locals[k] = float(v)
            except ValueError:
                exec_locals[k] = v
        try:
            return eval(text, exec_globals, exec_locals)
        except SyntaxError:
            try:
                exec(text, exec_globals, exec_locals)
            except Exception:
                return False
            if 'test' in exec_locals and exec_locals['test'] is False:
                return False
            new_mapping = tuple((Segment(k, '__var__'), Segment(str(v)))
                    for k, v in exec_locals.items() if k not in pre_exec_locals)
            return [Matching(new_mapping)]

    @staticmethod
    def rm(text, matching, kb, extra=None):
        logger.info(f'removing fact "{text}"')
        tree = kb.parse(text)
        fact = kb.from_parse_tree(tree)
        new_fact = fact.substitute(matching, kb)
        kb.fset.rm_fact(new_fact)

    @staticmethod
    def exec(text, matching, kb, extra=None):
        exec_globals = extra or {}
        pre_exec_locals = matching.to_dict()
        exec_locals = {}
        for k,v in pre_exec_locals.items():
            try:
                exec_locals[k] = float(v)
            except ValueError:
                exec_locals[k] = v
        try:
            exec(text, exec_globals, exec_locals)
        except Exception:
            return False  # TODO do not add consecuences, add a failure note to
                          # the kb
