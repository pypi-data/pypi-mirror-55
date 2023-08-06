"""
This extension automatically generates AutoSummaries for modules/classes.

This extension can be enabled by adding ``"nengo_sphinx_theme.ext.autoautosummary"``
to the ``extensions`` list in ``conf.py``.
"""

import inspect

from docutils.parsers.rst import directives
import sphinx.ext.autosummary as autosummary

# We import nengo_sphinx_theme here to test the issue that
# `patch_autosummary_import_by_name` fixes.

import nengo_sphinx_theme  # pylint: disable=unused-import


# should be ignored
a_test_attribute = None


def a_test_function():
    """This is a test function."""


class TestClass:
    """This is a test class."""

    # should be ignored
    an_attribute = None

    def __init__(self):
        """This is the init method."""

    def a_method(self):
        """This is a method."""

    @staticmethod
    def a_static_method():
        """This is a static method."""

    def _a_private_method(self):
        """A private method."""

    def _another_private_method(self):
        """This method will be manually added."""


class AutoAutoSummary(autosummary.Autosummary):
    """
    Automatically generates a summary for a class or module.

    For classes this adds a summary for all methods.

    For modules this adds a summary for all classes/functions.
    """

    option_spec = {
        "nosignatures": directives.unchanged,
        "exclude-members": directives.unchanged,
    }

    required_arguments = 1

    def get_members(self, obj):
        if inspect.isclass(obj):
            module_name = obj.__module__

            def filter(x):
                return inspect.isroutine(x)

        elif inspect.ismodule(obj):
            module_name = obj.__name__

            def filter(x):
                return inspect.isclass(x) or inspect.isfunction(x)

        else:
            raise TypeError(
                "AutoAutoSummary only works with classes or modules (got %s)"
                % type(obj)
            )

        excluded = [
            x.strip() for x in self.options.get("exclude-members", "").split(",")
        ]

        items = []
        # note: we use __dict__ because it preserves the order of attribute definitions
        # (in python >= 3.6)
        for name in obj.__dict__:
            if not (name.startswith("_") or name in excluded):
                attr = getattr(obj, name)

                if filter(attr) and attr.__module__ == module_name:
                    items.append(name)

        return items

    def run(self):
        clazz = str(self.arguments[0])
        (module_name, obj_name) = clazz.rsplit(".", 1)
        mod = __import__(module_name, globals(), locals(), [obj_name])
        obj = getattr(mod, obj_name)

        new_content = ["%s.%s" % (clazz, item) for item in self.get_members(obj)]

        if inspect.isclass(obj):
            # add the class itself
            new_content = [clazz] + new_content

        self.content = new_content + self.content.data

        return super(AutoAutoSummary, self).run()


def patch_autosummary_import_by_name():
    """Monkeypatch a function in autosummary to disallow module cycles"""

    orig_f = autosummary.import_by_name

    def import_by_name(name, prefixes):
        # Filter out problematic prefixes
        prefixes = [p for p in prefixes if p is None or not name.startswith(p)]
        return orig_f(name, prefixes)

    autosummary.import_by_name = import_by_name


def setup(app):
    patch_autosummary_import_by_name()
    app.add_directive("autoautosummary", AutoAutoSummary)
