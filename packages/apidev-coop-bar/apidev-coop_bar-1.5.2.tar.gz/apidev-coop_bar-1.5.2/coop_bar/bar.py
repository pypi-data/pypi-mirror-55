# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from importlib import import_module

from django.conf import settings


class CoopBar:
    """The main class"""

    __we_all_are_one = {}

    def __init__(self):
        self.__dict__ = self.__we_all_are_one  # Borg pattern

        if not self.__dict__:  # Don't reload for each instance
            self._callbacks = []
            self._headers = []
            self._css_classes = []
            coop_bar_modules = getattr(settings, 'COOP_BAR_MODULES', None)
            if coop_bar_modules:
                for module_name in coop_bar_modules:
                    try:
                        app_admin_bar_module = import_module(module_name)
                        loader_fct = getattr(app_admin_bar_module, 'load_commands')
                        loader_fct(self)
                    except ImportError as msg:
                        raise ImportError("coop_bar : error while loading '{0}': {1}".format(module_name, msg))
            else:
                for app in settings.INSTALLED_APPS:
                    try:
                        # load dynamically the admin_bar module of all apps
                        app_admin_bar_module = import_module(app+'.coop_bar_cfg')
                        if hasattr(app_admin_bar_module, 'load_commands'):
                            # call the load_commands function in this module
                            # This function should call the AdminBar:register_command for
                            # every item it want to insert in the bar
                            loader_fct = getattr(app_admin_bar_module, 'load_commands')
                            loader_fct(self)
                    except ImportError as msg:
                        pass

    def register_header(self, callback):
        self._headers.append(callback)

    def register_command(self, callback):
        self._callbacks.append(callback)

    def register_separator(self):
        self._callbacks.append(None)
        
    def register_css_classes(self, callback):
        self._css_classes.append(callback)

    def register(self, list_of_list_of_cmds):
        for list_of_cmds in list_of_list_of_cmds:
            for callback in list_of_cmds:
                self.register_command(callback)
            self.register_separator()

    def get_commands(self, request, context):
        commands = []
        separator = '<div class="separator"></div>'
        for the_callback in self._callbacks:
            if the_callback is None:
                # Replace None by separator. Avoid 2 following separators
                if commands and commands[-1] != separator:
                    html = separator
                else:
                    html = ''
            else:
                # when a page wants to display the admin_bar
                # calls the registred callback in order to know what to display
                html = the_callback(request, context)
            if html:
                commands.append(html)
        if commands and commands[-1] == separator:
            commands = commands[:-1]
        return commands

    def get_headers(self, request, context):
        headers = []
        for header in self._headers:
            html = header(request, context)
            if html:
                headers.append(html)
        return headers
    
    def get_css_classes(self, request, context):
        css_classes = []
        for css_class in self._css_classes:
            css_class = css_class(request, context)
            if css_class:
                if type(css_class) in (list, tuple):
                    css_classes.extend(css_class)
                else:
                    css_classes.append(css_class)
        return " ".join(list(set(css_classes)))
