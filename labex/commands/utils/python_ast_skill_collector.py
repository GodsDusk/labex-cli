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


class SklearnSkillCollector(ast.NodeVisitor):

    def __init__(self, clean_skills):
        self.clean_skills = clean_skills
        self.skills = set()

    def visit_Import(self, node):
        for alias in node.names:
            skill_name = self.extract_skill_name(alias.name)
            if skill_name:
                self.skills.add(skill_name)

    def visit_ImportFrom(self, node):
        if node.module and 'sklearn' in node.module:
            for alias in node.names:
                submodule = alias.name if node.module == 'sklearn' else node.module.split('sklearn.')[1]
                skill_name = self.extract_skill_name(submodule)
                if skill_name:
                    self.skills.add(skill_name)

    def extract_skill_name(self, module_name):
        skill = module_name.split('.')[0]
        if skill in self.clean_skills:
            return f'sklearn/{skill}'
        return None


class TkinterSkillCollector(ast.NodeVisitor):
    def __init__(self, build_in_functions):
        self.build_in_functions = build_in_functions
        self.tkinter_aliases = {'tkinter'}
        self.skills = set()

    def visit_Import(self, node):
        for alias in node.names:
            if 'tkinter' in alias.name:
                if alias.asname:
                    self.tkinter_aliases.add(alias.asname)
                else:
                    self.tkinter_aliases.add(alias.name)

    def visit_ImportFrom(self, node):
        if node.module and 'tkinter' in node.module:
            self.tkinter_aliases.add(node.module.split('.')[0])
            for alias in node.names:
                if alias.name in self.build_in_functions:
                    self.skills.add(f"tkinter/{alias.name.lower()}")

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id in self.tkinter_aliases and node.func.attr in self.build_in_functions:
                self.skills.add(f"tkinter/{node.func.attr.lower()}")


class PygameSkillCollector(ast.NodeVisitor):
    def __init__(self, build_in_functions):
        self.build_in_functions = build_in_functions
        self.skills = set()

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'pygame':
            self.check_and_add_skill(node.attr)
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        if isinstance(func, ast.Attribute):
            if isinstance(func.value, ast.Name) and func.value.id == 'pygame':
                self.check_and_add_skill(func.attr)
        self.generic_visit(node)

    def check_and_add_skill(self, attribute_name):
        if attribute_name in self.build_in_functions:
            self.skills.add(f"pygame/{attribute_name}")


class DjangoSkillCollector(ast.NodeVisitor):
    def __init__(self):
        self.skills = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.check_django_skill(alias.name)

    def visit_ImportFrom(self, node):
        if node.module and 'django' in node.module:
            self.check_django_skill(node.module)

    def check_django_skill(self, module_name):
        django_skill_map = {
            "django.apps": "django/applications",
            "django.views.generic": "django/built_in_views",
            "django.views.View": "django/built_in_views",
            "django.views.TemplateView": "django/built_in_views",
            "django.middleware.clickjacking": "django/clickjacking_protection",
            "django.contrib": "django/contrib_packages",
            "django.db": "django/databases",
            "django.contrib.admin": "django/django_admin",
            "django.core.exceptions": "django/django_exceptions",
            "django.core.files": "django/file_handling",
            "django.forms": "django/forms",
            "django.utils.log": "django/logging",
            "django.middleware": "django/middleware",
            "django.db.migrations": "django/migration_operations",
            "django.db.models": "django/models",
            "django.core.paginator": "django/paginator",
            "django.http": "django/request_and_response",
            "django.conf.settings": "django/settings",
            "django.dispatch": "django/signals",
            "django.template": "django/templates",
            "django.template.response": "django/simpletemplateresponse",
            "django.utils.encoding": "django/unicode_data",
            "django.urls": "django/django_urls",
            "django.core.validators": "django/validators"
        }

        for key, value in django_skill_map.items():
            if key in module_name:
                self.skills.add(value)


