from nose.selector import Selector
from nose.plugins import Plugin
from fnmatch import fnmatch
import builtins
import optparse
import logging
import inspect
import types
import nose
import sys
import os


class Lineage(object):
    """Knows how to get the lineage of things"""

    def __init__(self):
        self.lineage = {}
        self._ignored = {}
        self._focused = {}
        self._focused_all = {}

    def determine(self, thing):
        """
        Get all the classes in the lineage of this method
        Memoize the results for each method and class as we go along
        """
        if repr(thing) not in self.lineage:
            lineage = []

            def add(thing):
                """Add something and it's lineage to lineage"""
                if thing not in lineage:
                    lineage.append(thing)
                    for determined in self.determine(thing):
                        if determined not in lineage:
                            lineage.append(determined)

            if isinstance(thing, (types.BuiltinMethodType, types.BuiltinFunctionType)):
                pass

            elif isinstance(thing, types.ModuleType):
                name = thing.__name__
                if name.count(".") > 0:
                    parent = ".".join(name.split(".")[:-1])
                    if parent in sys.modules:
                        add(sys.modules[parent])

            else:
                is_method = (
                    isinstance(thing, types.FunctionType)
                    and getattr(thing, "__qualname__", "").count(".") > 0
                )
                if is_method or isinstance(thing, types.MethodType):
                    parent = None
                    if is_method:
                        # Damn you python3 and your inability to know if a Function comes from a class
                        parent = getattr(
                            sys.modules[thing.__module__], thing.__qualname__.split(".")[0]
                        )
                    if hasattr(thing, "im_class"):
                        parent = thing.im_class
                    elif hasattr(thing, "__self__"):
                        parent = thing.__self__.__class__

                    for ancestor in self.getmro(parent):
                        if thing.__name__ in ancestor.__dict__:
                            parent = ancestor
                            break

                    if parent:
                        add(parent)
                else:
                    module = getattr(thing, "__module__", None)
                    if isinstance(module, str):
                        module = sys.modules.get(module)

                    if module and module is not builtins:
                        add(module)

                    if not isinstance(thing, types.FunctionType):
                        klses = self.getmro(thing)

                        for kls in klses:
                            if kls and kls not in (thing, type, object):
                                add(kls)

            self.lineage[repr(thing)] = lineage
        return self.lineage[repr(thing)]

    def getmro(self, thing):
        """
        Get the mro list of a class and take into account custom __embedded_class_parent__ attribute.

        The __embedded_class_parent__ can be used by an embedded class to point at it's parent.
        """
        klses = list(inspect.getmro(thing))

        if hasattr(thing, "__embedded_class_parent__"):
            klses.extend(self.getmro(thing.__embedded_class_parent__))

        return klses

    def unmatched(self, thing):
        if hasattr(self, "selector") and hasattr(thing, "__name__"):
            if not self.selector.matches(thing.__name__):
                return False

    def ignored(self, thing):
        """Ignored is thing or anything in lineage with nose_ignore set to true"""
        if thing not in self._ignored:
            ignored = False
            lineage = self.determine(thing)
            if getattr(thing, "nose_focus_ignore", None) or (
                lineage and any(self.ignored(kls) for kls in lineage)
            ):
                ignored = True

            self._ignored[thing] = ignored
        return self._ignored[thing]

    def focused_all(self, thing):
        """Focused all is anything not ignored with the thing, or anything in it's lineage having focus_all set"""
        if thing not in self._focused_all:
            focused_all = False
            lineage = self.determine(thing)
            if not self.ignored(thing):
                if getattr(thing, "nose_focus_all", None) or (
                    lineage and any(self.focused_all(kls) for kls in lineage)
                ):
                    focused_all = True
            self._focused_all[thing] = focused_all
        return self._focused_all[thing]

    def focused(self, thing):
        """Focused is not ignored, any parents focused due to focus_all logic, or this thing or parent has nose_focus set to Truthy"""
        if thing not in self._focused:
            focused = False
            lineage = self.determine(thing)
            if not self.ignored(thing):
                if lineage and any(self.focused_all(kls) for kls in [thing] + lineage):
                    focused = True
                else:
                    parent = None
                    if lineage:
                        parent, lineage = lineage[0], lineage[1:]

                    is_class = isinstance(thing, type)
                    is_not_class = not is_class
                    parent_is_not_class = not parent or not isinstance(parent, type)
                    if getattr(thing, "nose_focus", None) or (
                        ((is_class and parent_is_not_class) or is_not_class)
                        and parent
                        and self.focused(parent)
                    ):
                        focused = True
            self._focused[thing] = focused
        return self._focused[thing]


class Plugin(Plugin):
    name = "nose_focus"

    def __init__(self, *args, **kwargs):
        self.lineage = Lineage()
        self.current_module = None
        super(Plugin, self).__init__(*args, **kwargs)

    def wantModule(self, module):
        self.current_module = module
        return

    def wantThing(self, thing):
        """Only want methods that have nose_focus set to a truthy value"""
        if not self.enabled or (not self.only_focus and not self.just_ignore):
            return

        if isinstance(thing, nose.pyversion.UnboundMethod):
            thing = thing._func

        if self.lineage.unmatched(thing) is False:
            return False

        if self.lineage.ignored(thing):
            return False

        if self.just_ignore:
            return

        return self.lineage.focused(thing)

    wantMethod = wantThing
    wantFunction = wantThing

    def wantFile(self, filename):
        """Ignore directories if we only want to include particular directories"""
        basename = os.path.basename(filename)
        if self.only_include_filename:
            if not any(fnmatch(basename, pattern) for pattern in self.only_include_filename):
                return False

    def options(self, parser, env={}):
        super(Plugin, self).options(parser, env)

        parser.add_option(
            "--with-focus",
            help="Enable nose_focus",
            action="store_true",
            dest="only_focus",
            default=False,
        )

        parser.add_option(
            "--without-ignored",
            help="Run all tests except those that are ignored",
            action="store_true",
            dest="just_ignore",
            default=False,
        )

        parser.add_option(
            "--only-include-filename", help="Glob of filenames to include", action="append"
        )

    def configure(self, options, conf):
        super(Plugin, self).configure(options, conf)
        if options.only_focus and options.just_ignore:
            raise optparse.OptionError(
                "Please specify only one --with-focus or --without-ignored", "--with-focus"
            )
        self.enabled = options.only_focus or options.just_ignore or options.only_include_filename
        self.lineage.selector = Selector(conf)
        self.only_focus = options.only_focus
        self.just_ignore = options.just_ignore
        self.only_include_filename = options.only_include_filename
        self.logger = logging.getLogger("{0}.{1}".format(__name__, type(self).__name__))
