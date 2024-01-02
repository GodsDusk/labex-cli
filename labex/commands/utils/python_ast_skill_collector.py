# -*- coding:utf-8 _*-
__author__ = 'xujunjie'
__date__ = '2024/1/2 09:40'

import ast


class PythonSkillCollector(ast.NodeVisitor):
    def __init__(self, standard_libraries, built_in_functions):
        self.skills = set()
        self.standard_libraries = standard_libraries
        self.built_in_functions = built_in_functions

    def check_variable_types(self, node):
        if isinstance(node, (ast.List, ast.Tuple, ast.Dict, ast.Set)):
            self.skills.add("python/variables_data_types")

    def visit_Name(self, node):
        if node.id in ["int", "float", "complex", "str", "bool"]:
            self.skills.add("python/variables_data_types")

            if node.id in ["int", "float", "complex"]:
                self.skills.add("python/numeric_types")

            if node.id == "str":
                self.skills.add("python/strings")

            if node.id in ["True", "False"]:
                self.skills.add("python/booleans")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ["int", "float", "str"]:
                self.skills.add("python/type_conversion")
            if node.func.id in ['list', 'tuple', 'set', 'dict']:
                self.skills.add("python/data_collections")
            if node.func.id == "open":
                self.skills.add("python/file_opening_closing")
            if node.func.id in ['iter', 'next']:
                self.skills.add("python/iterators")
            if node.func.id in self.built_in_functions:
                self.skills.add("python/build_in_functions")

        self.generic_visit(node)

    def visit_Comment(self, node):
        self.skills.add("python/comments")

    def visit_List(self, node):
        # Check for non-empty lists
        if node.elts:
            self.skills.add("python/lists")
        self.generic_visit(node)

    def visit_Tuple(self, node):
        # Check for tuples, avoiding confusion with function calls
        if len(node.elts) > 1:
            self.skills.add("python/tuples")
        self.generic_visit(node)

    def visit_Dict(self, node):
        # Check for dictionaries
        if node.keys:
            self.skills.add("python/dictionaries")
        self.generic_visit(node)

    def visit_Set(self, node):
        # Check for sets, distinguishing from dictionaries
        if node.elts:
            self.skills.add("python/sets")
        self.generic_visit(node)

    def visit_ClassDef(self, node):

        self.skills.add("python/classes_objects")
        self.skills.add("python/inheritance")

        # Check for classes with methods using self and dunder methods
        has_self = any("self" in arg.arg for method in node.body if isinstance(
            method, ast.FunctionDef) for arg in method.args.args)
        has_dunder_method = any(method.name.startswith("__") and method.name.endswith(
            "__") for method in node.body if isinstance(method, ast.FunctionDef))

        if has_self:
            self.skills.add("python/encapsulation")
            if has_dunder_method:
                self.skills.add("python/polymorphism")

        has_init = any(isinstance(method, ast.FunctionDef)
                       and method.name == '__init__' for method in node.body)
        if has_init:
            self.skills.add("python/constructor")

        if any(m.name in ["__enter__", "__exit__"] for m in node.body if isinstance(m, ast.FunctionDef)):
            self.skills.add("python/context_managers")

        self.generic_visit(node)

    def visit_If(self, node):
        self.skills.add("python/conditional_statements")
        if (isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Name)
                and node.test.left.id == '__name__' and isinstance(node.test.comparators[0], ast.Str)
                and node.test.comparators[0].s == '__main__'):
            self.skills.add("python/creating_modules")

        self.generic_visit(node)

    def visit_For(self, node):
        if isinstance(node.target, ast.Name):
            self.skills.add("python/for_loops")
        self.generic_visit(node)

    def visit_While(self, node):
        self.skills.add("python/while_loops")
        self.generic_visit(node)

    def visit_Break(self, node):
        self.skills.add("python/break_continue")
        self.generic_visit(node)

    def visit_Continue(self, node):
        self.skills.add("python/break_continue")
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.skills.add("python/list_comprehensions")
        self.generic_visit(node)

    def check_collection_types(self, node):
        if isinstance(node, (ast.List, ast.Tuple, ast.Set, ast.Dict)):
            self.skills.add("python/data_collections")

    def visit_FunctionDef(self, node):

        self.skills.add("python/function_definition")

        has_return = any(isinstance(child, ast.Return)
                         for child in ast.walk(node))
        if has_return:
            self.skills.add("python/arguments_return")

        has_default_args = any(arg for arg in node.args.defaults)
        if has_default_args:
            self.skills.add("python/default_arguments")

        if node.args.vararg or node.args.kwarg:
            self.skills.add("python/keyword_arguments")

        # Check for recursion
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id == node.name:
                    self.skills.add("python/recursion")
                    break

        if any(isinstance(decorator, ast.Name) and decorator.id in ['classmethod', 'staticmethod'] for decorator in
               node.decorator_list):
            self.skills.add("python/class_static_methods")

        if node.decorator_list:
            self.skills.add("python/decorators")
        self.generic_visit(node)

    def visit_Lambda(self, node):
        self.skills.add("python/lambda_functions")
        self.generic_visit(node)

    def visit_Global(self, node):
        self.skills.add("python/scope")
        self.generic_visit(node)

    def visit_Nonlocal(self, node):
        self.skills.add("python/scope")
        self.generic_visit(node)

    def visit_Try(self, node):
        self.skills.add("python/catching_exceptions")
        self.generic_visit(node)

    def visit_Raise(self, node):
        self.skills.add("python/raising_exceptions")
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.skills.add("python/custom_exceptions")
        self.generic_visit(node)

    def visit_With(self, node):
        self.skills.add("python/with_statement")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr in ["read", "write"]:
            self.skills.add("python/file_reading_writing")
        self.generic_visit(node)

    def visit_Yield(self, node):
        self.skills.add("python/generators")
        self.generic_visit(node)

    def visit_Import(self, node):
        # Check for specific library imports
        self.skills.add("python/importing_modules")
        for alias in node.names:
            self.check_import(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Check for specific module imports from a library
        self.skills.add("python/using_packages")
        self.check_import(node.module)
        self.generic_visit(node)

    def check_import(self, name):
        library_skill_mapping = {
            "re": ["python/regular_expressions"],
            "threading": ["python/threading_multiprocessing"],
            "multiprocessing": ["python/threading_multiprocessing"],
            "math": ["python/math_random"],
            "random": ["python/math_random"],
            "datetime": ["python/date_time"],
            "json": ["python/data_serialization"],
            "pickle": ["python/data_serialization"],
            "marshal": ["python/data_serialization"],
            "os": ["python/os_system"],
            "sys": ["python/os_system"],
            "socket": ["python/socket_programming"],
            "requests": ["python/http_requests"],
            "http.client": ["python/http_requests"],
            "numpy": ["python/numerical_computing"],
            "scipy": ["python/numerical_computing"],
            "pandas": ["python/numerical_computing", "python/data_analysis"],
            "matplotlib": ["python/data_visualization"],
            "seaborn": ["python/data_visualization"],
            "sklearn": ["python/machine_learning"],
            "tensorflow": ["python/machine_learning"],
            "keras": ["python/machine_learning"],
            "pytorch": ["python/machine_learning"]
        }
        if name in library_skill_mapping:
            self.skills.update(library_skill_mapping[name])
        if name in self.standard_libraries:
            self.skills.add("python/standard_libraries")