class PandasSkillCollector(ast.NodeVisitor):
    def __init__(self):
        self.skills = set()
        self.pandas_objects = set()  # Track names of pandas DataFrames/Series
        self.pandas_aliases = {'pandas'}

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'pandas':
                self.pandas_aliases.add(alias.asname if alias.asname else alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module == 'pandas':
            for alias in node.names:
                self.pandas_aliases.add(alias.asname if alias.asname else alias.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        pandas_creation_methods = ['read_csv', 'read_excel', 'read_sql', 'DataFrame', 'Series', 'read_table',
                                   'read_json', 'read_html', 'read_clipboard', 'read_pickle', 'read_msgpack',
                                   'read_hdf', 'read_feather', 'read_parquet', 'read_orc', 'read_sas', 'read_spss',
                                   'read_stata', 'read_sas7bdat', 'read_sas7bcat']

        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            if node.value.func.attr in pandas_creation_methods:
                if isinstance(node.targets[0], ast.Name):
                    self.pandas_objects.add(node.targets[0].id)

        # Check for Adding New Columns to a pandas DataFrame/Series
        if isinstance(node.targets[0], ast.Subscript):
            if isinstance(node.targets[0].value, ast.Name) and node.targets[0].value.id in self.pandas_objects:
                if isinstance(node.targets[0].slice, ast.Index) and isinstance(node.targets[0].slice.value, ast.Str):
                    self.skills.add("pandas/add_new_columns")

        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Ensure the operation is on a pandas DataFrame/Series
        if isinstance(node.value, ast.Name) and node.value.id in self.pandas_objects:
            if isinstance(node.slice.value, ast.Str):
                self.skills.add("pandas/select_columns")
            if any(isinstance(op, (ast.Eq, ast.NotEq, ast.Lt, ast.Gt, ast.LtE, ast.GtE, ast.In, ast.NotIn)) for op in
                   ast.walk(node)):
                self.skills.add("pandas/conditional_selection")
        self.generic_visit(node)

    def visit_Call(self, node):

        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                obj_id = node.func.value.id
                method_name = node.func.attr

                if obj_id in self.pandas_objects or obj_id in self.pandas_aliases:
                    self.check_pandas_method(method_name, node)
        self.generic_visit(node)

    def check_pandas_method(self, method_name, node):
        if method_name == 'read_csv':
            self.skills.add("pandas/read_csv")
        elif method_name == 'read_excel':
            self.skills.add("pandas/read_excel")
        elif method_name == 'read_sql':
            self.skills.add("pandas/read_sql")
        elif method_name == 'write_csv':
            self.skills.add("pandas/write_csv")
        elif method_name == 'write_sql':
            self.skills.add("pandas/write_sql")
        elif method_name == 'write_excel':
            self.skills.add("pandas/write_excel")
        elif method_name in ['loc', 'iloc']:
            if any(isinstance(arg, ast.Slice) for arg in ast.walk(node)):
                self.skills.add("pandas/slicing")
            else:
                self.skills.add("pandas/select_rows")
        elif method_name == 'drop':
            self.skills.add("pandas/drop_columns_rows")
        elif method_name == 'astype':
            self.skills.add("pandas/change_data_types")
        elif method_name in ['sort_values', 'sort_index']:
            self.skills.add("pandas/sort_data")
        elif method_name in ['fillna', 'dropna']:
            self.skills.add("pandas/handle_missing_values")
        elif method_name == 'drop_duplicates':
            self.skills.add("pandas/remove_duplicates")
        elif method_name in ['map', 'apply']:
            self.skills.add("pandas/data_mapping")
        elif method_name in ['mean', 'median', 'sum', 'count']:
            self.skills.add("pandas/basic_statistics")
        elif method_name == 'groupby':
            self.skills.add("pandas/groupby_operations")
        elif method_name in ['agg', 'aggregate']:
            self.skills.add("pandas/data_aggregation")
        elif method_name == 'pivot_table':
            self.skills.add("pandas/pivot_tables")
        # Check for MultiIndex Indexing
        elif method_name == 'MultiIndex':
            self.skills.append("pandas/multiindex_indexing")
        # Checks for merging data
        elif method_name in ['merge', 'join']:
            self.skills.append("pandas/merge_data")
        # Checks for reshaping data
        elif method_name in ['melt', 'pivot', 'stack', 'unstack']:
            self.skills.append("pandas/reshape_data")

        # Data Normalization requires a combination of checks
        elif method_name == 'apply':
            for arg in ast.walk(node):
                if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute):
                    if arg.func.attr in ['min', 'max', 'mean']:
                        self.skills.add("pandas/data_normalization")
                        break
        # Checks for plotting methods
        elif method_name == 'plot':
            # Check for kind argument in .plot() calls
            for keyword in node.keywords:
                if keyword.arg == 'kind':
                    if isinstance(keyword.value, ast.Str):
                        plot_type = keyword.value.s
                        if plot_type == 'bar':
                            self.skills.add("pandas/bar_plots")
                        elif plot_type == 'hist':
                            self.skills.add("pandas/histograms")
                        elif plot_type == 'scatter':
                            self.skills.add("pandas/scatter_plots")
                        elif plot_type == 'line':
                            self.skills.add("pandas/line_plots")
        elif method_name == 'bar':
            self.skills.add("pandas/bar_plots")
        elif method_name == 'hist':
            self.skills.add("pandas/histograms")
        elif method_name == 'scatter':
            self.skills.add("pandas/scatter_plots")
        elif method_name == 'line':
            self.skills.add("pandas/line_plots")
        # Checks for time series analysis methods
        elif method_name in ['resample', 'asfreq', 'rolling']:
            self.skills.add("pandas/time_series_analysis")

class MatplotlibSkillCollector(ast.NodeVisitor):
    def __init__(self):
        self.skills = set()

    def visit_Import(self, node):
        # Check for 'import matplotlib'
        for name in node.names:
            if name.name == 'matplotlib':
                self.skills.add('matplotlib/importing_matplotlib')
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Check for 'from matplotlib import'
        if node.module and 'matplotlib' in node.module:
            self.skills.add('matplotlib/importing_matplotlib')
            # Further checks for submodules like 'figure', 'pyplot', 'axes'
            if any(submod in node.module for submod in ['figure', 'pyplot', 'axes']):
                self.skills.add('matplotlib/figures_axes')
            if 'widgets' in node.module or 'backends' in node.module or 'animation' in node.module or 'rc' in node.module:
                self.skills.add("matplotlib/interactive_backends")
                self.skills.add("matplotlib/custom_backends")
                self.skills.add("matplotlib/animation_creation")
                self.skills.add("matplotlib/matplotlib_config")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            # Checking for different plotting methods
            if method_name == 'plot':
                self.skills.add('matplotlib/line_plots')
            elif method_name == 'scatter':
                self.skills.add('matplotlib/scatter_plots')
            elif method_name == 'bar':
                self.skills.add('matplotlib/bar_charts')
            elif method_name == 'hist':
                self.skills.add('matplotlib/histograms')
            elif method_name == 'boxplot':
                self.skills.add('matplotlib/box_plots')
            elif method_name == 'imshow' or method_name == 'heatmap':
                self.skills.add('matplotlib/heatmaps')
            elif method_name == 'errorbar':
                self.skills.add('matplotlib/error_bars')
            elif method_name == 'stackplot':
                self.skills.add('matplotlib/stacked_plots')
            elif method_name == 'fill_between':
                self.skills.add('matplotlib/fill_between')
            # Advanced plotting
            elif method_name == 'subplot':
                self.skills.add('matplotlib/subplots')
            elif method_name in ['twinx', 'twiny']:
                self.skills.add('matplotlib/secondary_axis')
            elif method_name == 'set_yscale' or method_name == 'set_xscale':
                # Check for log scale
                for arg in node.args:
                    if isinstance(arg, ast.Str) and arg.s == 'log':
                        self.skills.add('matplotlib/log_scale')
                        break
            elif method_name == 'polar':
                self.skills.add('matplotlib/polar_charts')
            elif method_name in ['plot_surface', 'plot_wireframe']:
                self.skills.add('matplotlib/3d_plots')
           # Plot Customization
            elif method_name == 'setp':
                self.skills.add('matplotlib/line_styles_colors')
            elif any(attr in node.func.attr for attr in ['title', 'xlabel', 'ylabel']):
                self.skills.add('matplotlib/titles_labels')
            elif method_name == 'legend':
                self.skills.append('matplotlib/legend_config')
            elif any(attr in node.func.attr for attr in ['xticks', 'yticks']):
                self.skills.add('matplotlib/axis_ticks')
            elif method_name == 'grid':
                self.skills.add('matplotlib/grid_config')
            elif method_name == 'annotate':
                self.skills.add('matplotlib/text_annotations')
            elif method_name == 'table':
                self.skills.add('matplotlib/adding_tables')
            # Specialized Plots
            elif method_name == 'pie':
                self.skills.add('matplotlib/pie_charts')
            elif method_name == 'bubble':
                self.skills.add('matplotlib/bubble_charts')
            elif method_name == 'violinplot':
                self.skills.add('matplotlib/violin_plots')
            elif method_name in ['contour', 'contourf']:
                self.skills.add('matplotlib/contour_plots')
            elif method_name == 'quiver':
                self.skills.add('matplotlib/quiver_plots')
            elif method_name == 'streamplot':
                self.skills.add('matplotlib/stream_plots')
            elif method_name in ['connect', 'slider']:
                self.skills.add("matplotlib/event_handling")
                self.skills.add("matplotlib/widgets_sliders")
        self.generic_visit(node)
