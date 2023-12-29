import ast
import re


class ParseSkills:
    def __init__(self) -> None:
        pass

    def __parse_python_skill(self, content):
        skills = set()
        # Standard libraries
        standard_libraries = [
            "os",
            "sys",
            "math",
            "datetime",
            "json",
            "http",
            "urllib",
            "re",
            "subprocess",
            "multiprocessing",
            "threading",
            "collections",
            "itertools",
            "functools",
            "random",
            "pickle",
            "socket",
            "struct",
            "hashlib",
            "tempfile",
            "glob",
            "shutil",
            "logging",
            "argparse",
            "unittest",
            "pdb",
            "profile",
            "time",
            "csv",
            "xml",
            "html",
            "ftplib",
            "http",
            "io",
            "zipfile",
            "sqlite3",
            "xmlrpc",
            "configparser",
            "contextlib",
            "queue",
            "weakref",
            "base64",
            "binascii",
            "errno",
            "gettext",
            "locale",
            "string",
            "textwrap",
            "unicodedata",
            "stringprep",
            "calendar",
            "codecs",
            "dis",
            "inspect",
            "ast",
            "symtable",
            "token",
            "keyword",
            "tokenize",
            "tabnanny",
            "pyclbr",
            "pydoc",
            "doctest",
            "trace",
            "tracemalloc",
            "importlib",
            "pkgutil",
            "modulefinder",
            "runpy",
            "parser",
            "platform",
            "errno",
            "ctypes",
            "select",
            "asyncio",
            "ssl",
            "email",
            "json",
            "mailcap",
            "mailbox",
            "mimetypes",
            "smtplib",
            "uuid",
            "cgi",
            "cgitb",
            "wsgiref",
            "xml",
            "xmlrpc",
            "webbrowser",
            "cmd",
            "shlex",
        ]
        # Built-in functions
        built_in_functions = [
            "abs",
            "all",
            "any",
            "ascii",
            "bin",
            "bool",
            "bytearray",
            "bytes",
            "callable",
            "chr",
            "classmethod",
            "compile",
            "complex",
            "delattr",
            "dict",
            "dir",
            "divmod",
            "enumerate",
            "eval",
            "exec",
            "filter",
            "float",
            "format",
            "frozenset",
            "getattr",
            "globals",
            "hasattr",
            "hash",
            "help",
            "hex",
            "id",
            "input",
            "int",
            "isinstance",
            "issubclass",
            "iter",
            "len",
            "list",
            "locals",
            "map",
            "max",
            "memoryview",
            "min",
            "next",
            "object",
            "oct",
            "open",
            "ord",
            "pow",
            "print",
            "property",
            "range",
            "repr",
            "reversed",
            "round",
            "set",
            "setattr",
            "slice",
            "sorted",
            "staticmethod",
            "str",
            "sum",
            "super",
            "tuple",
            "type",
            "vars",
            "zip",
            "__import__",
        ]

        class SkillCollector(ast.NodeVisitor):
            def check_variable_types(self, node):
                if isinstance(node, (ast.List, ast.Tuple, ast.Dict, ast.Set)):
                    skills.add("python/variables_data_types")

            def visit_Name(self, node):
                if node.id in ["int", "float", "complex", "str", "bool"]:
                    skills.add("python/variables_data_types")

                    if node.id in ["int", "float", "complex"]:
                        skills.add("python/numeric_types")

                    if node.id == "str":
                        skills.add("python/strings")

                    if node.id in ["True", "False"]:
                        skills.add("python/booleans")
                self.generic_visit(node)

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ["int", "float", "str"]:
                        skills.add("python/type_conversion")
                    if node.func.id in ['list', 'tuple', 'set', 'dict']:
                        skills.add("python/data_collections")
                    if node.func.id == "open":
                        skills.add("python/file_opening_closing")
                    if node.func.id in ['iter', 'next']:
                        skills.add("python/iterators")
                    if node.func.id in built_in_functions:
                        skills.add("python/build_in_functions")

                self.generic_visit(node)

            def visit_Comment(self, node):
                skills.add("python/comments")

            def visit_List(self, node):
                # Check for non-empty lists
                if node.elts:
                    skills.add("python/lists")
                self.generic_visit(node)

            def visit_Tuple(self, node):
                # Check for tuples, avoiding confusion with function calls
                if len(node.elts) > 1:
                    skills.add("python/tuples")
                self.generic_visit(node)

            def visit_Dict(self, node):
                # Check for dictionaries
                if node.keys:
                    skills.add("python/dictionaries")
                self.generic_visit(node)

            def visit_Set(self, node):
                # Check for sets, distinguishing from dictionaries
                if node.elts:
                    skills.add("python/sets")
                self.generic_visit(node)

            def visit_ClassDef(self, node):

                skills.add("python/classes_objects")
                skills.add("python/inheritance")

                # Check for classes with methods using self and dunder methods
                has_self = any("self" in arg.arg for method in node.body if isinstance(
                    method, ast.FunctionDef) for arg in method.args.args)
                has_dunder_method = any(method.name.startswith("__") and method.name.endswith(
                    "__") for method in node.body if isinstance(method, ast.FunctionDef))

                if has_self:
                    skills.add("python/encapsulation")
                    if has_dunder_method:
                        skills.add("python/polymorphism")

                has_init = any(isinstance(method, ast.FunctionDef)
                               and method.name == '__init__' for method in node.body)
                if has_init:
                    skills.add("python/constructor")

                if any(m.name in ["__enter__", "__exit__"] for m in node.body if isinstance(m, ast.FunctionDef)):
                    skills.add("python/context_managers")

                self.generic_visit(node)

            def visit_If(self, node):
                skills.add("python/conditional_statements")
                if isinstance(node.test, ast.Compare) and any(isinstance(el, ast.Name) for el in node.test.left.elts if el.id == '__name__'):
                    skills.add("python/creating_modules")

                self.generic_visit(node)

            def visit_For(self, node):
                if isinstance(node.target, ast.Name):
                    skills.add("python/for_loops")
                self.generic_visit(node)

            def visit_While(self, node):
                skills.add("python/while_loops")
                self.generic_visit(node)

            def visit_Break(self, node):
                skills.add("python/break_continue")
                self.generic_visit(node)

            def visit_Continue(self, node):
                skills.add("python/break_continue")
                self.generic_visit(node)

            def visit_ListComp(self, node):
                skills.add("python/list_comprehensions")
                self.generic_visit(node)

            def check_collection_types(self, node):
                if isinstance(node, (ast.List, ast.Tuple, ast.Set, ast.Dict)):
                    skills.add("python/data_collections")

            def visit_FunctionDef(self, node):

                skills.add("python/function_definition")

                has_return = any(isinstance(child, ast.Return)
                                 for child in ast.walk(node))
                if has_return:
                    skills.add("python/arguments_return")

                has_default_args = any(arg for arg in node.args.defaults)
                if has_default_args:
                    skills.add("python/default_arguments")

                if node.args.vararg or node.args.kwarg:
                    skills.add("python/keyword_arguments")

                # Check for recursion
                if any(child.name == node.name for child in ast.walk(node) if isinstance(child, ast.Call)):
                    skills.add("python/recursion")

                if any(isinstance(decorator, ast.Name) and decorator.id in ['classmethod', 'staticmethod'] for decorator in node.decorator_list):
                    skills.add("python/class_static_methods")

                if node.decorator_list:
                    skills.add("python/decorators")
                self.generic_visit(node)

            def visit_Lambda(self, node):
                skills.add("python/lambda_functions")
                self.generic_visit(node)

            def visit_Global(self, node):
                skills.add("python/scope")
                self.generic_visit(node)

            def visit_Nonlocal(self, node):
                skills.add("python/scope")
                self.generic_visit(node)

            def visit_Try(self, node):
                skills.add("python/catching_exceptions")
                self.generic_visit(node)

            def visit_Raise(self, node):
                skills.add("python/raising_exceptions")
                self.generic_visit(node)

            def visit_Assert(self, node):
                skills.add("python/custom_exceptions")
                self.generic_visit(node)

            def visit_With(self, node):
                skills.add("python/with_statement")
                self.generic_visit(node)

            def visit_Attribute(self, node):
                if node.attr in ["read", "write"]:
                    skills.add("python/file_reading_writing")
                self.generic_visit(node)

            def visit_Yield(self, node):
                skills.add("python/generators")
                self.generic_visit(node)

            def visit_Import(self, node):
                # Check for specific library imports
                skills.add("python/importing_modules")
                for alias in node.names:
                    self.check_import(alias.name)
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                # Check for specific module imports from a library
                skills.add("python/using_packages")
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
                    skills.update(library_skill_mapping[name])
                if name in standard_libraries:
                    skills.add("python/standard_libraries")

        tree = ast.parse(content)
        collector = SkillCollector()
        collector.visit(tree)

        # Regex-based checks
        # Python Shell
        if re.search(r"^\s*>>> |\s*\.\.\. ", content, re.MULTILINE):
            skills.add("python/python_shell")

        # IPython Shell
        if re.search(
            r"^\s*In \[\d+\]: |\s*Out\[\d+\]: |^\s*%[a-zA-Z]+", content, re.MULTILINE
        ):
            skills.add("python/python_shell")

        return list(skills)

    def __parse_linux_skill(self, content):
        skills = []

        # 定义每个 SKILL ID 的匹配规则
        skill_patterns = {
            "linux/echo": r"\becho\b",
            "linux/clear": r"\bclear\b",
            "linux/ls": r"\bls\b",
            "linux/cd": r"\bcd\b",
            "linux/pwd": r"\bpwd\b",
            "linux/mkdir": r"\bmkdir\b",
            "linux/touch": r"\btouch\b",
            "linux/cp": r"\bcp\b",
            "linux/mv": r"\bmv\b",
            "linux/rm": r"\brm\b",
            "linux/ln": r"\bln\b",
            "linux/cat": r"\bcat\b",
            "linux/head": r"\bhead\b",
            "linux/tail": r"\btail\b",
            "linux/wc": r"\bwc\b",
            "linux/cut": r"\bcut\b",
            "linux/less": r"\bless\b",
            "linux/more": r"\bmore\b",
            "linux/chown": r"\bchown\b",
            "linux/chmod": r"\bchmod\b",
            "linux/wildcard_character": r"[\*\?]",  # 匹配星号或问号
            "linux/find": r"\bfind\b",
            "linux/locate": r"\blocate\b",
            "linux/which": r"\bwhich\b",
            "linux/whereis": r"\bwhereis\b",
            "linux/grep": r"\bgrep\b",
            "linux/sed": r"\bsed\b",
            "linux/awk": r"\bawk\b",
            "linux/sort": r"\bsort\b",
            "linux/uniq": r"\buniq\b",
            "linux/tr": r"\btr\b",
            "linux/col": r"\bcol\b",
            "linux/paste": r"\bpaste\b",
            "linux/join": r"\bjoin\b",
            "linux/diff": r"\bdiff\b",
            "linux/comm": r"\bcomm\b",
            "linux/patch": r"\bpatch\b",
            "linux/vim": r"\bvim\b",
            "linux/vimdiff": r"\bvimdiff\b",
            "linux/nano": r"\bnano\b",
            "linux/gedit": r"\bgedit\b",
            "linux/tar": r"\btar\b",
            "linux/zip": r"\bzip\b",
            "linux/unzip": r"\bunzip\b",
            "linux/bc": r"\bbc\b",
            "linux/logical": r"(&&|\|\|)",
            "linux/column": r"\bcolumn\b",
            "linux/test": r"\btest\b",
            "linux/xargs": r"\bxargs\b",
            "linux/tree": r"\btree\b",
            "linux/help": r"\bhelp\b",
            "linux/man": r"\bman\b",
            "linux/nl": r"\bnl\b",
            "linux/read": r"\bread\b",
            "linux/printf": r"\bprintf\b",
            "linux/sleep": r"\bsleep\b",
            "linux/declare": r"\bdeclare\b",
            "linux/source": r"(\bsource\b)",
            "linux/exit": r"\bexit\b",
            "linux/ssh": r"\bssh\b",
            "linux/telnet": r"\btelnet\b",
            "linux/scp": r"\bscp\b",
            "linux/sftp": r"\bsftp\b",
            "linux/ftp": r"\bftp\b",
            "linux/nc": r"\bnc\b",
            "linux/ifconfig": r"\bifconfig\b",
            "linux/netstat": r"\bnetstat\b",
            "linux/ping": r"\bping\b",
            "linux/ip": r"\bip\b",
            "linux/useradd": r"\buseradd\b",
            "linux/userdel": r"\buserdel\b",
            "linux/usermod": r"\busermod\b",
            "linux/passwd": r"\bpasswd\b",
            "linux/sudo": r"\bsudo\b",
            "linux/su": r"\bsu\b",
            "linux/groups": r"\bgroups\b",
            "linux/groupadd": r"\bgroupadd\b",
            "linux/groupdel": r"\bgroupdel\b",
            "linux/chgrp": r"\bchgrp\b",
            "linux/whoami": r"\bwhoami\b",
            "linux/who": r"\bwho\b",
            "linux/env": r"\benv\b",
            "linux/id": r"\bid\b",
            "linux/set": r"\bset\b",
            "linux/export": r"\bexport\b",
            "linux/unset": r"\bunset\b",
            "linux/df": r"\bdf\b",
            "linux/du": r"\bdu\b",
            "linux/mount": r"\bmount\b",
            "linux/watch": r"\bwatch\b",
            "linux/crontab": r"\bcrontab\b",
            "linux/uname": r"\buname\b",
            "linux/hostname": r"\bhostname\b",
            "linux/ps": r"\bps\b",
            "linux/top": r"\btop\b",
            "linux/free": r"\bfree\b",
            "linux/date": r"\bdate\b",
            "linux/time": r"\btime\b",
            "linux/dd": r"\bdd\b",
            "linux/service": r"\bservice\b",
            "linux/curl": r"\bcurl\b",
            "linux/wget": r"\bwget\b",
            "linux/apt": r"\bapt\b",
            "linux/pip": r"\bpip\b",
            "linux/yum": r"\byum\b",
            "linux/jobs": r"\bjobs\b",
            "linux/bg_running": r"&\s*$",
            "linux/fg": r"\bfg\b",
            "linux/kill": r"\bkill\b",
            "linux/killall": r"\bkillall\b",
            "linux/pkill": r"\bpkill\b",
            "linux/wait": r"\bwait\b",
            "linux/bg_process": r"\b&\s",
            "linux/tee": r"\btee\b",
            "linux/pipeline": r"\|",
            "linux/redirect": r"(\>|\<|\>\>|2\>|\&\>)",
        }

        # 检查每个 SKILL ID 是否出现在内容中
        for skill, pattern in skill_patterns.items():
            if re.search(pattern, content):
                skills.append(skill)

        return list(set(skills))

    def __parse_tkinter_skill(self, content):
        build_in_functions = [
            "Button",
            "Checkbutton",
            "Combobox",
            "Entry",
            "Frame",
            "Label",
            "LabeledScale",
            "Labelframe",
            "Menubutton",
            "Notebook",
            "OptionMenu",
            "Panedwindow",
            "Progressbar",
            "Radiobutton",
            "Scale",
            "Scrollbar",
            "Separator",
            "Sizegrip",
            "Spinbox",
            "Treeview",
            "Canvas",
            "Listbox",
            "Menu",
            "Text",
            "Toplevel",
            "Variable",
            "BooleanVar",
            "DoubleVar",
            "IntVar",
            "StringVar",
            "BitmapImage",
            "PhotoImage",
            "Directory",
            "Open",
            "SaveAs",
            "Chooser",
            "Style",
            "Font",
        ]
        skills = []
        for function in build_in_functions:
            if f".{function}" in content:
                skills.append(f"tkinter/{function.lower()}")
        return list(set(skills))

    def __parse_sklearn_skill(self, content):
        sklearn_skills = """
        sklearn.base: Base Classes and Utility Functions
        sklearn.calibration: Probability Calibration
        sklearn.cluster: Clustering
        sklearn.compose: Composite Estimators
        sklearn.covariance: Covariance Estimators
        sklearn.cross_decomposition: Cross decomposition
        sklearn.datasets: Datasets
        sklearn.decomposition: Matrix Decomposition
        sklearn.discriminant_analysis: Discriminant Analysis
        sklearn.dummy: Dummy estimators
        sklearn.ensemble: Ensemble Methods
        sklearn.exceptions: Exceptions and Warnings
        sklearn.experimental: Experimental
        sklearn.feature_extraction: Feature Extraction
        sklearn.feature_selection: Feature Selection
        sklearn.gaussian_process: Gaussian Processes
        sklearn.impute: Impute
        sklearn.inspection: Inspection
        sklearn.isotonic: Isotonic Regression
        sklearn.kernel_approximation: Kernel Approximation
        sklearn.kernel_ridge: Kernel Ridge Regression
        sklearn.linear_model: Linear Models
        sklearn.manifold: Manifold Learning
        sklearn.metrics: Metrics
        sklearn.mixture: Gaussian Mixture Models
        sklearn.model_selection: Model Selection
        sklearn.multiclass: Multiclass Classification
        sklearn.multioutput: Multioutput Regression and Classification
        sklearn.naive_bayes: Naive Bayes
        sklearn.neighbors: Nearest Neighbors
        sklearn.neural_network: Neural Network Models
        sklearn.pipeline: Pipeline
        sklearn.preprocessing: Preprocessing and Normalization
        sklearn.random_projection: Random Projection
        sklearn.semi_supervised: Semi-Supervised Learning
        sklearn.svm: Support Vector Machines
        sklearn.tree: Decision Trees
        sklearn.utils: Utilities
        """

        clean_skills = []
        for line in sklearn_skills.split("\n"):
            if len(line) > 0:
                skill_id = line.split(": ")[0].strip()
                clean_skills.append(skill_id)

        add_skills = []
        for s in clean_skills:
            if f"{s}" in content:
                add_skills.append(s.replace(".", "/"))
        return list(set(add_skills))

    def __parse_shell_skill(self, content):
        skills = []

        # Basic Syntax and Structure
        if re.search(r"^\s*#!", content, re.MULTILINE):
            skills.append("shell/shebang")
        if re.search(r"#", content):
            skills.append("shell/comments")
        if re.search(r'["\']', content):
            skills.append("shell/quoting")

        # Variable Handling
        if re.search(r"\b[A-Za-z_][A-Za-z0-9_]*\s*=", content):
            skills.append("shell/variables_decl")
        if re.search(r"\$[A-Za-z_][A-Za-z0-9_]*", content):
            skills.append("shell/variables_usage")
        if re.search(r"\$\{[^}]*\}", content):
            skills.append("shell/param_expansion")
        if re.search(r"\$\([^\)]*\)", content):
            skills.append("shell/cmd_substitution")
        if re.search(r"\b[A-Za-z_][A-Za-z0-9_]*\s*=\s*\(", content):
            skills.append("shell/arrays")
        if re.search(r"\bdeclare\s+-A\b", content):
            skills.append("shell/assoc_arrays")

        # Control Flow
        if re.search(r"\bif\b", content):
            skills.append("shell/if_else")
        if re.search(r"\bcase\b", content):
            skills.append("shell/case")
        if re.search(r"\bfor\b", content):
            skills.append("shell/for_loops")
        if re.search(r"\bwhile\b", content):
            skills.append("shell/while_loops")
        if re.search(r"\buntil\b", content):
            skills.append("shell/until_loops")
        if re.search(r"\[\[.*\]\]|\[.*\]", content):
            skills.append("shell/cond_expr")
        if re.search(r"\bexit\b|\breturn\b", content):
            skills.append("shell/exit_status")

        # Functions and Scope
        if re.search(r"\bfunction\b", content):
            skills.append("shell/func_def")
        if re.search(r"\blocal\b", content):
            skills.append("shell/scope_vars")

        # Advanced Scripting Concepts
        if re.search(r"\(\(", content):
            skills.append("shell/arith_expansion")
        if re.search(r"\>\|?|\|>|<\(|<<", content):
            skills.append("shell/adv_redirection")
        if re.search(r"<<<", content):
            skills.append("shell/here_strings")

        # System Interaction and Configuration
        if re.search(r"\btrap\b", content):
            skills.append("shell/trap_statements")
        if re.search(r"\bset\b|\bshopt\b", content):
            skills.append("shell/shell_options")
        if re.search(r"\bjobs\b|\bfg\b|\bbg\b", content):
            skills.append("shell/signal_handling")
        if re.search(r"\*|\?|\[", content):
            skills.append("shell/globbing_expansion")

        # Subshells and Command Groups
        if re.search(r"\([^)]*\)", content):
            skills.append("shell/subshells")

        # String Manipulation
        if re.search(r"\$\{[^}]*\}", content) or re.search(
            r"\b[A-Za-z_][A-Za-z0-9_]*\s*\+=\s*", content
        ):
            skills.append("shell/str_manipulation")

        # Arithmetic Operations
        if re.search(r"\b[0-9]+(\s*[\+\-\*/]\s*[0-9]+)+", content) or re.search(
            r"\$\(\s*[0-9]+ \s*[\+\-\*/] \s*[0-9]+\s*\)", content
        ):
            skills.append("shell/arith_ops")

        # Reading Input
        if re.search(r"\bread\b", content):
            skills.append("shell/read_input")

        # Exit Status Checks
        if re.search(r"\$\?", content):
            skills.append("shell/exit_status_checks")

        return list(set(skills))

    def __parse_rust_skill(self, content):
        skills = []

        # Define a dictionary to map skill IDs to their corresponding regex patterns
        skill_patterns = {
            "rust/variable_declarations": r"\b(?:let(?:\s+mut)?|const)\b",
            "rust/mutable_variables": r"\b(?:let\s+mut)\b",
            "rust/constants_usage": r"\b(?:const)\b",
            "rust/shadowing": r"\b(?:let)\b.*\b(?:let)\b",
            "rust/generic_types": r"\b(?:<\w+>)\b",
            "rust/traits": r"\b(?:trait\s+\w+|impl\s+\w+)\b",
            "rust/unsafe_rust": r"\b(?:unsafe)\b",
            "rust/operator_overloading": r"\b(?:\+|-|\*|/|%|==|!=|<|>)\b",
            "rust/ffi": r'\b(?:extern\s+"[^\"]+"\s*\{\s*fn\s+\w+)\b',
            "rust/integer_types": r"\b(?:i[0-9]+\b|\bu[0-9]+\b)",
            "rust/floating_types": r"\b(?:f[0-9]+\b)",
            "rust/boolean_type": r"\b(?:true|false)\b",
            "rust/char_type": r"\b(?:\'[^\']\'|\"[^\"]\")\b",
            "rust/string_type": r"\b(?:\"[^\"]*\")\b",
            "rust/tuple_type": r"\b(?:\([^)]*\))\b",
            "rust/array_type": r"\b(?:\[[^\]]*\])\b",
            "rust/type_casting": r"\b(?:as)\b",
            "rust/function_syntax": r"\b(?:fn\s+\w+)\b",
            "rust/function_params": r"\b(?:fn\s+\w+\s*\([^)]*\))\b",
            "rust/return_values": r"\b(?:->)\b",
            "rust/expressions_statements": r"\b(?:\w+\s*=\s*[^;]+\b|\b[^;]+\s*;\s*)",
            "rust/closures": r"\b(?:\|[^|]*\|\s*->)\b",
            "rust/if_expression": r"\b(?:if\s*\([^)]*\))\b",
            "rust/while_loop": r"\b(?:while\s*\([^)]*\))\b",
            "rust/for_loop": r"\b(?:for\s+\w+\s+in)\b",
            "rust/pattern_matching": r"\b(?:match\s*\w+\s*\{[^\}]+\})\b",
            "rust/iterators": r"\b(?:\.\w+\(\)|\w+\.\w+\(\))\b",
            "rust/ownership_rules": r"\b(?:\&\w+|\&mut\s+\w+|\&\'[^\']+)\b",
            "rust/references_borrowing": r"\b(?:\&\w+|\&mut\s+\w+|\&\'[^\']+)\b",
            "rust/slices": r"\b(?:&\w+\[[^\]]*\])\b",
            "rust/lifetime_specifiers": r"\b(?:\'[^\']+\b)",
            "rust/box_usage": r"\b(?:Box::new\([^)]*\))\b",
            "rust/deref_trait": r"\b(?:\*\w+)\b",
            "rust/drop_trait": r"\b(?:impl\s+Drop\s+for\s+\w+)|\b(?:(?:\*\w+\s*=\s*)?Drop::drop\([^)]*\))\b",
            "rust/rc_pointer": r"\b(?:Rc::new\([^)]*\)|Rc::clone\([^)]*\))\b",
            "rust/struct_def": r"\b(?:struct\s+\w+\s*\{|enum\s+\w+\s*\{)\b",
            "rust/struct_instantiate": r"\b(?:\w+\s*{\s*[^\}]+\})\b",
            "rust/method_syntax": r"\b(?:\.\w+\(|\w+::\w+\()",
            "rust/enum_def": r"\b(?:enum\s+\w+\s*\{[^\}]+\})\b",
            "rust/match_operator": r"\b(?:match\s+\w+\s*\{[^\}]+\})\b",
            "rust/if_let": r"\b(?:if\s+let\s+\w+\s*=\s*\w+\s*\{)\b",
            "rust/panic_usage": r"\b(?:panic!\s*\()",
            "rust/result_enum": r"\b(?:Result<[^>]+,[^>]+>)\b",
            "rust/error_propagation": r"\b(?:\?\w+|\b(?:try)\b)",
            "rust/writing_tests": r"\b(?:\#[\[\w\s\]]+\btest\b)",
            "rust/running_tests": r"\b(?:\btest\b\s*\()",
            "rust/test_org": r"\b(?:\btest\b\s*\()",
            "rust/async_programming": r"\b(?:async\s+\{|\bawait\b|\basync\s+fn\b)",
            "rust/thread_usage": r"\b(?:std::thread::spawn\(|std::thread::join\(|std::thread::sleep\()",
            "rust/message_passing": r"\b(?:std::sync::mpsc::channel\(|recv\(|send\()",
            "rust/shared_state_concurrency": r"\b(?:std::sync::Arc::new\(|std::sync::Mutex::lock\(|std::sync::RwLock::read\(|std::sync::RwLock::write\()",
            "rust/create_package": r'\b(?:cargo\s+new\s+\w+\s*--\s*[^"]+)',
            "rust/module_system": r"\b(?:mod\s+\w+\s*;)",
            "rust/cargo_crates": r"\b(?:\bextern\s+crate\s+\w+\b)",
            "rust/crates_io": r"\b(?:\buse\s+[\w:]+\s*;\s*//\s*crates\.io\b)",
            "rust/file_io": r"\b(?:std::fs::File::open\(|std::fs::File::create\(|std::fs::read_to_string\()",
            "rust/std_io": r"\b(?:std::io::stdin\(|std::io::stdout\(|std::io::stderr\(|std::io::Read::read_to_string\(|std::io::Write::write_all\()",
            "rust/io_errors": r"\b(?:std::io::Result<[^>]+>)\b",
            "rust/declarative_macros": r"\b(?:macro_rules!\s+\w+\s*\{[^}]+\})\b",
            "rust/procedural_macros": r"\b(?:\bproc_macro\b\s*::\s*TokenStream\b)",
            "rust/attributes": r"\b(?:\#\[[^\]]+\])\b",
        }

        # Iterate through the skill patterns and check if they match in the content
        for skill_id, pattern in skill_patterns.items():
            if re.search(pattern, content):
                skills.append(skill_id)

        return list(set(skills))

    def __parse_pygame_skill(self, content):
        build_in_functions = [
            "color",
            "display",
            "draw",
            "event",
            "font",
            "image",
            "key",
            "locals",
            "mixer",
            "mouse",
            "rect",
            "surface",
            "time",
            "music",
            "cursors",
            "joystick",
            "mask",
            "sprite",
            "transform",
            "bufferproxy",
            "freetype",
            "gfxdraw",
            "midi",
            "pixelarray",
            "pixelcopy",
            "sndarray",
            "surfarray",
            "math",
            "camera",
            "controller",
            "examples",
            "fastevent",
            "scrap",
            "tests",
            "touch",
            "version",
        ]

        skills = []
        for function in build_in_functions:
            if f"pygame.{function}." in content:
                skills.append(f"pygame/{function}")
        return list(set(skills))

    def __parse_django_skill(self, content):
        skills = []
        # django/applications
        if "django.apps" in content:
            skills.append("django/applications")
        # django/built_in_views
        if (
            "django.views.generic" in content
            or "django.views.View" in content
            or "django.views.TemplateView" in content
        ):
            skills.append("django/built_in_views")
        # django/clickjacking_protection
        if "django.middleware.clickjacking" in content:
            skills.append("django/clickjacking_protection")
        # django/contrib_packages
        if "django.contrib" in content:
            skills.append("django/contrib_packages")
        # django/databases
        if "django.db" in content:
            skills.append("django/databases")
        # django/django_admin
        if "django.contrib.admin" in content:
            skills.append("django/django_admin")
        # django/django_exceptions
        if "django.core.exceptions" in content:
            skills.append("django/django_exceptions")
        # django/file_handling
        if "django.core.files" in content:
            skills.append("django/file_handling")
        # django/forms
        if "django.forms" in content:
            skills.append("django/forms")
        # django/logging
        if "django.utils.log" in content:
            skills.append("django/logging")
        # django/middleware
        if "django.middleware" in content:
            skills.append("django/middleware")
        # django/migration_operations
        if "django.db.migrations" in content:
            skills.append("django/migration_operations")
        # django/models
        if "django.db.models" in content:
            skills.append("django/models")
        # django/paginator
        if "django.core.paginator" in content:
            skills.append("django/paginator")
        # django/request_and_response
        if "django.http" in content:
            skills.append("django/request_and_response")
        # django/schemaeditor
        if "django.db.models" in content:
            skills.append("django/schemaeditor")
        # django/settings
        if "django.conf.settings" in content:
            skills.append("django/settings")
        # django/signals
        if "django.dispatch" in content:
            skills.append("django/signals")
        # django/templates
        if "django.template" in content:
            skills.append("django/templates")
        # django/simpletemplateresponse
        if "django.template.response" in content:
            skills.append("django/simpletemplateresponse")
        # django/unicode_data
        if "django.utils.encoding" in content:
            skills.append("django/unicode_data")
        # django/django_urls
        if "django.urls" in content:
            skills.append("django/django_urls")
        # django/validators
        if "django.core.validators" in content:
            skills.append("django/validators")
        return list(set(skills))

    def __parse_go_skill(self, content):
        skills = []
        # go/for
        if "for " in content:
            skills.append("go/for")
        # go/if_else
        if "if " in content and "else " in content:
            skills.append("go/if_else")
        # go/switch
        if "switch " in content and "case " in content:
            skills.append("go/switch")
        # go/slices
        if "[]" in content:
            skills.append("go/slices")
        # go/range
        if "range " in content:
            skills.append("go/range")
        # go/maps
        if "map " in content:
            skills.append("go/maps")
        # go/functions
        if "() {" in content and "func " in content:
            skills.append("go/functions")
        # go/variables
        if "var " in content:
            skills.append("go/variables")
        # go/constants
        if "const " in content:
            skills.append("go/constants")
        # go/closures
        if "func " in content and "return " in content:
            skills.append("go/closures")
        # go/pointers
        if "*" in content:
            skills.append("go/pointers")
        # go/strings
        if "string " in content:
            skills.append("go/strings")
        # go/structs
        if "struct " in content:
            skills.append("go/structs")
        # go/interfaces
        if "interface " in content:
            skills.append("go/interfaces")
        # go/struct_embedding
        if "type " in content:
            skills.append("go/struct_embedding")
        # go/generics
        if "<" in content and ">" in content:
            skills.append("go/generics")
        # go/errors
        if "error " in content:
            skills.append("go/errors")
        # go/channels
        if "chan " in content:
            skills.append("go/channels")
        # go/select
        if "select " in content:
            skills.append("go/select")
        # go/timeouts
        if "time.Sleep(" in content:
            skills.append("go/timeouts")
        # go/timers
        if "time.AfterFunc(" in content:
            skills.append("go/timers")
        # go/tickers
        if "time.Tick(" in content:
            skills.append("go/tickers")
        # go/waitgroups
        if "sync.WaitGroup " in content:
            skills.append("go/waitgroups")
        # go/rate_limiting
        if "time.Sleep(" in content:
            skills.append("go/rate_limiting")
        # go/atomic
        if "atomic.Value " in content:
            skills.append("go/atomic")
        # go/mutexes
        if "sync.Mutex " in content:
            skills.append("go/mutexes")
        # go/sorting
        if "sort.Slice " in content:
            skills.append("go/sorting")
        # go/panic
        if "panic(" in content:
            skills.append("go/panic")
        # go/defer
        if "defer " in content:
            skills.append("go/defer")
        # go/recover
        if "recover(" in content:
            skills.append("go/recover")
        # go/text_templates
        if "template " in content:
            skills.append("go/text_templates")
        # go/regular_expressions
        if "regexp " in content:
            skills.append("go/regular_expressions")
        # go/json
        if "json.Marshal " in content:
            skills.append("go/json")
        # go/xml
        if "xml.Marshal " in content:
            skills.append("go/xml")
        # go/time
        if "time.Now " in content:
            skills.append("go/time")
        # go/epoch
        if "time.Unix " in content:
            skills.append("go/epoch")
        # go/time_formatting_parsing
        if "time.Parse " in content:
            skills.append("go/time_formatting_parsing")
        # go/random_numbers
        if "rand.Intn " in content:
            skills.append("go/random_numbers")
        # go/number_parsing
        if "strconv.Atoi " in content:
            skills.append("go/number_parsing")
        # go/url_parsing
        if "url.Parse " in content:
            skills.append("go/url_parsing")
        # go/sha256_hashes
        if "crypto.SHA256 " in content:
            skills.append("go/sha256_hashes")
        # go/base64_encoding
        if "encoding.Base64 " in content:
            skills.append("go/base64_encoding")
        # go/reading_files
        if "os.Open " in content:
            skills.append("go/reading_files")
        # go/writing_files
        if "os.Create " in content:
            skills.append("go/writing_files")
        # go/line_filters
        if "bufio.NewScanner " in content:
            skills.append("go/line_filters")
        # go/file_paths
        if "filepath.Join " in content:
            skills.append("go/file_paths")
        # go/directories
        if "os.Mkdir " in content:
            skills.append("go/directories")
        # go/temporary_files_and_directories
        if "os.TempDir " in content:
            skills.append("go/temporary_files_and_directories")
        # go/embed_directive
        if "embed " in content:
            skills.append("go/embed_directive")
        # go/testing_and_benchmarking
        if "testing.T " in content:
            skills.append("go/testing_and_benchmarking")
        # go/command_line
        if "os.Args " in content:
            skills.append("go/command_line")
        # go/environment_variables
        if "os.Getenv " in content:
            skills.append("go/environment_variables")
        # go/http_client
        if "http.Get " in content:
            skills.append("go/http_client")
        # go/http_server
        if "http.HandleFunc " in content:
            skills.append("go/http_server")
        # go/context
        if "context.Background " in content:
            skills.append("go/context")
        # go/processes
        if "os.StartProcess " in content:
            skills.append("go/processes")
        # go/signals
        if "os.Signal " in content:
            skills.append("go/signals")
        # go/exit
        if "os.Exit " in content:
            skills.append("go/exit")
        # go/values
        if "reflect.ValueOf " in content:
            skills.append("go/values")

        return list(set(skills))

    def __parse_flask_skill(self, content):
        flask_skills = """
        Application Object
        Flask
        Flask.aborter
        Flask.aborter_class
        Flask.add_template_filter()
        Flask.add_template_global()
        Flask.add_template_test()
        Flask.add_url_rule()
        Flask.after_request()
        Flask.after_request_funcs
        Flask.app_context()
        Flask.app_ctx_globals_class
        Flask.async_to_sync()
        Flask.auto_find_instance_path()
        Flask.before_request()
        Flask.before_request_funcs
        Flask.blueprints
        Flask.cli
        Flask.config
        Flask.config_class
        Flask.context_processor()
        Flask.create_global_jinja_loader()
        Flask.create_jinja_environment()
        Flask.create_url_adapter()
        Flask.debug
        Flask.default_config
        Flask.delete()
        Flask.dispatch_request()
        Flask.do_teardown_appcontext()
        Flask.do_teardown_request()
        Flask.endpoint()
        Flask.ensure_sync()
        Flask.error_handler_spec
        Flask.errorhandler()
        Flask.extensions
        Flask.full_dispatch_request()
        Flask.get()
        Flask.get_send_file_max_age()
        Flask.got_first_request
        Flask.handle_exception()
        Flask.handle_http_exception()
        Flask.handle_url_build_error()
        Flask.handle_user_exception()
        Flask.has_static_folder
        Flask.import_name
        Flask.inject_url_defaults()
        Flask.instance_path
        Flask.iter_blueprints()
        Flask.jinja_env
        Flask.jinja_environment
        Flask.jinja_loader
        Flask.jinja_options
        Flask.json
        Flask.json_provider_class
        Flask.log_exception()
        Flask.logger
        Flask.make_aborter()
        Flask.make_config()
        Flask.make_default_options_response()
        Flask.make_response()
        Flask.make_shell_context()
        Flask.name
        Flask.open_instance_resource()
        Flask.open_resource()
        Flask.patch()
        Flask.permanent_session_lifetime
        Flask.post()
        Flask.preprocess_request()
        Flask.process_response()
        Flask.put()
        Flask.redirect()
        Flask.register_blueprint()
        Flask.register_error_handler()
        Flask.request_class
        Flask.request_context()
        Flask.response_class
        Flask.root_path
        Flask.route()
        Flask.run()
        Flask.secret_key
        Flask.select_jinja_autoescape()
        Flask.send_static_file()
        Flask.session_interface
        Flask.shell_context_processor()
        Flask.shell_context_processors
        Flask.should_ignore_error()
        Flask.static_folder
        Flask.static_url_path
        Flask.teardown_appcontext()
        Flask.teardown_appcontext_funcs
        Flask.teardown_request()
        Flask.teardown_request_funcs
        Flask.template_context_processors
        Flask.template_filter()
        Flask.template_folder
        Flask.template_global()
        Flask.template_test()
        Flask.test_cli_runner()
        Flask.test_cli_runner_class
        Flask.test_client()
        Flask.test_client_class
        Flask.test_request_context()
        Flask.testing
        Flask.trap_http_exception()
        Flask.update_template_context()
        Flask.url_build_error_handlers
        Flask.url_default_functions
        Flask.url_defaults()
        Flask.url_for()
        Flask.url_map
        Flask.url_map_class
        Flask.url_rule_class
        Flask.url_value_preprocessor()
        Flask.url_value_preprocessors
        Flask.view_functions
        Flask.wsgi_app()
        Blueprint Objects
        Blueprint
        Blueprint.add_app_template_filter()
        Blueprint.add_app_template_global()
        Blueprint.add_app_template_test()
        Blueprint.add_url_rule()
        Blueprint.after_app_request()
        Blueprint.after_request()
        Blueprint.after_request_funcs
        Blueprint.app_context_processor()
        Blueprint.app_errorhandler()
        Blueprint.app_template_filter()
        Blueprint.app_template_global()
        Blueprint.app_template_test()
        Blueprint.app_url_defaults()
        Blueprint.app_url_value_preprocessor()
        Blueprint.before_app_request()
        Blueprint.before_request()
        Blueprint.before_request_funcs
        Blueprint.cli
        Blueprint.context_processor()
        Blueprint.delete()
        Blueprint.endpoint()
        Blueprint.error_handler_spec
        Blueprint.errorhandler()
        Blueprint.get()
        Blueprint.get_send_file_max_age()
        Blueprint.has_static_folder
        Blueprint.import_name
        Blueprint.jinja_loader
        Blueprint.make_setup_state()
        Blueprint.open_resource()
        Blueprint.patch()
        Blueprint.post()
        Blueprint.put()
        Blueprint.record()
        Blueprint.record_once()
        Blueprint.register()
        Blueprint.register_blueprint()
        Blueprint.register_error_handler()
        Blueprint.root_path
        Blueprint.route()
        Blueprint.send_static_file()
        Blueprint.static_folder
        Blueprint.static_url_path
        Blueprint.teardown_app_request()
        Blueprint.teardown_request()
        Blueprint.teardown_request_funcs
        Blueprint.template_context_processors
        Blueprint.template_folder
        Blueprint.url_default_functions
        Blueprint.url_defaults()
        Blueprint.url_value_preprocessor()
        Blueprint.url_value_preprocessors
        Blueprint.view_functions
        Incoming Request Data
        Request
        Request.accept_charsets
        Request.accept_encodings
        Request.accept_languages
        Request.accept_mimetypes
        Request.access_control_request_headers
        Request.access_control_request_method
        Request.access_route
        Request.application()
        Request.args
        Request.authorization
        Request.base_url
        Request.blueprint
        Request.blueprints
        Request.cache_control
        Request.charset
        Request.close()
        Request.content_encoding
        Request.content_length
        Request.content_md5
        Request.content_type
        Request.cookies
        Request.data
        Request.date
        Request.dict_storage_class
        Request.encoding_errors
        Request.endpoint
        Request.environ
        Request.files
        Request.form
        Request.form_data_parser_class
        Request.from_values()
        Request.full_path
        Request.get_data()
        Request.get_json()
        Request.headers
        Request.host
        Request.host_url
        Request.if_match
        Request.if_modified_since
        Request.if_none_match
        Request.if_range
        Request.if_unmodified_since
        Request.input_stream
        Request.is_json
        Request.is_multiprocess
        Request.is_multithread
        Request.is_run_once
        Request.is_secure
        Request.json
        Request.list_storage_class
        Request.make_form_data_parser()
        Request.max_content_length
        Request.max_form_memory_size
        Request.max_form_parts
        Request.max_forwards
        Request.method
        Request.mimetype
        Request.mimetype_params
        Request.on_json_loading_failed()
        Request.origin
        Request.parameter_storage_class
        Request.path
        Request.pragma
        Request.query_string
        Request.range
        Request.referrer
        Request.remote_addr
        Request.remote_user
        Request.root_path
        Request.root_url
        Request.routing_exception
        Request.scheme
        Request.script_root
        Request.server
        Request.shallow
        Request.stream
        Request.trusted_hosts
        Request.url
        Request.url_charset
        Request.url_root
        Request.url_rule
        Request.user_agent
        Request.user_agent_class
        Request.values
        Request.view_args
        Request.want_form_data_parsed
        request
        Response Objects
        Response
        Response.accept_ranges
        Response.access_control_allow_credentials
        Response.access_control_allow_headers
        Response.access_control_allow_methods
        Response.access_control_allow_origin
        Response.access_control_expose_headers
        Response.access_control_max_age
        Response.add_etag()
        Response.age
        Response.allow
        Response.autocorrect_location_header
        Response.automatically_set_content_length
        Response.cache_control
        Response.calculate_content_length()
        Response.call_on_close()
        Response.charset
        Response.close()
        Response.content_encoding
        Response.content_language
        Response.content_length
        Response.content_location
        Response.content_md5
        Response.content_range
        Response.content_security_policy
        Response.content_security_policy_report_only
        Response.content_type
        Response.cross_origin_embedder_policy
        Response.cross_origin_opener_policy
        Response.data
        Response.date
        Response.default_mimetype
        Response.default_status
        Response.delete_cookie()
        Response.direct_passthrough
        Response.expires
        Response.force_type()
        Response.freeze()
        Response.from_app()
        Response.get_app_iter()
        Response.get_data()
        Response.get_etag()
        Response.get_json()
        Response.get_wsgi_headers()
        Response.get_wsgi_response()
        Response.implicit_sequence_conversion
        Response.is_json
        Response.is_sequence
        Response.is_streamed
        Response.iter_encoded()
        Response.json
        Response.last_modified
        Response.location
        Response.make_conditional()
        Response.make_sequence()
        Response.max_cookie_size
        Response.mimetype
        Response.mimetype_params
        Response.response
        Response.retry_after
        Response.set_cookie()
        Response.set_data()
        Response.set_etag()
        Response.status
        Response.status_code
        Response.stream
        Response.vary
        Response.www_authenticate
        Sessions
        session
        session.new
        session.modified
        session.permanent
        Session Interface
        SessionInterface
        SessionInterface.get_cookie_domain()
        SessionInterface.get_cookie_httponly()
        SessionInterface.get_cookie_name()
        SessionInterface.get_cookie_path()
        SessionInterface.get_cookie_samesite()
        SessionInterface.get_cookie_secure()
        SessionInterface.get_expiration_time()
        SessionInterface.is_null_session()
        SessionInterface.make_null_session()
        SessionInterface.null_session_class
        SessionInterface.open_session()
        SessionInterface.pickle_based
        SessionInterface.save_session()
        SessionInterface.should_set_cookie()
        SecureCookieSessionInterface
        SecureCookieSessionInterface.digest_method()
        SecureCookieSessionInterface.key_derivation
        SecureCookieSessionInterface.open_session()
        SecureCookieSessionInterface.salt
        SecureCookieSessionInterface.save_session()
        SecureCookieSessionInterface.serializer
        SecureCookieSessionInterface.session_class
        SecureCookieSession
        SecureCookieSession.accessed
        SecureCookieSession.get()
        SecureCookieSession.modified
        SecureCookieSession.setdefault()
        NullSession
        NullSession.clear()
        NullSession.pop()
        NullSession.popitem()
        NullSession.setdefault()
        NullSession.update()
        SessionMixin
        SessionMixin.accessed
        SessionMixin.modified
        SessionMixin.permanent
        Test Client
        FlaskClient
        FlaskClient.open()
        FlaskClient.session_transaction()
        Test CLI Runner
        FlaskCliRunner
        FlaskCliRunner.invoke()
        Application Globals
        g
        _AppCtxGlobals
        _AppCtxGlobals.get()
        _AppCtxGlobals.pop()
        _AppCtxGlobals.setdefault()
        Useful Functions and Classes
        current_app
        has_request_context()
        copy_current_request_context()
        has_app_context()
        url_for()
        abort()
        redirect()
        make_response()
        after_this_request()
        send_file()
        send_from_directory()
        Message Flashing
        flash()
        get_flashed_messages()
        JSON Support
        jsonify()
        dumps()
        dump()
        loads()
        load()
        JSONProvider
        JSONProvider.dumps()
        JSONProvider.dump()
        JSONProvider.loads()
        JSONProvider.load()
        JSONProvider.response()
        DefaultJSONProvider
        DefaultJSONProvider.default()
        DefaultJSONProvider.ensure_ascii
        DefaultJSONProvider.sort_keys
        DefaultJSONProvider.compact
        DefaultJSONProvider.mimetype
        DefaultJSONProvider.dumps()
        DefaultJSONProvider.loads()
        DefaultJSONProvider.response()
        Tagged JSON
        TaggedJSONSerializer
        TaggedJSONSerializer.default_tags
        TaggedJSONSerializer.dumps()
        TaggedJSONSerializer.loads()
        TaggedJSONSerializer.register()
        TaggedJSONSerializer.tag()
        TaggedJSONSerializer.untag()
        JSONTag
        JSONTag.check()
        JSONTag.key
        JSONTag.tag()
        JSONTag.to_json()
        JSONTag.to_python()
        Template Rendering
        render_template()
        render_template_string()
        stream_template()
        stream_template_string()
        get_template_attribute()
        Configuration
        Config
        Config.from_envvar()
        Config.from_file()
        Config.from_mapping()
        Config.from_object()
        Config.from_prefixed_env()
        Config.from_pyfile()
        Config.get_namespace()
        Stream Helpers
        stream_with_context()
        Useful Internals
        RequestContext
        RequestContext.copy()
        RequestContext.match_request()
        RequestContext.pop()
        flask.globals.request_ctx
        AppContext
        AppContext.pop()
        AppContext.push()
        flask.globals.app_ctx
        BlueprintSetupState
        BlueprintSetupState.add_url_rule()
        BlueprintSetupState.app
        BlueprintSetupState.blueprint
        BlueprintSetupState.first_registration
        BlueprintSetupState.options
        BlueprintSetupState.subdomain
        BlueprintSetupState.url_defaults
        BlueprintSetupState.url_prefix
        Signals
        template_rendered
        request_started
        request_finished
        got_request_exception
        request_tearing_down
        appcontext_tearing_down
        appcontext_pushed
        appcontext_popped
        message_flashed
        signals.signals_available
        Class-Based Views
        View
        View.as_view()
        View.decorators
        View.dispatch_request()
        View.init_every_request
        View.methods
        View.provide_automatic_options
        MethodView
        MethodView.dispatch_request()
        URL Route Registrations
        View Function Options
        Command Line Interface
        FlaskGroup
        FlaskGroup.get_command()
        FlaskGroup.list_commands()
        FlaskGroup.make_context()
        FlaskGroup.parse_args()
        AppGroup
        AppGroup.command()
        AppGroup.group()
        ScriptInfo
        ScriptInfo.app_import_path
        ScriptInfo.create_app
        ScriptInfo.data
        ScriptInfo.load_app()
        load_dotenv()
        with_appcontext()
        pass_script_info()
        run_command
        shell_command
        """

        skills_map = {
            "flask/appgroup": "flask/command_line_interface",
            "flask/securecookiesession": "flask/session_interface",
            "flask/request": "flask/incoming_request_data",
            "flask/blueprint": "flask/blueprint_objects",
            "flask/_appctxglobals": "flask/application_globals",
            "flask/config": "flask/configuration",
            "flask/view": "flask/class_based_views",
            "flask/blueprintsetupstate": "flask/useful_internals",
            "flask/appcontext": "flask/useful_internals",
            "flask/session": "flask/sessions",
            "flask/flaskclirunner": "flask/test_cli_runner",
            "flask/response": "flask/response_objects",
            "flask/jsonprovider": "flask/json_support",
            "flask/flaskclient": "flask/test_client",
            "flask/nullsession": "flask/session_interface",
            "flask/sessionmixin": "flask/session_interface",
            "flask/taggedjsonserializer": "flask/json_support",
            "flask/scriptinfo": "flask/command_line_interface",
            "flask/flask": "flask/application_object",
            "flask/defaultjsonprovider": "flask/json_support",
            "flask/jsontag": "flask/json_support",
            "flask/requestcontext": "flask/useful_internals",
        }

        all_skills = {}

        for line in flask_skills.split("\n"):
            if len(line) > 0:
                split_line = line.split(".")
                if len(split_line) > 1:
                    skill_id = line.split(".")[0].strip()
                    skill_function = line.split(
                        ".")[1].strip().replace(")", "")
                    if skill_id not in all_skills:
                        all_skills[skill_id] = []
                    all_skills[skill_id].append(skill_function)

        add_skills = []
        for s_name in all_skills:
            for s_id in all_skills[s_name]:
                if s_id in content:
                    add_skills.append(skills_map[f"flask/{s_name.lower()}"])
        return list(set(add_skills))

    def __parse_cpp_skill(self, content):
        skills = []
        # Variables: Look for variable declarations
        if re.search(
            r"\bint\b|\bfloat\b|\bdouble\b|\bchar\b|\bwchar_t\b|\bbool\b", content
        ):
            skills.append("cpp/variables")

        # Data Types: Look for specific data type declarations
        if re.search(
            r"\bint\b|\bfloat\b|\bdouble\b|\bchar\b|\bwchar_t\b|\bbool\b|\blong\b|\bshort\b",
            content,
        ):
            skills.append("cpp/data_types")

        # Operators: Look for operators like +, -, *, /, %, ++, --
        if re.search(r"\+|-|\*|\/|%|\+\+|--", content):
            skills.append("cpp/operators")

        # Booleans: Look for boolean values and operators
        if re.search(r"\btrue\b|\bfalse\b|\b&&\b|\b\|\|\b|\b!\b", content):
            skills.append("cpp/booleans")

        # Arrays: Look for array declarations
        if re.search(r"\b\w+\[\d*\]", content):
            skills.append("cpp/arrays")

        # Strings: Look for string declarations
        if re.search(r"\bstd::string\b|\bchar\s+\w+\[\d*\]", content):
            skills.append("cpp/strings")

        # Conditions: Look for if, else if, else
        if re.search(r"\bif\b|\belse\b", content):
            skills.append("cpp/conditions")

        # If...Else: Specific check for if-else structure
        if re.search(r"\bif\s*\(.*\)\s*\{.*\}\s*else\s*\{.*\}", content):
            skills.append("cpp/if_else")

        # Switch: Look for switch-case structure
        if re.search(r"\bswitch\s*\(.*\)\s*\{", content):
            skills.append("cpp/switch")

        # Loops: Look for different loop structures
        if re.search(r"\bfor\s*\(.*\)\s*\{", content):
            skills.append("cpp/for_loop")
        if re.search(r"\bwhile\s*\(.*\)\s*\{", content):
            skills.append("cpp/while_loop")

        # Break/Continue: Look for break and continue statements
        if re.search(r"\bbreak\b|\bcontinue\b", content):
            skills.append("cpp/break_continue")

        # Functions: Look for function definitions
        if re.search(r"\b\w+\s+\w+\s*\([^)]*\)\s*\{", content):
            skills.append("cpp/functions")

        # Function Parameters: Look for functions with parameters
        if re.search(r"\b\w+\s+\w+\s*\([^)]+.*\)\s*\{", content):
            skills.append("cpp/function_parameters")

        # Function Overloading: This is harder to detect directly without more context
        # Recursion: This is also difficult to detect directly without analyzing the function's behavior

        # Classes/Objects: Look for class definitions
        if re.search(r"\bclass\b\s+\w+\s*\{", content):
            skills.append("cpp/classes_objects")

        # Class Methods: Look for methods inside class definitions
        if re.search(r"\bclass\b\s+\w+\s*\{[^}]*\b\w+\s+\w+\s*\([^)]*\)\s*\{", content):
            skills.append("cpp/class_methods")

        # Access Specifiers: Look for public, private, protected
        if re.search(r"\bpublic\b|\bprivate\b|\bprotected\b", content):
            skills.append("cpp/access_specifiers")

        # Constructors: Look for constructor definitions
        if re.search(r"\b\w+::\w+\s*\([^)]*\)\s*:", content):
            skills.append("cpp/constructors")

        # Encapsulation, Inheritance, Polymorphism, Pointers, References, Structures, Exceptions, Templates
        # These require more complex analysis or context and are hard to detect with simple regex.

        # Output: Look for cout statements
        if re.search(r"\bstd::cout\b", content):
            skills.append("cpp/output")

        # User Input: Look for cin statements
        if re.search(r"\bstd::cin\b", content):
            skills.append("cpp/user_input")

        # Files: Look for file operations
        if re.search(r"\bstd::fstream\b|\bstd::ifstream\b|\bstd::ofstream\b", content):
            skills.append("cpp/files")

        # Math: Look for math operations and functions
        if re.search(r"\bsqrt\b|\bpow\b|\bfabs\b|\bceil\b|\bfloor\b", content):
            skills.append("cpp/math")

        # String manipulation: Look for string operations
        if re.search(
            r"\bstd::string\b.*\.length\b|\bstd::string\b.*\.substr\b|\bstd::string\b.*\.find\b",
            content,
        ):
            skills.append("cpp/string_manipulation")

        # Standard Containers: Look for standard container usage like vector, map, set
        if re.search(r"\bstd::vector\b|\bstd::map\b|\bstd::set\b", content):
            skills.append("cpp/standard_containers")

        # Comments: Look for single and multi-line comments
        if re.search(r"//|/\*.*\*/", content):
            skills.append("cpp/comments")

        # Code Formatting: This is more about the style and cannot be detected via regex.
        # Function Overloading: Difficult to detect with regex, requires analysis of multiple function signatures with the same name
        # Recursion: Hard to detect with regex, requires analyzing whether a function calls itself

        # Encapsulation: Generally related to the use of access specifiers and class structure
        if re.search(r"\bclass\b.*\b(private|protected|public)\b", content):
            skills.append("cpp/encapsulation")

        # Inheritance: Look for class inheritance patterns
        if re.search(
            r"\bclass\b\s+\w+\s*:\s*(public|private|protected)\s+\w+", content
        ):
            skills.append("cpp/inheritance")

        # Polymorphism: Complex to detect, often involves function overriding in derived classes
        # Pointers: Look for pointer declarations
        if re.search(r"\b\w+\s*\*\w+", content):
            skills.append("cpp/pointers")

        # References: Look for reference declarations
        if re.search(r"\b\w+&\w+", content):
            skills.append("cpp/references")

        # Structures: Look for struct definitions
        if re.search(r"\bstruct\b\s+\w+", content):
            skills.append("cpp/structures")

        # Exceptions: Look for try, catch, throw
        if re.search(r"\btry\b|\bcatch\b|\bthrow\b", content):
            skills.append("cpp/exceptions")

        # Templates: Look for template declarations
        if re.search(r"\btemplate\s*<", content):
            skills.append("cpp/templates")
        return list(set(skills))

    def __parse_c_skill(self, content):
        skills = []
        # Variables
        if re.search(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*=", content):
            skills.append("c/variables")

        # Data Types
        if re.search(r"\b(int|char|float|double|long|short)\b", content):
            skills.append("c/data_types")

        # Constants
        if re.search(r"\b(const)\b", content):
            skills.append("c/constants")

        # Operators
        if re.search(r"[-+*/%<>=!&|]", content):
            skills.append("c/operators")

        # Comments
        if re.search(r"//|/\*.*\*/", content, re.DOTALL):
            skills.append("c/comments")

        # If...Else
        if re.search(r"\bif\s*\(|\belse\b", content):
            skills.append("c/if_else")

        # Switch
        if re.search(r"\bswitch\s*\(", content):
            skills.append("c/switch")

        # For Loop
        if re.search(r"\bfor\s*\(", content):
            skills.append("c/for_loop")

        # While Loop
        if re.search(r"\bwhile\s*\(", content):
            skills.append("c/while_loop")

        # Break/Continue
        if re.search(r"\bbreak\b|\bcontinue\b", content):
            skills.append("c/break_continue")

        # Arrays
        if re.search(r"\[\]", content):
            skills.append("c/arrays")

        # Strings
        if re.search(r"\bchar\s*\*\s*|\bchar\s*\[", content):
            skills.append("c/strings")

        # Function Declaration
        if re.search(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*\{", content):
            skills.append("c/function_declaration")

        # Function Parameters
        if re.search(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]+\)\s*\{", content):
            skills.append("c/function_parameters")

        # Math Functions
        if re.search(r"\b(sin|cos|tan|sqrt|pow)\b", content):
            skills.append("c/math_functions")

        # Structures
        if re.search(r"\bstruct\b", content):
            skills.append("c/structures")

        # Enums
        if re.search(r"\benum\b", content):
            skills.append("c/enums")

        # Pointers
        if re.search(r"\*[^;=]*\s*\w+", content):
            skills.append("c/pointers")

        # Memory Address
        if re.search(r"\&[a-zA-Z_][a-zA-Z0-9_]*", content):
            skills.append("c/memory_address")

        # Write To Files
        if re.search(r"fopen\s*\([^)]*\)\s*|fprintf\s*\(", content):
            skills.append("c/write_to_files")

        # User Input
        if re.search(r"scanf\s*\(", content):
            skills.append("c/user_input")

        # Recursion
        for match in re.finditer(
            r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{", content
        ):
            func_name = match.group(1)
            func_body_start = match.end()
            brace_count = 1
            i = func_body_start
            while i < len(content) and brace_count > 0:
                if content[i] == "{":
                    brace_count += 1
                elif content[i] == "}":
                    brace_count -= 1
                i += 1
            func_body = content[func_body_start:i]
            if re.search(r"\b" + re.escape(func_name) + r"\s*\(", func_body):
                skills.append("c/recursion")
                break

        # Create Files
        if re.search(r"fopen\s*\([^)]*\)\s*", content):
            skills.append("c/create_files")

        # Read Files
        if re.search(r"fopen\s*\([^)]*\)\s*|fscanf\s*\(", content):
            skills.append("c/read_files")

        # Output
        if re.search(r"printf\s*\(", content):
            skills.append("c/output")

        return list(set(skills))

    def __parse_html_skill(self, content):
        skills = []

        # Basic HTML Structure
        if re.search(r"<(base|body)[ >]", content):
            skills.append("html/basic_elems")

        if re.search(r"<meta[^>]*charset", content):
            skills.append("html/charset")

        if re.search(r"<html[^>]*lang", content):
            skills.append("html/lang_decl")

        if re.search(r"<meta[^>]*viewport", content):
            skills.append("html/viewport")

        if re.search(r"<head[ >]", content):
            skills.append("html/head_elems")

        # HTML Text Content and Formatting
        if re.search(
            r"<(h[1-6]|strong|em|b|i|mark|del|ins|sub|sup|small|s|abbr|address|cite|blockquote)[ >]",
            content,
        ):
            skills.append("html/text_head")

        if re.search(r"<(p|br)[ >]", content):
            skills.append("html/para_br")

        if re.search(r"<(q|blockquote)[ >]", content):
            skills.append("html/quotes")

        if re.search(r"<(bdi|bdo)[ >]", content):
            skills.append("html/text_dir")

        if re.search(r"<(ol|ul|li|dl|dt|dd)[ >]", content):
            skills.append("html/lists_desc")

        # HTML Layout and Sectioning
        if re.search(r"<(section|article|aside|header|footer|main)[ >]", content):
            skills.append("html/layout")

        if re.search(r"<(nav|a)[ >]", content):
            skills.append("html/nav_links")

        if re.search(r"aria-", content):
            skills.append("html/access_cons")

        if re.search(r"<div[ >]", content):
            skills.append("html/doc_flow")

        # HTML Multimedia and Graphics
        if re.search(r"<(img|audio|video|canvas)[ >]", content):
            skills.append("html/multimedia")

        if re.search(r"<map[ >]", content):
            skills.append("html/img_maps")

        if re.search(r"<(figure|figcaption)[ >]", content):
            skills.append("html/fig_cap")

        if re.search(r"<(iframe|embed|object)[ >]", content):
            skills.append("html/embed_media")

        # HTML Tables
        if re.search(r"<table[ >]", content):
            skills.append("html/tables")

        if re.search(r"<table[^>]*(rowspan|colspan)[ >]", content):
            skills.append("html/complex_tbl")

        if re.search(r"<th[ >]", content):
            skills.append("html/tbl_access")

        # HTML Forms and Input
        if re.search(
            r"<(form|input|button|select|optgroup|option|label|fieldset|legend|datalist|output|textarea|progress|meter)[ >]",
            content,
        ):
            skills.append("html/forms")

        if re.search(r'(required|type=["\']text)["\']', content):
            skills.append("html/form_valid")

        if re.search(r"<fieldset[ >]", content):
            skills.append("html/form_group")

        if re.search(r"<(input|select|textarea|button)[^>]*aria-", content):
            skills.append("html/form_access")

        # Advanced HTML Elements
        if re.search(
            r"<(template|noscript|data|bdi|ruby|rt|rp|dfn|code|var|samp|kbd|pre)[ >]",
            content,
        ):
            skills.append("html/inter_elems")

        if re.search(r"data-[^=]*=", content):
            skills.append("html/custom_attr")

        if re.search(r"role=", content):
            skills.append("html/adv_access")

        if re.search(r"<template[ >]", content):
            skills.append("html/templating")

        return list(set(skills))

    def __parse_css_skill(self, content):
        skills = []
        # css/selectors
        if "{" in content and "}" in content and ":" in content:
            skills.append("css/selectors")
        # css/properties
        if ":" in content and ";" in content and "{" not in content:
            skills.append("css/properties")
        # css/values
        if ":" in content and ";" in content and "{" not in content:
            skills.append("css/values")
        # css/colors
        if "#" in content or "rgb(" in content or "rgba(" in content:
            skills.append("css/colors")
        # css/fonts
        if "font-" in content:
            skills.append("css/fonts")
        # css/text_styling
        if "text-" in content:
            skills.append("css/text_styling")
        # css/box_model
        if "box-" in content:
            skills.append("css/box_model")
        # css/margin_and_padding
        if "margin" in content or "padding:" in content:
            skills.append("css/margin_and_padding")
        # css/borders
        if "border" in content:
            skills.append("css/borders")
        # css/width_and_height
        if "width" in content or "height:" in content:
            skills.append("css/width_and_height")
        # css/display_property
        if "display" in content:
            skills.append("css/display_property")
        # css/positioning
        if "position" in content:
            skills.append("css/positioning")
        # css/flexbox
        if "flex" in content:
            skills.append("css/flexbox")
        # css/grid_layout
        if "grid-" in content:
            skills.append("css/grid_layout")
        # css/pseudo_classes
        if (
            ":hover" in content
            or ":active" in content
            or ":focus" in content
            or ":link" in content
            or ":visited" in content
            or ":first-child" in content
            or ":last-child" in content
            or ":nth-child" in content
            or ":nth-last-child" in content
            or ":nth-of-type" in content
            or ":nth-last-of-type" in content
            or ":first-of-type" in content
            or ":last-of-type" in content
            or ":only-child" in content
            or ":only-of-type" in content
            or ":empty" in content
            or ":target" in content
            or ":enabled" in content
            or ":disabled" in content
            or ":checked" in content
        ):
            skills.append("css/pseudo_classes")
        # css/pseudo_elements
        if "::" in content:
            skills.append("css/pseudo_elements")
        # css/backgrounds
        if "background" in content:
            skills.append("css/backgrounds")
        # css/lists_and_tables
        if "list-" in content or "table-" in content:
            skills.append("css/lists_and_tables")
        # css/media_queries
        if "@media" in content:
            skills.append("css/media_queries")
        # css/mobile_first_design
        if "min-" in content or "max-" in content:
            skills.append("css/mobile_first_design")
        # css/animations
        if "animation" in content:
            skills.append("css/animations")
        # css/transitions
        if "transition" in content:
            skills.append("css/transitions")
        # css/transformations
        if "transform" in content:
            skills.append("css/transformations")
        # css/variables
        if "--var" in content or "var(" in content:
            skills.append("css/variables")
        # css/mixins
        if "@" in content and "{" in content:
            skills.append("css/mixins")
        # css/nesting
        if "&" in content or ">" in content:
            skills.append("css/nesting")
        # css/import_and_extend
        if "extend" in content or "import" in content:
            skills.append("css/import_and_extend")
        # css/comments
        if "/*" in content or "*/" in content:
            skills.append("css/comments")

        return list(set(skills))

    def __parse_jquery_skill(self, content):
        skills = set()  # 使用集合以确保唯一性

        # 基础理解（Basic Understanding）
        if re.search(r"\.jQuery\(\s*'\w+'\s*\)", content):
            skills.add("jquery/syntax")

        if re.search(r"\$\(\s*'\w+'\s*\)", content):
            skills.add("jquery/selectors")

        if re.search(r"\.html\(\s*'\w+'\s*\)", content):
            skills.add("jquery/dom_interaction")

        # 事件处理（Event Handling）
        if re.search(r"\.click\(", content):
            skills.add("jquery/event_methods")

        if re.search(r"\.on\(\s*'click'", content):
            skills.add("jquery/event_delegation")

        if re.search(r"\.fadeIn\(", content):
            skills.add("jquery/event_effects")

        # DOM 操作（DOM Manipulation）
        if re.search(r"\.find\(", content):
            skills.add("jquery/dom_traversal")

        if re.search(r"\.text\(\s*'\w+'\s*\)", content):
            skills.add("jquery/content_manipulation")

        if re.search(r"\.append\(", content):
            skills.add("jquery/element_management")

        # 数据处理（Data Handling）
        if re.search(r"\.ajax\(", content):
            skills.add("jquery/ajax")

        if re.search(r"\.parseJSON\(", content):
            skills.add("jquery/json")

        if re.search(r"\.serialize\(", content):
            skills.add("jquery/form_serialization")

        # 高级技术（Advanced Techniques）
        if re.search(r"\.end\(\)", content):
            skills.add("jquery/chaining")

        if re.search(r"\.plugin\(", content):
            skills.add("jquery/plugins")

        if re.search(r"\.optimize\(", content):
            skills.add("jquery/performance")

        # 用户界面交互（User Interface Interaction）
        if re.search(r"\.show\(", content):
            skills.add("jquery/ui_effects")

        if re.search(r"\.datepicker\(", content):
            skills.add("jquery/widgets")

        if re.search(r"\.responsive\(", content):
            skills.add("jquery/responsive_design")

        return list(skills)

    def __parse_javascript_skill(self, content):
        skills = []

        # Basic Concepts
        if re.search(r"\bvar\b|\blet\b|\bconst\b", content):
            skills.append("javascript/variables")
        if re.search(
            r"['\"].*['\"]|\b\d+\b|\btrue\b|\bfalse\b|\bnull\b|\bundefined\b|\b\[\]|\b\{\}",
            content,
        ):
            skills.append("javascript/data_types")
        if re.search(r"\+|-|\*|\/|%|\+\+|--", content):
            skills.append("javascript/arith_ops")
        if re.search(r"==|!=|===|!==|>|<|>=|<=", content):
            skills.append("javascript/comp_ops")
        if re.search(r"\b&&\b|\b\|\|\b|\b!\b", content):
            skills.append("javascript/logic_ops")
        if re.search(r"\bif\b|\belse\b", content):
            skills.append("javascript/cond_stmts")
        if re.search(r"\bswitch\b.*\bcase\b", content, re.DOTALL):
            skills.append("javascript/switch_stmts")
        if re.search(r"\bfor\b|\bwhile\b|\bdo\b", content):
            skills.append("javascript/loops")
        if re.search(r"\bfunction\b\s+\w+|\bfunction\s*\(", content):
            skills.append("javascript/functions")
        if re.search(r"\b\w+\s*\+\s*['\"]|\b\w+\s*\+\=\s*['\"]", content):
            skills.append("javascript/str_manip")
        if re.search(r"\b\w+\s*\[\s*\w*\s*\]", content):
            skills.append("javascript/array_methods")
        if re.search(r"\b\w+\.\w+\s*=", content):
            skills.append("javascript/obj_manip")

        # Advanced Concepts
        if re.search(r"\bclass\b\s+\w+", content):
            skills.append("javascript/oop")
        if re.search(
            r"\bsetTimeout\b|\bsetInterval\b|\bPromise\b|\basync\b|\bawait\b", content
        ):
            skills.append("javascript/async_prog")
        if re.search(r"\btry\b|\bcatch\b|\bfinally\b|\bthrow\b", content):
            skills.append("javascript/error_handle")
        if re.search(r"function\s*\([^)]*\)\s*{[^}]*}[^)]*\)", content, re.DOTALL):
            skills.append("javascript/closures")
        if re.search(r"\bmap\b|\bfilter\b|\breduce\b", content):
            skills.append("javascript/higher_funcs")
        if re.search(r"\bprototype\b|\b__proto__\b|\bextends\b", content):
            skills.append("javascript/proto_inherit")
        if re.search(r"\{.*\:\s*\w+\s*\}", content):
            skills.append("javascript/destr_assign")
        if re.search(r"\.\.\.\w+", content):
            skills.append("javascript/spread_rest")
        if re.search(r"`[^`]*\$\{[^}]*\}[^`]*`", content):
            skills.append("javascript/template_lit")
        if re.search(r"import\s+.*\s+from\s+|export\s+.*", content):
            skills.append("javascript/es6")

        # DOM Manipulation
        if re.search(
            r"\bdocument\.getElementById\b|\bdocument\.querySelector\b", content
        ):
            skills.append("javascript/dom_select")
        if re.search(r"\binnerHTML\b|\btextContent\b|\bcreateElement\b", content):
            skills.append("javascript/dom_manip")
        if re.search(r"\baddEventListener\b", content):
            skills.append("javascript/event_handle")
        if re.search(r"\bparentNode\b|\bnextSibling\b|\bchildren\b", content):
            skills.append("javascript/dom_traverse")

        # Tools and Environment
        if re.search(r"\bconsole\.log\b|\bconsole\.", content):
            skills.append("javascript/debugging")
        if re.search(
            r"\bwindow\b|\bdocument\b|\bnavigator\b|\blocation\b|\bhistory\b", content
        ):
            skills.append("javascript/bom")
        if re.search(r"\blocalStorage\b|\bsessionStorage\b", content):
            skills.append("javascript/web_storage")

        # Networking
        if re.search(r"\bfetch\b|\bXMLHttpRequest\b", content):
            skills.append("javascript/http_req")
        if re.search(r"\bJSON\.parse\b|\bJSON\.stringify\b", content):
            skills.append("javascript/json")
        if re.search(r"\bfetch\b.*\bthen\b|\baxios\b", content):
            skills.append("javascript/api_interact")
        if re.search(r"\bWebSocket\b", content):
            skills.append("javascript/websockets")

        # Security
        if re.search(r"\binnerHTML\b|\bdocument\.createElement\b", content):
            skills.append("javascript/xss")
        if re.search(r"\bhttps\b|\bssl\b|\btls\b|\bsecurity\b", content):
            skills.append("javascript/web_sec")

        return list(set(skills))

    def __parse_react_skill(self, content):
        skills = []

        # JSX
        if re.search(r"(<\w+.*?>)|(<\/\w+>)", content):
            skills.append("react/jsx")

        # Components and Props
        if re.search(r"class\s+\w+\s+extends\s+React\.Component", content) or re.search(
            r"function\s+\w+\s*\(", content
        ):
            skills.append("react/components_props")

        # State and Lifecycle
        if re.search(r"this\.state\b|\bsetState\(", content):
            skills.append("react/state_lifecycle")

        # Handling Events
        if re.search(r"on[A-Z]\w+\s*=", content):
            skills.append("react/event_handling")

        # Conditional Rendering
        if re.search(r"\{.*\?.*\:.*\}", content):
            skills.append("react/conditional_render")

        # Lists and Keys
        if re.search(r"\.map\(", content) and "key=" in content:
            skills.append("react/list_keys")

        # Context API
        if re.search(r"React\.createContext", content):
            skills.append("react/context_api")

        # Higher-Order Components
        # Note: HOCs detection would require analyzing the pattern of function returning a component or wrapping components.

        # React Hooks
        if re.search(r"\buse[A-Z]\w+\b", content):
            skills.append("react/hooks")

        # Code Splitting
        if re.search(r"\bReact\.lazy\b", content) or re.search(
            r"\bimport\(\)", content
        ):
            skills.append("react/code_split")

        # Portals
        if re.search(r"React\.createPortal", content):
            skills.append("react/portals")

        # Error Boundaries
        if re.search(r"componentDidCatch", content) or re.search(
            r"getDerivedStateFromError", content
        ):
            skills.append("react/error_boundary")

        # Using useState and useReducer
        if re.search(r"\buseState\b|\buseReducer\b", content):
            skills.append("react/use_state_reducer")

        # Managing Global State
        # Note: Global state management would typically involve detecting context or external state management libraries.

        # Using Context for State
        if re.search(r"\buseContext\b", content):
            skills.append("react/context_state")

        # React Router Basics, Dynamic Routing, Nested Routes
        if re.search(r"from\s+\'react-router-dom\'", content) or re.search(
            r'from\s+"react-router-dom"', content
        ):
            skills.append("react/router_basic")
            # Further analysis can be required to distinguish between basic, dynamic, and nested routing.

        # CSS in React
        if re.search(r"style\s*=\s*\{", content):
            skills.append("react/css_in_react")

        # Styled Components
        if re.search(r"styled\.\w+\s*\`", content):
            skills.append("react/styled_comp")

        # CSS Modules
        if re.search(r"import\s.*\sfrom\s.*\.module\.css", content):
            skills.append("react/css_modules")

        # Memoization with useMemo
        if re.search(r"\buseMemo\b", content):
            skills.append("react/memoization")

        # Virtual DOM and Reconciliation
        # Note: This is more of a conceptual understanding and might not be directly detectable from code.

        # Lazy Loading Components
        if re.search(r"React\.lazy", content):
            skills.append("react/lazy_loading")

        # Unit Testing with Jest
        # Note: This would typically involve checking for Jest configurations or import statements.

        # Testing Components with React Testing Library
        # Note: Look for imports from '@testing-library/react'.

        # End-to-End Testing Strategies
        # Note: Detection would involve recognizing E2E testing frameworks like Cypress.

        # Using Create React App
        # Note: Typically involves inspecting build scripts or project configuration.

        # Understanding Webpack and Babel
        # Note: This would typically involve checking configuration files or specific Webpack/Babel usage in the project.

        # Navigating the React DevTools
        # Note: This is more of a usage skill and not directly detectable from code.

        return list(set(skills))

    def __parse_java_skill(self, content):
        skills = []

        # Identifier
        if re.search(r"\b[a-zA-Z_$][a-zA-Z\d_$]*\b", content):
            skills.append("java/identifier")

        # Data Types
        data_types_pattern = (
            r"\b(int|String|float|double|boolean|char|long|short|byte)\b"
        )
        if re.search(data_types_pattern, content):
            skills.append("java/data_types")

        # Operators
        if re.search(
            r"[+\-*\/%]|[\+\-]=|==|!=|>|<|>=|<=|&&|\|\||!|>>=|<<=|>>>|<<<|\^=|\|=|&=",
            content,
        ):
            skills.append("java/operators")

        # Booleans
        if re.search(r"\b(true|false)\b", content):
            skills.append("java/booleans")

        # Variables
        if re.search(
            r"\b(int|String|float|double|boolean|char|long|short|byte)\s+\w+\s*=",
            content,
        ):
            skills.append("java/variables")

        # If...Else
        if re.search(r"\bif\s*\(.*?\)\s*\{.*?\}|\belse\s*\{", content, re.DOTALL):
            skills.append("java/if_else")

        # Switch
        if re.search(r"\bswitch\s*\(.*?\)\s*\{", content):
            skills.append("java/switch")

        # For Loop
        if re.search(r"\bfor\s*\(.*?;.*?;.*?\)\s*\{", content, re.DOTALL):
            skills.append("java/for_loop")

        # While Loop
        if re.search(r"\bwhile\s*\(.*?\)\s*\{", content):
            skills.append("java/while_loop")

        # Break/Continue
        if re.search(r"\b(break|continue);", content):
            skills.append("java/break_continue")

        # Comments
        if re.search(r"//.*?$|/\*[\s\S]*?\*/", content, re.MULTILINE):
            skills.append("java/comments")

        # Output (System.out.println or System.out.print)
        if re.search(r"System\.out\.(println|print)\(.*?\)", content):
            skills.append("java/output")

        # Type Casting
        if re.search(
            r"\(\s*(int|String|float|double|boolean|char|long|short|byte)\s*\)", content
        ):
            skills.append("java/type_casting")

        # Math
        if re.search(r"\bMath\.", content):
            skills.append("java/math")

        # Strings
        if re.search(r'".*?"', content):
            skills.append("java/strings")

        # StringBuffer/StringBuilder
        if re.search(r"\b(StringBuffer|StringBuilder)\b", content):
            skills.append("java/stringbuffer_stringbuilder")

        # RegEx
        if re.search(r"\bPattern\b|\bMatcher\b", content):
            skills.append("java/regex")

        # Arrays
        if re.search(r"\b\w+\[\]\s+\w+", content):
            skills.append("java/arrays")

        # Arrays Methods
        if re.search(
            r"\b(Arrays\.(sort|binarySearch|equals|fill|toString|copyOf|copyOfRange))\b",
            content,
        ):
            skills.append("java/arrays_methods")

        # Sorting
        if re.search(r"\b(Arrays\.sort|Collections\.sort)\b", content):
            skills.append("java/sorting")

        # Collections Methods
        if re.search(
            r"\b(Collections\.(sort|binarySearch|reverse|shuffle|max|min))\b", content
        ):
            skills.append("java/collections_methods")

        # Classes/Objects
        if re.search(r"\bclass\s+\w+", content):
            skills.append("java/classes_objects")

        # Class Attributes
        # Note: This is a rough approximation, might include variables outside class scope
        if re.search(
            r"\b(private|protected|public|static|final)\s+\w+\s+\w+;", content
        ):
            skills.append("java/class_attributes")

        # Class Methods
        # Note: This is a rough approximation, might include methods outside class scope
        if re.search(
            r"\b(private|protected|public|static|final)\s+\w+\s+\w+\(.*?\)\s*\{",
            content,
        ):
            skills.append("java/class_methods")

        # Constructors
        if re.search(r"\bpublic\s+\w+\(.*?\)\s*\{", content):
            skills.append("java/constructors")

        # Modifiers
        if re.search(
            r"\b(public|protected|private|static|final|abstract|synchronized|volatile|transient|native|strictfp)\b",
            content,
        ):
            skills.append("java/modifiers")

        # Packages / API
        # Note: This is a broad category and might require more specific patterns
        if re.search(r"\bimport\s+\w+(\.\w+)*;", content):
            skills.append("java/packages_api")

        # User Input (Scanner class usage)
        if re.search(r"\bScanner\b", content):
            skills.append("java/user_input")

        # Date
        if re.search(r"\bDate\b|\bCalendar\b|\bLocalDate\b|\bLocalDateTime\b", content):
            skills.append("java/date")

        # OOP Concepts (Inheritance, Polymorphism, Encapsulation, Abstraction)
        # Note: Accurately identifying these concepts requires more than regex matching.
        #       The following are very basic and may not cover all cases.
        if re.search(r"\bextends\b", content):
            skills.append("java/inheritance")
        if re.search(r"\boverride\b", content):
            skills.append("java/polymorphism")
        if re.search(r"\bprivate\s+\w+", content):
            skills.append("java/encapsulation")
        # Abstraction is difficult to detect via regex alone

        # Interface
        if re.search(r"\binterface\b", content):
            skills.append("java/interface")

        # Enums
        if re.search(r"\benum\b", content):
            skills.append("java/enums")

        # Exceptions
        if re.search(r"\btry\s*\{.*?\}\s*catch\s*\(.*?\)\s*\{", content, re.DOTALL):
            skills.append("java/exceptions")

        # Wrapper Classes
        if re.search(
            r"\b(Integer|Float|Double|Boolean|Character|Long|Short|Byte)\b", content
        ):
            skills.append("java/wrapper_classes")

        # ArrayList
        if re.search(r"\bArrayList\b", content):
            skills.append("java/arraylist")

        # LinkedList
        if re.search(r"\bLinkedList\b", content):
            skills.append("java/linkedlist")

        # HashMap
        if re.search(r"\bHashMap\b", content):
            skills.append("java/hashmap")

        # HashSet
        if re.search(r"\bHashSet\b", content):
            skills.append("java/hashset")

        # Iterator
        if re.search(r"\bIterator\b", content):
            skills.append("java/iterator")

        # Inner Classes
        if re.search(r"class\s+\w+\s*\{.*?class\s+\w+", content, re.DOTALL):
            skills.append("java/inner_classes")

        # Annotation
        if re.search(r"@\w+", content):
            skills.append("java/annotation")

        # Generics
        if re.search(r"\b\w+<\w+>", content):
            skills.append("java/generics")

        # Format
        # Note: This is a broad category and might require more specific patterns
        if re.search(r"String\.format|System\.out\.printf", content):
            skills.append("java/format")

        # Reflect
        if re.search(r"\bjava\.lang\.reflect\b", content):
            skills.append("java/reflect")

        # Serialization
        if re.search(r"\bimplements Serializable\b", content):
            skills.append("java/serialization")

        # Method Overloading (尝试匹配可能的方法重载情况)
        # 这个正则表达式查找相同类中的相同方法名但参数不同的情况
        # 注意：这可能不会完全准确，因为它依赖于方法的命名和格式化
        method_pattern = (
            r"(public|private|protected)?\s+(static)?\s*\w+\s+(\w+)\s*\((.*?)\)\s*\{"
        )
        methods = re.findall(method_pattern, content)
        method_names = {}

        for access, static, name, args in methods:
            args_count = len(args.split(","))
            if name not in method_names:
                method_names[name] = {args_count}
            else:
                method_names[name].add(args_count)

        for name, arg_counts in method_names.items():
            if len(arg_counts) > 1:
                skills.append("java/method_overloading")
                break

        # Note: Difficult to accurately identify with regex
        # Method Overriding (可能需要更复杂的逻辑来确定是否真的是方法覆盖)
        # 这里的正则表达式仅尝试匹配可能表示覆盖的方法声明
        if re.search(r"@Override\s+public\s+\w+\s+\w+\(.*?\)", content):
            skills.append("java/method_overriding")

        # Recursion (递归通常表现为函数内部调用自己)
        if re.search(r"\b(\w+)\s*\([^)]*\)\s*\{[^}]*\1\s*\(", content):
            skills.append("java/recursion")

        # Scope (捕获不同类型的作用域声明，如局部变量、循环内变量等)
        if re.search(
            r"\bfor\s*\(|\bwhile\s*\(|\bif\s*\(|\{[^}]*\bint\b|\{[^}]*\bString\b",
            content,
        ):
            skills.append("java/scope")

        # Lambda (匹配 Lambda 表达式的基本模式)
        if re.search(r"\([^)]*\)\s*->", content):
            skills.append("java/lambda")

        # Files (匹配文件操作相关的类或方法)
        if re.search(
            r"\bFile\b|\bFileReader\b|\bFileWriter\b|\bFileInputStream\b|\bFileOutputStream\b",
            content,
        ):
            skills.append("java/files")

        # Create/Write Files (检查文件创建和写入相关的代码)
        if re.search(r"new\s+FileOutputStream|new\s+FileWriter", content):
            skills.append("java/create_write_files")

        # Read Files (匹配文件读取相关的代码)
        if re.search(r"new\s+FileInputStream|new\s+FileReader", content):
            skills.append("java/read_files")

        # Delete Files (匹配文件删除的代码)
        if re.search(r"\.delete\(\)", content):
            skills.append("java/delete_files")

        # IO (捕获输入输出流相关的代码)
        if re.search(
            r"\bInputStream\b|\bOutputStream\b|\bReader\b|\bWriter\b", content
        ):
            skills.append("java/io")

        # Stream (流相关的操作)
        if re.search(r"\.stream\(\)|\.parallelStream\(\)", content):
            skills.append("java/stream")

        # NIO (新输入输出，java.nio 包的使用)
        if re.search(r"\bjava\.nio\b", content):
            skills.append("java/nio")

        # XML/Dom4j (匹配 XML 或 Dom4j 相关的代码)
        if re.search(r"\bDocument\b|\bElement\b|\bSAXReader\b", content):
            skills.append("java/xml_dom4j")

        # Math Methods (数学函数和操作)
        if re.search(r"\bMath\.\w+\(", content):
            skills.append("java/math_methods")

        # Object Methods (匹配常用的 Object 类方法)
        if re.search(r"\bequals\(|\bhashCode\(|\btoString\(", content):
            skills.append("java/object_methods")

        # String Methods (字符串操作的方法)
        if re.search(
            r"\bString\s+\w+\s*=|\b\w+\.length\(\)|\b\w+\.charAt\(|\b\w+\.substring\(",
            content,
        ):
            skills.append("java/string_methods")

        # System Methods (System 类相关的方法调用)
        if re.search(r"\bSystem\.out\.print|System\.in|System\.exit\(", content):
            skills.append("java/system_methods")

        # Threads (线程相关的代码)
        if re.search(r"\bThread\b|\bRunnable\b|\bstart\(\)", content):
            skills.append("java/threads")

        # Working (可能是关于多线程或并发的工作，但这需要更明确的上下文来确定)
        # 这里简单匹配线程和并发相关的关键字
        if re.search(r"\bThread\b|\bRunnable\b|\bExecutorService\b", content):
            skills.append("java/working")

        # Net (网络编程相关的代码)
        if re.search(r"\bSocket\b|\bServerSocket\b|\bURLConnection\b", content):
            skills.append("java/net")

        # OOP Concepts
        if re.search(r"\bclass\b|\bextends\b|\bimplements\b|\bnew\b", content):
            skills.append("java/oop")

        # Abstraction
        if re.search(r"\babstract class\b|\binterface\b", content):
            skills.append("java/abstraction")

        # 这里可以继续添加其他技能点的匹配规则

        return list(set(skills))

    def __parse_mysql_skill(self, content):
        skills = []
        # mysql/select
        if "SELECT " in content:
            skills.append("mysql/select")
        # mysql/insert
        if "INSERT " in content:
            skills.append("mysql/insert")
        # mysql/update
        if "UPDATE " in content:
            skills.append("mysql/update")
        # mysql/delete
        if "DELETE " in content:
            skills.append("mysql/delete")
        # mysql/create_table
        if "CREATE TABLE " in content:
            skills.append("mysql/create_table")
        # mysql/drop_table
        if "DROP TABLE " in content:
            skills.append("mysql/drop_table")
        # mysql/alter_table
        if "ALTER TABLE " in content:
            skills.append("mysql/alter_table")
        # mysql/load_data
        if "LOAD DATA " in content:
            skills.append("mysql/load_data")
        # mysql/rename
        if "RENAME " in content:
            skills.append("mysql/rename")
        # mysql/source
        if "SOURCE " in content:
            skills.append("mysql/source")
        # mysql/use_database
        if "USE " in content:
            skills.append("mysql/use_database")
        # mysql/create_database
        if "CREATE DATABASE " in content:
            skills.append("mysql/create_database")
        # mysql/drop_database
        if "DROP DATABASE " in content:
            skills.append("mysql/drop_database")
        # mysql/database
        if "DATABASE " in content:
            skills.append("mysql/database")
        # mysql/user
        if "USER " in content:
            skills.append("mysql/user")
        # mysql/version
        if "VERSION " in content:
            skills.append("mysql/version")
        # mysql/int
        if "INT " in content:
            skills.append("mysql/int")
        # mysql/varchar
        if "VARCHAR " in content:
            skills.append("mysql/varchar")
        # mysql/date
        if "DATE " in content:
            skills.append("mysql/date")
        # mysql/float
        if "FLOAT " in content:
            skills.append("mysql/float")
        # mysql/boolean
        if "BOOLEAN " in content:
            skills.append("mysql/boolean")
        # mysql/index
        if "INDEX " in content:
            skills.append("mysql/index")
        # mysql/explain_query
        if "EXPLAIN " in content:
            skills.append("mysql/explain_query")
        # mysql/begin_transaction
        if "BEGIN " in content:
            skills.append("mysql/begin_transaction")
        # mysql/commit
        if "COMMIT " in content:
            skills.append("mysql/commit")
        # mysql/rollback
        if "ROLLBACK " in content:
            skills.append("mysql/rollback")
        # mysql/identified_by
        if "IDENTIFIED BY " in content:
            skills.append("mysql/identified_by")
        # mysql/grant_permission
        if "GRANT " in content:
            skills.append("mysql/grant_permission")
        # mysql/revoke_permission
        if "REVOKE " in content:
            skills.append("mysql/revoke_permission")
        # mysql/show_status
        if "SHOW STATUS " in content:
            skills.append("mysql/show_status")
        # mysql/show_variables
        if "SHOW VARIABLES " in content:
            skills.append("mysql/show_variables")
        # mysql/mysqladmin
        if "mysqladmin" in content:
            skills.append("mysql/mysqladmin")
        # mysql/mysqldump
        if "mysqldump" in content:
            skills.append("mysql/mysqldump")
        # mysql/mysqlimport
        if "mysqlimport" in content:
            skills.append("mysql/mysqlimport")
        # mysql/secure_file_priv
        if "secure_file_priv" in content:
            skills.append("mysql/secure_file_priv")
        # mysql/stored_procedures
        if "CREATE PROCEDURE " in content:
            skills.append("mysql/stored_procedures")
        # mysql/triggers
        if "CREATE TRIGGER " in content:
            skills.append("mysql/triggers")
        # mysql/views
        if "CREATE VIEW " in content:
            skills.append("mysql/views")
        return list(set(skills))

    def __parse_pandas_skill(self, content):
        skills = []

        # Read CSV
        if re.search(r"\.read_csv\(", content):
            skills.append("pandas/read_csv")

        # Read Excel
        if re.search(r"\.read_excel\(", content):
            skills.append("pandas/read_excel")

        # Read from SQL
        if re.search(r"\.read_sql\(", content):
            skills.append("pandas/read_sql")

        # Write to CSV
        if re.search(r"\.to_csv\(", content):
            skills.append("pandas/write_csv")

        # Write to Excel
        if re.search(r"\.to_excel\(", content):
            skills.append("pandas/write_excel")

        # Write to SQL
        if re.search(r"\.to_sql\(", content):
            skills.append("pandas/write_sql")

        # Select Columns
        if (
            re.search(r"\[[\"'].*[\"']\]", content)
            or re.search(r"\.loc\[", content)
            or re.search(r"\.iloc\[", content)
        ):
            skills.append("pandas/select_columns")

        # Select Rows
        if re.search(r"\.loc\[", content) or re.search(r"\.iloc\[", content):
            skills.append("pandas/select_rows")

        # Conditional Selection
        if re.search(r"\[.*\]", content) and re.search(
            r"==|!=|>|<|>=|<=| in | not in ", content
        ):
            skills.append("pandas/conditional_selection")

        # Slicing
        if re.search(r"\.loc\[.*:.*\]", content) or re.search(
            r"\.iloc\[.*:.*\]", content
        ):
            skills.append("pandas/slicing")

        # Adding New Columns
        if re.search(r"\['\w+'\]\s*=\s*", content):
            skills.append("pandas/add_new_columns")

        # Dropping Columns/Rows
        if re.search(r"\.drop\(", content):
            skills.append("pandas/drop_columns_rows")

        # Changing Data Types
        if re.search(r"\.astype\(", content):
            skills.append("pandas/change_data_types")

        # Sorting Data
        if re.search(r"\.sort_values\(", content) or re.search(
            r"\.sort_index\(", content
        ):
            skills.append("pandas/sort_data")

        # Handling Missing Values
        if re.search(r"\.fillna\(", content) or re.search(r"\.dropna\(", content):
            skills.append("pandas/handle_missing_values")

        # Removing Duplicates
        if re.search(r"\.drop_duplicates\(", content):
            skills.append("pandas/remove_duplicates")

        # Data Normalization
        # 此项可能需要根据具体使用场景进行判断，因为数据规范化方法可能多样

        # Data Mapping
        if re.search(r"\.map\(", content) or re.search(r"\.apply\(", content):
            skills.append("pandas/data_mapping")

        # Basic Statistics
        if (
            re.search(r"\.mean\(", content)
            or re.search(r"\.median\(", content)
            or re.search(r"\.sum\(", content)
            or re.search(r"\.count\(", content)
        ):
            skills.append("pandas/basic_statistics")

        # GroupBy Operations
        if re.search(r"\.groupby\(", content):
            skills.append("pandas/groupby_operations")

        # Data Aggregation
        if re.search(r"\.agg\(", content) or re.search(r"\.aggregate\(", content):
            skills.append("pandas/data_aggregation")

        # Pivot Tables
        if re.search(r"\.pivot_table\(", content):
            skills.append("pandas/pivot_tables")

        # Data Normalization
        if re.search(r"(\.min\(\)|\.max\(\)|\.mean\(\))", content) and re.search(
            r"\.apply\(", content
        ):
            skills.append("pandas/data_normalization")

        # Bar Plots
        if re.search(r"\.plot\(\s*kind\s*=\s*['\"]bar['\"]", content) or re.search(
            r"\.bar\(", content
        ):
            skills.append("pandas/bar_plots")

        # Histograms
        if re.search(r"\.hist\(", content) or re.search(
            r"\.plot\(\s*kind\s*=\s*['\"]hist['\"]", content
        ):
            skills.append("pandas/histograms")

        # Scatter Plots
        if re.search(r"\.plot\(\s*kind\s*=\s*['\"]scatter['\"]", content) or re.search(
            r"\.scatter\(", content
        ):
            skills.append("pandas/scatter_plots")

        # Line Plots
        if re.search(r"\.plot(\(\s*kind\s*=\s*['\"]line['\"])?", content) or re.search(
            r"\.line\(", content
        ):
            skills.append("pandas/line_plots")

        # Time Series Analysis
        if (
            re.search(r"\.resample\(", content)
            or re.search(r"\.asfreq\(", content)
            or re.search(r"\.rolling\(", content)
        ):
            skills.append("pandas/time_series_analysis")

        # MultiIndex Indexing
        if re.search(r"\.MultiIndex\(", content):
            skills.append("pandas/multiindex_indexing")

        # Merging Data
        if re.search(r"\.merge\(", content) or re.search(r"\.join\(", content):
            skills.append("pandas/merge_data")

        # Reshaping Data
        if (
            re.search(r"\.melt\(", content)
            or re.search(r"\.pivot\(", content)
            or re.search(r"\.stack\(", content)
            or re.search(r"\.unstack\(", content)
        ):
            skills.append("pandas/reshape_data")

        return list(set(skills))

    def __parse_matplotlib_skill(self, content):
        skills = []

        # Basic Concepts
        if re.search(r"(import matplotlib|from matplotlib import)", content):
            skills.append("matplotlib/importing_matplotlib")
        if re.search(
            r"matplotlib\.(figure|pyplot|axes)|from matplotlib\.figure import|from matplotlib\.pyplot import|from matplotlib\.axes import",
            content,
            re.IGNORECASE,
        ):
            skills.append("matplotlib/figures_axes")
        if re.search(r"figure\(\s*size\s*=", content):
            skills.append("matplotlib/figure_size_dpi")
        if re.search(r"savefig\(", content):
            skills.append("matplotlib/saving_figures")

        # Plotting Data
        if re.search(r"\.plot\(", content):
            skills.append("matplotlib/line_plots")
        if re.search(r"\.scatter\(", content):
            skills.append("matplotlib/scatter_plots")
        if re.search(r"\.bar\(", content):
            skills.append("matplotlib/bar_charts")
        if re.search(r"\.hist\(", content):
            skills.append("matplotlib/histograms")
        if re.search(r"\.boxplot\(", content):
            skills.append("matplotlib/box_plots")
        if re.search(r"(\.imshow\(|heatmap)", content):
            skills.append("matplotlib/heatmaps")
        if re.search(r"\.errorbar\(", content):
            skills.append("matplotlib/error_bars")
        if re.search(r"\.stackplot\(", content):
            skills.append("matplotlib/stacked_plots")
        if re.search(r"\.fill_between\(", content):
            skills.append("matplotlib/fill_between")

        # Advanced Plotting
        if re.search(r"\.subplot\(", content):
            skills.append("matplotlib/subplots")
        if re.search(r"\.(twinx\(|twiny\()", content):
            skills.append("matplotlib/secondary_axis")
        if re.search(r"\.set_yscale\(['\"]log['\"]\)", content) or re.search(
            r"\.set_xscale\(['\"]log['\"]\)", content
        ):
            skills.append("matplotlib/log_scale")
        if re.search(r"\.polar\(", content):
            skills.append("matplotlib/polar_charts")
        if re.search(r"\.plot_surface\(", content) or re.search(
            r"\.plot_wireframe\(", content
        ):
            skills.append("matplotlib/3d_plots")

        # Plot Customization
        if re.search(r"\.setp\(", content) or re.search(
            r"(linestyle|linecolor)", content
        ):
            skills.append("matplotlib/line_styles_colors")
        if re.search(r"(\.title\(|\.xlabel\(|\.ylabel\()", content):
            skills.append("matplotlib/titles_labels")
        if re.search(r"\.legend\(", content):
            skills.append("matplotlib/legend_config")
        if re.search(r"(\.xticks\(|\.yticks\()", content):
            skills.append("matplotlib/axis_ticks")
        if re.search(r"\.grid\(", content):
            skills.append("matplotlib/grid_config")
        if re.search(r"\.annotate\(", content):
            skills.append("matplotlib/text_annotations")
        if re.search(r"\.table\(", content):
            skills.append("matplotlib/adding_tables")

        # Specialized Plots
        if re.search(r"\.pie\(", content):
            skills.append("matplotlib/pie_charts")
        if re.search(r"\.bubble\(", content):
            skills.append("matplotlib/bubble_charts")
        if re.search(r"\.violinplot\(", content):
            skills.append("matplotlib/violin_plots")
        if re.search(r"\.contour\(", content) or re.search(r"\.contourf\(", content):
            skills.append("matplotlib/contour_plots")
        if re.search(r"\.quiver\(", content):
            skills.append("matplotlib/quiver_plots")
        if re.search(r"\.streamplot\(", content):
            skills.append("matplotlib/stream_plots")

        # Interactive Features
        if "interactive" in content or re.search(r"matplotlib\.widgets", content):
            skills.append("matplotlib/interactive_backends")
        if re.search(r"(widgets|slider)", content):
            skills.append("matplotlib/widgets_sliders")

        # Advanced Topics
        if "backend" in content or re.search(r"matplotlib\.backends", content):
            skills.append("matplotlib/custom_backends")
        if "animation" in content or re.search(r"matplotlib\.animation", content):
            skills.append("matplotlib/animation_creation")
        if re.search(r"(event|connect\()", content):
            skills.append("matplotlib/event_handling")

        # Matplotlib Configurations
        if "rcParams" in content or re.search(r"matplotlib\.rc", content):
            skills.append("matplotlib/matplotlib_config")

        return list(set(skills))

    def __parse_numpy_skill(self, content):
        skills = []

        # Array Basics
        if re.search(r"np\.array\(\[[^\[\]]*\]\)", content):  # Matches 1D arrays
            skills.append("numpy/1d_array")
        # Matches multi-dimensional arrays
        if re.search(r"np\.array\(\[\[", content):
            skills.append("numpy/multi_array")
        if re.search(
            r"np\.array\(", content
        ):  # General array creation, could be 1D or multi-dimensional
            skills.append("numpy/data_array")
        if re.search(r"\.shape\b", content):
            skills.append("numpy/shape_dim")
        if re.search(r"\.dtype\b", content):
            skills.append("numpy/data_type")
        if re.search(r"\.(ndim|size|itemsize|nbytes)\b", content):
            skills.append("numpy/attr")

        # Indexing and Slicing
        if re.search(r"\[\s*\d+\s*\]", content):  # Basic indexing
            skills.append("numpy/basic_idx")
        if re.search(r"\[\s*:\s*\]", content):  # Slicing
            skills.append("numpy/slice")
        if re.search(r"\[.*?\]", content):  # Boolean or fancy indexing
            skills.append("numpy/bool_idx")
            skills.append("numpy/fancy_idx")

        # Array Manipulation
        if re.search(r"np\.reshape|\.reshape\b", content):
            skills.append("numpy/reshape")
        if re.search(r"np\.transpose|\.T\b", content):
            skills.append("numpy/transpose")
        if re.search(r"np\.(concatenate|stack|vstack|hstack)\b", content):
            skills.append("numpy/merge")
        if re.search(r"np\.(split|vsplit|hsplit)\b", content):
            skills.append("numpy/split")
        if re.search(r"np\.(tile|repeat)\b", content):
            skills.append("numpy/expand")

        # Math and Statistics
        if re.search(
            r"np\.(sum|mean|median|max|min|std|var|add|subtract|multiply|divide)\b",
            content,
        ):
            skills.append("numpy/math_ops")
        if re.search(r"np\.linalg\.", content):  # Linear algebra
            skills.append("numpy/lin_alg")
        if re.search(r"np\.random\.", content):  # Random numbers
            skills.append("numpy/rand_num")
        # Adding specific patterns for statistical analysis
        if re.search(r"np\.(sum|mean|median|max|min|std|var)\b", content):
            skills.append("numpy/stats")

        # Advanced Features
        if re.search(
            r"np\.broadcast", content
        ):  # Broadcasting, tricky to match precisely
            skills.append("numpy/broadcast")
        if re.search(
            r"np\.(sort|argsort|searchsorted|where)\b", content
        ):  # Sort and search
            skills.append("numpy/sort_search")
        if re.search(
            r"np\.ufunc", content
        ):  # Universal functions, tricky to match precisely
            skills.append("numpy/ufuncs")

        # File Input/Output
        if re.search(r"np\.(loadtxt|savetxt)\b", content):
            skills.append("numpy/text_io")
        if re.search(r"np\.(load|save|savez)\b", content):
            skills.append("numpy/bin_io")

        # Special Techniques
        if re.search(r"np\.(datetime64|timedelta64)\b", content):
            skills.append("numpy/datetime")
        if re.search(r"np\.ma\.", content):  # Masked arrays
            skills.append("numpy/mask_array")
        if re.search(r"np\.dtype\(\[", content):  # Structured arrays
            skills.append("numpy/struct_array")

        return list(set(skills))

    def __parse_sql_skill(self, content):
        skills = []

        # Basic SQL Commands
        if re.search(r"\bSELECT\b", content, re.IGNORECASE):
            skills.append("sql/select")
        if re.search(r"\bINSERT INTO\b", content, re.IGNORECASE):
            skills.append("sql/insert")
        if re.search(r"\bUPDATE\b", content, re.IGNORECASE):
            skills.append("sql/update")
        if re.search(r"\bDELETE\b", content, re.IGNORECASE):
            skills.append("sql/delete")
        if re.search(r"\bCREATE TABLE\b", content, re.IGNORECASE):
            skills.append("sql/create_table")
        if re.search(r"\bALTER TABLE\b", content, re.IGNORECASE):
            skills.append("sql/alter_table")
        if re.search(r"\bDROP TABLE\b", content, re.IGNORECASE):
            skills.append("sql/drop_table")
        if re.search(r"\bTRUNCATE TABLE\b", content, re.IGNORECASE):
            skills.append("sql/truncate_table")

        # Data Manipulation and Querying
        if re.search(r"\bWHERE\b", content, re.IGNORECASE):
            skills.append("sql/where")
        if re.search(r"\bIN\b", content, re.IGNORECASE):
            skills.append("sql/in")
        if re.search(r"\bORDER BY\b", content, re.IGNORECASE):
            skills.append("sql/order_by")
        if re.search(r"\bGROUP BY\b", content, re.IGNORECASE):
            skills.append("sql/group_by")
        if re.search(r"\bHAVING\b", content, re.IGNORECASE):
            skills.append("sql/having")
        if re.search(r"\bUNION\b", content, re.IGNORECASE):
            skills.append("sql/union")
        if re.search(r"\bLIKE\b", content, re.IGNORECASE):
            skills.append("sql/like")
        if re.search(r"\bBETWEEN\b", content, re.IGNORECASE):
            skills.append("sql/between")
        if re.search(r"\b(EXISTS|NOT EXISTS)\b", content, re.IGNORECASE):
            skills.append("sql/exists")
        if re.search(r"\bSUBSELECT\b|\bSUBQUERY\b", content, re.IGNORECASE):
            skills.append("sql/subqueries")
        if re.search(r"\bMERGE\b", content, re.IGNORECASE):
            skills.append("sql/merge")
        if re.search(r"OVER\s*\(", content, re.IGNORECASE):
            skills.append("sql/window_functions")

        # Data Definition and Integrity
        if re.search(
            r"\b(INT|VARCHAR|CHAR|TEXT|DATE|TIME|DATETIME|TIMESTAMP|FLOAT|DOUBLE|DECIMAL|NUMERIC|BOOLEAN|BLOB|BINARY|VARBINARY|BIGINT|SMALLINT|TINYINT|GEOMETRY|JSON)\b",
            content,
            re.IGNORECASE,
        ):
            skills.append("sql/data_types")
        if re.search(
            r"\b(PRIMARY KEY|FOREIGN KEY|UNIQUE|CHECK|NOT NULL|DEFAULT|INDEX)\b",
            content,
            re.IGNORECASE,
        ):
            skills.append("sql/constraints")
        if re.search(r"\bNORMALIZATION\b", content, re.IGNORECASE):
            skills.append("sql/normalization")

        # Advanced Data Operations
        if re.search(r"\bJOIN\b", content, re.IGNORECASE):
            skills.append("sql/join")
        if re.search(r"\bVIEW\b", content, re.IGNORECASE):
            skills.append("sql/views")
        if re.search(r"\bPROCEDURE\b", content, re.IGNORECASE):
            skills.append("sql/stored_procedures")
        if re.search(r"\bCAST\b", content, re.IGNORECASE):
            skills.append("sql/cast")
        if re.search(r"\bCONVERT\b", content, re.IGNORECASE):
            skills.append("sql/convert")
        if re.search(
            r"\b(CONCAT|SUBSTRING|TRIM|LENGTH|LOWER|UPPER|REPLACE|LTRIM|RTRIM)\b",
            content,
            re.IGNORECASE,
        ):
            skills.append("sql/string_functions")
        if re.search(
            r"\b(SUM|AVG|COUNT|MAX|MIN|ROUND|CEIL|CEILING|FLOOR|ABS|MOD|POWER|SQRT|SIGN|LOG|EXP|ACOS|ASIN|ATAN|ATAN2|COS|SIN|TAN)\b",
            content,
            re.IGNORECASE,
        ):
            skills.append("sql/numeric_functions")
        if re.search(
            r"\b(CURDATE|CURTIME|NOW|DATE_ADD|DATE_SUB|DATEDIFF|DAY|MONTH|YEAR|HOUR|MINUTE|SECOND)\b",
            content,
            re.IGNORECASE,
        ):
            skills.append("sql/date_time_functions")

        # Database Management and Optimization
        if re.search(r"\bTRANSACTION\b", content, re.IGNORECASE):
            skills.append("sql/transaction_control")
        if re.search(r"\bGRANT\b|\bREVOKE\b", content, re.IGNORECASE):
            skills.append("sql/security_permissions")
        if re.search(r"\bINDEX\b", content, re.IGNORECASE):
            skills.append("sql/creating_indexes")
        # Detecting "using indexes" might be complex and context-dependent
        if re.search(
            r"\bINFORMATION_SCHEMA\b|\bINFORMATION_SCHEMA\.COLUMNS\b",
            content,
            re.IGNORECASE,
        ):
            skills.append("sql/information_schema")
        if re.search(r"\bEXPLAIN\b", content, re.IGNORECASE):
            skills.append("sql/explain")

        if re.search(r"\bWHERE\b|\bJOIN\b|\bORDER BY\b", content, re.IGNORECASE):
            skills.append("sql/using_indexes")

        return list(set(skills))

    def parse(self, language: str, content: str):
        if language == "python":
            return self.__parse_python_skill(content)
        elif language == "linux":
            skills_a = self.__parse_linux_skill(content)
            skills_b = self.__parse_shell_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "tkinter":
            skills_a = self.__parse_tkinter_skill(content)
            skills_b = self.__parse_python_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "sklearn":
            skills_a = self.__parse_sklearn_skill(content)
            skills_b = self.__parse_python_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "shell":
            return self.__parse_shell_skill(content)
        elif language == "rust":
            return self.__parse_rust_skill(content)
        elif language == "pygame":
            skills_a = self.__parse_pygame_skill(content)
            skills_b = self.__parse_python_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "django":
            skills_a = self.__parse_django_skill(content)
            skills_b = self.__parse_python_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "go":
            return self.__parse_go_skill(content)
        elif language == "flask":
            skills_a = self.__parse_flask_skill(content)
            skills_b = self.__parse_python_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "cpp":
            return self.__parse_cpp_skill(content)
        elif language == "c":
            return self.__parse_c_skill(content)
        elif language == "html":
            return self.__parse_html_skill(content)
        elif language == "css":
            return self.__parse_css_skill(content)
        elif language == "jquery":
            skills_a = self.__parse_jquery_skill(content)
            skills_b = self.__parse_javascript_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "javascript":
            return self.__parse_javascript_skill(content)
        elif language == "react":
            skills_a = self.__parse_react_skill(content)
            skills_b = self.__parse_javascript_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "java":
            return self.__parse_java_skill(content)
        elif language == "mysql":
            skills_a = self.__parse_mysql_skill(content)
            skills_b = self.__parse_sql_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "pandas":
            skills_a = self.__parse_pandas_skill(content)
            skills_b = self.__parse_python_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "matplotlib":
            skills_a = self.__parse_matplotlib_skill(content)
            skills_b = self.__parse_python_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "numpy":
            skills_a = self.__parse_numpy_skill(content)
            skills_b = self.__parse_python_skill(content)
            return list(set(skills_a + skills_b))
        elif language == "sql":
            return self.__parse_sql_skill(content)
