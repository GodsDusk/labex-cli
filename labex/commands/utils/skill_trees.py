import re


class ParseSkills:
    def __init__(self) -> None:
        pass

    def __parse_python_skill(self, content):
        build_in_functions = [
            "abs(",
            "enumerate(",
            "float(",
            "input(",
            "int(",
            "len(",
            "map(",
            "max(",
            "min(",
            "next(",
            "open(",
            "print(",
            "round(",
            "sorted(",
            "str(",
            "sum(",
            "zip(",
            "type(",
            "super(",
            "id(",
            "filter(",
            "ord(",
            "reversed(",
            "bytes(",
            "assert(",
            "encode(",
            "isinstance(",
            "all(",
            "bin(",
            "any(",
            "hex(",
            "divmod(",
            "chr(",
            "slice(",
            "strip(",
        ]

        librarys = [
            "re",
            "os",
            "glob",
            "argparse",
            "math",
            "datetime",
            "sys",
            "multiprocessing",
            "unittest",
            "sqlite3",
            "logging",
            "copy",
            "collections",
            "itertools",
            "typing",
            "threading",
            "time",
            "webbrowser",
            "pygame",
            "random",
            "zlib",
            "textwrap",
            "calendar",
            "functools",
            "operator",
            "enum",
            "dateutil",
            "secrets",
            "io",
            "pathlib",
            "dask",
            "tkinter",
            "ctypes",
            "requests",
            "pytz",
            "tqdm",
            "bitstring",
            "numpy",
            "pandas",
            "matplotlib",
            "flask",
            "pyarrow",
            "scipy",
            "beautifulsoup",
            "seaborn",
            "sklearn",
            "basic_units",
            "pil",
        ]

        skills = []
        # python/if_else
        if "if " in content and "else" in content:
            skills.append("python/if_else")
        # python/python_interpreter
        if "python3" in content:
            skills.append("python/python_interpreter")
        # python/python_scripts
        if ".py" in content:
            skills.append("python/python_scripts")
        # python/math_operator
        if (
            " + " in content
            or " - " in content
            or " * " in content
            or " / " in content
            or " % " in content
            or " ** " in content
            or " // " in content
        ):
            skills.append("python/math_operator")
        # python/assignment
        if " = " in content:
            skills.append("python/assignment")
        # python/variables
        if "int(" in content or "float(" in content or "str(" in content:
            skills.append("python/variables")
        # python/ipython
        if "ipython" in content:
            skills.append("python/ipython")
        # python/del
        if "del " in content:
            skills.append("python/del")
        # python/function_basic
        if "def " in content:
            skills.append("python/function_basic")
        # python/args_and_kwargs
        if "*args" in content or "**kwargs" in content:
            skills.append("python/args_and_kwargs")
        # python/lambda_function
        if "lambda " in content:
            skills.append("python/lambda_function")
        # python/local_and_global
        if "global " in content:
            skills.append("python/local_and_global")
        # python/yield_values
        if "yield " in content:
            skills.append("python/yield_values")
        # python/comparison
        if (
            " == " in content
            or " != " in content
            or " < " in content
            or " > " in content
        ):
            skills.append("python/comparison")
        # python/boolean
        if " True" in content or " False" in content:
            skills.append("python/boolean")
        # python/switch_case
        if "switch " in content and "case " in content:
            skills.append("python/switch_case")
        # python/while_loop
        if "while " in content:
            skills.append("python/while_loop")
        # python/range
        if "range(" in content:
            skills.append("python/range")
        # python/walrus
        if ":=" in content:
            skills.append("python/walrus")
        # python/data_types
        if "list(" in content or "tuple(" in content or "dict(" in content:
            skills.append("python/data_types")
        # python/list
        if "append(" in content or "pop(" in content or "remove(" in content:
            skills.append("python/list")
        # python/tuple
        if "tuple(" in content:
            skills.append("python/tuple")
        # python/dict
        if "dict(" in content:
            skills.append("python/dict")
        # python/set
        if "set(" in content:
            skills.append("python/set")
        # python/virtual_environments
        if "virtualenv" in content:
            skills.append("python/virtual_environments")
        # python/pypi
        if "pip install " in content:
            skills.append("python/pypi")
        # python/conda
        if "conda install " in content:
            skills.append("python/conda")
        # python/try_except
        if "try:" in content and "except" in content:
            skills.append("python/try_except")
        # python/syntax_errors
        if "SyntaxError" in content:
            skills.append("python/syntax_errors")
        # python/raise_errors
        if "raise " in content:
            skills.append("python/raise_errors")
        # python/class
        if "class " in content:
            skills.append("python/class")
        # python/attributes
        if "self." in content:
            skills.append("python/attributes")
        # python/inheritance
        if "super(" in content:
            skills.append("python/inheritance")

        for function in build_in_functions:
            if function in content:
                skills.append(f"python/{function[:-1]}")
        for library in librarys:
            if f"import {library}" in content or f"from {library}" in content:
                skills.append(f"python/{library}")

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
        # shell/if_else
        if "if" in content and "else" in content:
            skills.append("shell/if_else")
        # shell/case_esac
        if "case" in content and "esac" in content:
            skills.append("shell/case_esac")
        # shell/while_loop
        if "while" in content:
            skills.append("shell/while_loop")
        # shell/break
        if "break" in content:
            skills.append("shell/break")
        # shell/for_loop
        if "for" in content:
            skills.append("shell/for_loop")
        # shell/function_return_values
        if "return" in content:
            skills.append("shell/function_return_values")
        # shell/function_basic
        if "function" in content:
            skills.append("shell/function_basic")
        # shell/function_arguments
        if "$1" in content:
            skills.append("shell/function_arguments")
        # shell/variable_substitution
        if "${" in content:
            skills.append("shell/variable_substitution")
        # shell/string_operator
        if "==" in content or "!=" in content:
            skills.append("shell/string_operator")
        # shell/boolean_operator
        if "&&" in content or "||" in content:
            skills.append("shell/boolean_operator")
        # shell/file_test_operator
        if "-f" in content or "-d" in content:
            skills.append("shell/file_test_operator")
        # shell/relational_operator
        if "-eq" in content or "-ne" in content:
            skills.append("shell/relational_operator")
        # shell/arithmetic_operator
        if "$((" in content:
            skills.append("shell/arithmetic_operator")
        # shell/local_variables
        if "local" in content:
            skills.append("shell/local_variables")
        # shell/special_variables
        if "$#" in content:
            skills.append("shell/special_variables")
        # shell/input_redirection
        if " < " in content:
            skills.append("shell/input_redirection")
        # shell/output_redirection
        if " > " in content:
            skills.append("shell/output_redirection")

        return list(set(skills))

    def __parse_rust_skill(self, content):
        build_in_functions = [
            "never",
            "array",
            "bool",
            "char",
            "f32",
            "f64",
            "fn",
            "i8",
            "i16",
            "i32",
            "i64",
            "i128",
            "isize",
            "pointer",
            "reference",
            "slice",
            "tuple",
            "u8",
            "u16",
            "u32",
            "u64",
            "u128",
            "unit",
            "usize",
            "assert_matches",
            "async_iter",
            "intrinsics",
            "simd",
            "alloc",
            "any",
            "arch",
            "ascii",
            "backtrace",
            "borrow",
            "boxed",
            "cell",
            "clone",
            "cmp",
            "collections",
            "convert",
            "default",
            "env",
            "error",
            "ffi",
            "fmt",
            "fs",
            "future",
            "hash",
            "hint",
            "io",
            "iter",
            "marker",
            "mem",
            "net",
            "num",
            "ops",
            "option",
            "os",
            "panic",
            "path",
            "pin",
            "prelude",
            "primitive",
            "process",
            "ptr",
            "rc",
            "result",
            "string",
            "sync",
            "task",
            "thread",
            "time",
            "vec",
            "concat_bytes",
            "concat_idents",
            "const_format_args",
            "format_args_nl",
            "log_syntax",
            "trace_macros",
            "assert",
            "assert_eq",
            "assert_ne",
            "cfg",
            "column",
            "compile_error",
            "concat",
            "dbg",
            "debug_assert",
            "debug_assert_eq",
            "debug_assert_ne",
            "eprint",
            "eprintln",
            "format",
            "format_args",
            "include",
            "include_bytes",
            "include_str",
            "x86_64",
            "line",
            "matches",
            "module_path",
            "option_env",
            "print",
            "println",
            "stringify",
            "thread_local",
            "todo",
            "trydeprecated",
            "unimplemented",
            "unreachable",
            "write",
            "writeln",
            "selfty",
            "async",
            "await",
            "break",
            "const",
            "continue",
            "crate",
            "dyn",
            "else",
            "enum",
            "extern",
            "false",
            "for",
            "if",
            "impl",
            "let",
            "loop",
            "match",
            "mod",
            "move",
            "mut",
            "pub",
            "ref",
            "return",
            "self",
            "static",
            "struct",
            "super",
            "trait",
            "true",
            "type",
            "union",
            "unsafe",
            "use",
            "where",
            "while",
            "rustc",
            "rustup",
        ]
        skills = []
        for function in build_in_functions:
            if f".{function}" in content:
                skills.append(f"rust/{function.lower()}")
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
        # django/django_utils
        if "django.utils" in content:
            skills.append("django/django_utils")
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
                    skill_function = line.split(".")[1].strip().replace(")", "")
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
        # css/pseudo-classes
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
            skills.append("css/pseudo-classes")
        # css/pseudo-elements
        if "::" in content:
            skills.append("css/pseudo-elements")
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
        slugs = {
            "children": "children",
            "parent": "parent",
            "siblings": "siblings",
            "append": "append",
            "addClass": "add_class",
            "remove": "remove",
            "removeClass": "remove_class",
            "attr": "attr",
            "html": "html",
            "text": "text",
            "css": "css",
            "show": "show",
            "fadeOut": "fade_out",
            "hide": "hide",
            "bind": "bind",
            "on": "on",
            "appendTo": "append_to",
            "mouseover": "mouseover",
            "toggle": "toggle",
            "fadeIn": "fade_in",
        }

        skills = []
        for slug in slugs:
            if f".{slug}(" in content:
                skills.append(f"jquery/{slugs[slug]}")

        return list(set(skills))

    def __parse_javascript_skill(self, content):
        skills = []
        document_group = {
            "appendChild": "append_child",
            "classList": "class_list",
            "createElement": "create_element",
            "getElementById": "get_element_by_id",
            "innerText": "inner_text",
            "querySelector": "query_selector",
            "querySelectorAll": "query_selector_all",
            "removeChild": "remove_child",
        }
        for slug in document_group:
            if f"document.{slug}(" in content:
                skills.append(f"js/{document_group[slug]}")
        date_method_group = {
            "getDate": "get_date",
            "getDay": "get_day",
            "getFullYear": "get_full_year",
            "getMonth": "get_month",
            "getSeconds": "get_seconds",
            "getTime": "get_time",
            "getTimezoneOffset": "get_time_zone_offset",
            "setDate": "set_date",
            "toISOString": "to_iso_string",
            "toLocaleDateString": "to_locale_date_string",
            "toTimeString": "to_time_string",
        }
        for slug in date_method_group:
            if f".{slug}(" in content:
                skills.append(f"js/{date_method_group[slug]}")
        object_method_group = {
            "assign": "obj_assign",
            "constructor": "obj_constructor",
            "create": "obj_create",
            "entries": "obj_entries",
            "getPrototypeOf": "obj_get_prototype_of",
            "keys": "obj_keys",
            "values": "obj_values",
            "freeze": "freeze",
            "fromEntries": "from_entries",
            "hasOwnProperty": "has_own_property",
            "isFrozen": "is_frozen",
        }
        for slug in object_method_group:
            if f"Object.{slug}(" in content or f".{slug}(" in content:
                skills.append(f"js/{object_method_group[slug]}")
        math_method_group = {
            "PI": "pi",
            "abs": "abs",
            "acos": "acos",
            "ceil": "ceil",
            "cos": "cos",
            "floor": "floor",
            "hypot": "hypot",
            "log": "log",
            "log10": "log10",
            "max": "max",
            "min": "min",
            "pow": "pow",
            "random": "random",
            "round": "round",
            "sign": "sign",
            "sqrt": "sqrt",
        }
        for slug in math_method_group:
            if f"Math.{slug}(" in content:
                skills.append(f"js/{math_method_group[slug]}")
        array_method_group = {
            "concat": "arr_concat",
            "every": "arr_every",
            "fill": "arr_fill",
            "filter": "arr_filter",
            "find": "arr_find",
            "findIndex": "arr_find_index",
            "forEach": "arr_for_each",
            "from": "arr_from",
            "includes": "arr_includes",
            "indexOf": "arr_index_of",
            "join": "arr_join",
            "length": "arr_length",
            "map": "arr_map",
            "pop": "arr_pop",
            "push": "arr_push",
            "reduce": "arr_reduce",
            "reduceRight": "arr_reduce_right",
            "reverse": "arr_reverse",
            "shift": "arr_shift",
            "slice": "arr_slice",
            "some": "arr_some",
            "sort": "arr_sort",
            "splice": "arr_splice",
            "toString": "arr_to_string",
            "unshift": "arr_unshift",
            "isArray": "is_array",
        }
        for slug in array_method_group:
            if f"Array.{slug}(" in content or f".{slug}(" in content:
                skills.append(f"js/{array_method_group[slug]}")
        # js/addition
        if " + " in content:
            skills.append("js/addition")
        # js/conditional_operator
        if " ? " in content:
            skills.append("js/conditional_operator")
        # js/decrement
        if " -- " in content:
            skills.append("js/decrement")
        # js/division
        if " / " in content:
            skills.append("js/division")
        # js/equality
        if " == " in content:
            skills.append("js/equality")
        # js/greater_than
        if " > " in content:
            skills.append("js/greater_than")
        # js/increment
        if " ++ " in content:
            skills.append("js/increment")
        # js/less_than
        if " < " in content:
            skills.append("js/less_than")
        # js/logic
        if " && " in content or " || " in content:
            skills.append("js/logic")
        # js/multiplication
        if " * " in content:
            skills.append("js/multiplication")
        # js/remainder
        if " % " in content:
            skills.append("js/remainder")
        # js/spread_operator
        if "..." in content:
            skills.append("js/spread_operator")
        # js/strict_equality
        if " === " in content:
            skills.append("js/strict_equality")
        # js/subtraction
        if " - " in content:
            skills.append("js/subtraction")
        # js/template_literals
        if "`" in content:
            skills.append("js/template_literals")
        # js/const
        if "const " in content:
            skills.append("js/const")
        # js/instanceof
        if " instanceof " in content:
            skills.append("js/instanceof")
        # js/let
        if "let " in content:
            skills.append("js/let")
        # js/typeof
        if "typeof " in content:
            skills.append("js/typeof")
        # js/num_is_finite
        if "isFinite(" in content:
            skills.append("js/num_is_finite")
        # js/num_is_nan
        if "isNaN(" in content:
            skills.append("js/num_is_nan")
        # js/num_parse_float
        if "parseFloat(" in content:
            skills.append("js/num_parse_float")
        # js/num_parse_int
        if "parseInt(" in content:
            skills.append("js/num_parse_int")
        # js/num_to_locale_string
        if "toLocaleString(" in content:
            skills.append("js/num_to_locale_string")
        # js/to_fixed
        if "toFixed(" in content:
            skills.append("js/to_fixed")
        # js/str_last_index_of
        if "lastIndexOf(" in content:
            skills.append("js/str_last_index_of")
        # js/str_length
        if ".length" in content:
            skills.append("js/str_length")
        # js/str_match
        if ".match(" in content:
            skills.append("js/str_match")
        # js/str_normalize
        if ".normalize(" in content:
            skills.append("js/str_normalize")
        # js/str_repeat
        if ".repeat(" in content:
            skills.append("js/str_repeat")
        # js/str_replace
        if ".replace(" in content:
            skills.append("js/str_replace")
        # js/str_split
        if ".split(" in content:
            skills.append("js/str_split")
        # js/char_code_at
        if ".charCodeAt(" in content:
            skills.append("js/char_code_at")
        # js/from_char_code
        if "fromCharCode(" in content:
            skills.append("js/from_char_code")
        # js/locale_compare
        if ".localeCompare(" in content:
            skills.append("js/locale_compare")
        # js/pad_end
        if ".padEnd(" in content:
            skills.append("js/pad_end")
        # js/pad_start
        if ".padStart(" in content:
            skills.append("js/pad_start")
        # js/starts_with
        if ".startsWith(" in content:
            skills.append("js/starts_with")
        # js/to_lower_case
        if ".toLowerCase(" in content:
            skills.append("js/to_lower_case")
        # js/to_upper_case
        if ".toUpperCase(" in content:
            skills.append("js/to_upper_case")
        # js/array
        if "[]" in content:
            skills.append("js/array")
        # js/blob
        if "Blob(" in content:
            skills.append("js/blob")
        # js/boolean
        if "Boolean(" in content:
            skills.append("js/boolean")
        # js/date
        if "Date(" in content:
            skills.append("js/date")
        # js/function
        if "function " in content:
            skills.append("js/function")
        # js/generator
        if "function*" in content:
            skills.append("js/generator")
        # js/intl_number_format
        if "Intl.NumberFormat(" in content:
            skills.append("js/intl_number_format")
        # js/iterator
        if "iterator" in content:
            skills.append("js/iterator")
        # js/json
        if "JSON." in content:
            skills.append("js/json")
        # js/map
        if "Map(" in content:
            skills.append("js/map")
        # js/math
        if "Math." in content:
            skills.append("js/math")
        # js/object
        if "Object." in content:
            skills.append("js/object")
        # js/promise
        if "Promise(" in content:
            skills.append("js/promise")
        # js/reg_exp
        if "RegExp(" in content:
            skills.append("js/reg_exp")
        # js/set
        if "Set(" in content:
            skills.append("js/set")
        # js/string
        if "String(" in content:
            skills.append("js/string")
        # js/symbol
        if "Symbol(" in content:
            skills.append("js/symbol")
        # js/type_error
        if "TypeError(" in content:
            skills.append("js/type_error")
        # js/url
        if "URL(" in content:
            skills.append("js/url")
        # js/weak_set
        if "WeakSet(" in content:
            skills.append("js/weak_set")
        # js/encode_url_component
        if "encodeURIComponent(" in content:
            skills.append("js/encode_url_component")
        # js/do_while
        if "do {" in content:
            skills.append("js/do_while")
        # js/for
        if "for (" in content:
            skills.append("js/for")
        # js/for_of
        if "for (" in content and "of " in content:
            skills.append("js/for_of")
        # js/for_in
        if "for (" in content and "in " in content:
            skills.append("js/for_in")
        # js/if_else
        if "if (" in content:
            skills.append("js/if_else")
        # js/switch_case
        if "switch (" in content:
            skills.append("js/switch_case")
        # js/try_catch
        if "try {" in content:
            skills.append("js/try_catch")
        # js/while
        if "while (" in content:
            skills.append("js/while")
        # js/set_has
        if ".has(" in content:
            skills.append("js/set_has")
        # js/set_size
        if ".size" in content:
            skills.append("js/set_size")
        # js/func_apply
        if ".apply(" in content:
            skills.append("js/func_apply")
        # js/func_bind
        if ".bind(" in content:
            skills.append("js/func_bind")
        # js/func_call
        if ".call(" in content:
            skills.append("js/func_call")
        # js/add_event_listener
        if ".addEventListener(" in content:
            skills.append("js/add_event_listener")
        # js/clear_timeout
        if "clearTimeout(" in content:
            skills.append("js/clear_timeout")
        # js/onchange
        if "onchange" in content:
            skills.append("js/onchange")
        # js/set_timeout
        if "setTimeout(" in content:
            skills.append("js/set_timeout")
        # js/console
        if "console." in content:
            skills.append("js/console")
        # js/crypto
        if "crypto." in content:
            skills.append("js/crypto")

        return list(set(skills))

    def __parse_react_skill(self, content):
        slugs = {
            "useCallback": "use_callback",
            "useContext": "use_context",
            "useEffect": "use_effect",
            "useForm": "use_form",
            "useLayoutEffect": "use_layout_effect",
            "useLocation": "use_location",
            "useMemo": "use_memo",
            "useParams": "use_params",
            "useReducer": "use_reducer",
            "useRef": "use_ref",
            "useState": "use_state",
            "createPortal": "create_portal",
            "createRoot": "create_root",
            "render": "render",
            "unmountComponentAtNode": "unmount_component_at_node",
            "Component": "component",
            "Link": "link",
            "Route": "route",
        }
        skills = []
        for slug in slugs:
            if f"React.{slug}(" in content:
                skills.append(f"react/{slugs[slug]}")
        return list(set(skills))

    def __parse_java_skill(self, content):
        skills = []
        # java/method_overriding
        if "@Override" in content:
            skills.append("java/method_overriding")
        # java/annotation
        if "@" in content:
            skills.append("java/annotation")
        # java/net
        if "net." in content:
            skills.append("java/net")
        # java/reflect
        if "reflect." in content:
            skills.append("java/reflect")
        # java/stream
        if "stream." in content:
            skills.append("java/stream")
        # java/xml_dom4j
        if "dom4j." in content:
            skills.append("java/xml_dom4j")
        # java/abstraction
        if "abstract" in content:
            skills.append("java/abstraction")
        # java/arraylist
        if "ArrayList" in content:
            skills.append("java/arraylist")
        # java/classes_objects
        if "class " in content:
            skills.append("java/classes_objects")
        # java/date
        if "date." in content:
            skills.append("java/date")
        # java/enums
        if "enum " in content:
            skills.append("java/enums")
        # java/exceptions
        if "Exception" in content:
            skills.append("java/exceptions")
        # java/hashmap
        if "HashMap" in content:
            skills.append("java/hashmap")
        # java/hashset
        if "HashSet" in content:
            skills.append("java/hashset")
        # java/inheritance
        if "extends " in content:
            skills.append("java/inheritance")
        # java/interface
        if "interface " in content:
            skills.append("java/interface")
        # java/iterator
        if "Iterator" in content:
            skills.append("java/iterator")
        # java/linkedlist
        if "LinkedList" in content:
            skills.append("java/linkedlist")
        # java/packages_api
        if "package " in content:
            skills.append("java/packages_api")
        # java/regex
        if "regex." in content:
            skills.append("java/regex")
        # java/threads
        if "Thread" in content:
            skills.append("java/threads")
        # java/user_input
        if "Scanner" in content:
            skills.append("java/user_input")
        # java/wrapper_classes
        if (
            "intValue(" in content
            or "doubleValue(" in content
            or "booleanValue(" in content
            or "byteValue(" in content
            or "shortValue(" in content
            or "longValue(" in content
            or "floatValue(" in content
            or "charValue(" in content
        ):
            skills.append("java/wrapper_classes")
        # java/files
        if "File" in content:
            skills.append("java/files")
        # java/io
        if "io." in content:
            skills.append("java/io")
        # java/nio
        if "nio." in content:
            skills.append("java/nio")
        # java/create_write_files
        if "File" in content and ".createNewFile(" in content:
            skills.append("java/create_write_files")
        # java/delete_files
        if "File" in content and ".delete(" in content:
            skills.append("java/delete_files")
        # java/read_files
        if "File" in content and ".read(" in content:
            skills.append("java/read_files")
        # java/identifier
        if "identifier" in content:
            skills.append("java/identifier")
        # java/sorting
        if "sort(" in content:
            skills.append("java/sorting")
        # java/stringbuffer_stringbuilder
        if "StringBuffer" in content or "StringBuilder" in content:
            skills.append("java/stringbuffer_stringbuilder")
        # java/working
        if "working" in content:
            skills.append("java/working")
        # java/arrays
        if "[]" in content:
            skills.append("java/arrays")
        # java/booleans
        if "boolean" in content:
            skills.append("java/booleans")
        # java/break_continue
        if "break" in content or "continue" in content:
            skills.append("java/break_continue")
        # java/comments
        if "//" in content or "/*" in content:
            skills.append("java/comments")
        # java/data_types
        if (
            "byte" in content
            or "short" in content
            or "int" in content
            or "long" in content
            or "float" in content
            or "double" in content
            or "char" in content
            or "boolean" in content
        ):
            skills.append("java/data_types")
        # java/for_loop
        if "for (" in content:
            skills.append("java/for_loop")
        # java/if_else
        if "if (" in content:
            skills.append("java/if_else")
        # java/math
        if "Math." in content:
            skills.append("java/math")
        # java/operators
        if (
            "+" in content
            or "-" in content
            or "*" in content
            or "/" in content
            or "%" in content
            or "=" in content
            or "++" in content
            or "--" in content
        ):
            skills.append("java/operators")
        # java/output
        if "System.out.println(" in content:
            skills.append("java/output")
        # java/strings
        if "String " in content:
            skills.append("java/strings")
        # java/switch
        if "switch (" in content:
            skills.append("java/switch")
        # java/variables
        if "var " in content:
            skills.append("java/variables")
        # java/while_loop
        if "while (" in content:
            skills.append("java/while_loop")
        # java/collections_methods
        if "Collections." in content:
            skills.append("java/collections_methods")
        # java/math_methods
        if "Math." in content:
            skills.append("java/math_methods")
        if "System." in content:
            skills.append("java/system_methods")

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

    def parse(self, language: str, content: str):
        if language == "python":
            return self.__parse_python_skill(content)
        elif language == "tkinter":
            return self.__parse_tkinter_skill(content)
        elif language == "sklearn":
            return self.__parse_sklearn_skill(content)
        elif language == "shell":
            return self.__parse_shell_skill(content)
        elif language == "rust":
            return self.__parse_rust_skill(content)
        elif language == "pygame":
            return self.__parse_pygame_skill(content)
        elif language == "django":
            return self.__parse_django_skill(content)
        elif language == "go":
            return self.__parse_go_skill(content)
        elif language == "flask":
            return self.__parse_flask_skill(content)
        elif language == "cpp":
            return self.__parse_cpp_skill(content)
        elif language == "c":
            return self.__parse_c_skill(content)
        elif language == "html":
            return self.__parse_html_skill(content)
        elif language == "css":
            return self.__parse_css_skill(content)
        elif language == "jquery":
            return self.__parse_jquery_skill(content)
        elif language == "javascript":
            return self.__parse_javascript_skill(content)
        elif language == "react":
            return self.__parse_react_skill(content)
        elif language == "java":
            return self.__parse_java_skill(content)
        elif language == "mysql":
            return self.__parse_mysql_skill(content)
        elif language == "pandas":
            return self.__parse_pandas_skill(content)
        elif language == "matplotlib":
            return self.__parse_matplotlib_skill(content)
