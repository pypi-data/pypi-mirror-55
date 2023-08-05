"""Module for working with the dodo configurations."""
import os
import ruamel.yaml
import sys
import json
import re

from dodo_commands.framework.paths import Paths
from dodo_commands.framework.config_io import ConfigIO
from dodo_commands.framework.command_error import CommandError
from dodo_commands.framework.config_expander import ConfigExpander
from dodo_commands.framework.config_expander import Key, KeyNotFound  # noqa
from dodo_commands.framework.global_config import create_global_config  # noqa

try:
    from dotenv import dotenv_values
except ImportError:
    # Stub
    def dotenv_values(x):
        raise CommandError(
            "Package python-dotenv not installed. Please run: pip install python-dotenv."
        )


def merge_into_config(config, layer, xpath=None):
    def _is_list(x):
        return isinstance(x, type(list()))

    def _is_dict(x):
        return isinstance(x, type(dict()))

    def _raise(xpath):
        raise CommandError("Cannot merge configurations. Check key /%s" %
                           '/'.join(new_xpath))

    xpath = xpath or []
    for key, val in (layer or {}).items():
        new_xpath = xpath + [key]

        if key not in config:
            config[key] = val
        elif _is_dict(val):
            if not _is_dict(config[key]):
                _raise(new_xpath)
            merge_into_config(config[key], val, new_xpath)
        elif _is_list(val):
            if not _is_list(config[key]):
                _raise(new_xpath)
            config[key].extend(val)
        else:
            config[key] = val


def _add_to_config(config, section, key, value):
    if section in config:
        if key not in config[section]:
            config[section][key] = value


def _system_commands_dir():
    """Return directory where system command scripts are stored"""
    import dodo_commands.dodo_system_commands
    return os.path.dirname(dodo_commands.dodo_system_commands.__file__)


def _extend_config(config):
    """Add special values to the project's config"""
    project_dir = Paths().project_dir()
    if project_dir:
        _add_to_config(config, "ROOT", "project_name",
                       os.path.basename(project_dir))
        _add_to_config(config, "ROOT", "project_dir", project_dir)
        _add_to_config(config, "ROOT", "res_dir", Paths().res_dir())


def extend_command_path(config):
    """Add the system commands to the command path"""
    _add_to_config(config, "ROOT", "command_path", [])
    config['ROOT']['command_path'].append(_system_commands_dir())
    if not Paths().project_dir():
        config['ROOT']['command_path'].append(
            os.path.join(Paths().default_commands_dir(), '*'))


def _report(x):
    sys.stderr.write(x)
    sys.stderr.flush()


def load_config(layer_filenames, config_io=None, filenames_and_layers=None):
    config_io = config_io or ConfigIO()
    try:
        config = {'ROOT': {}}
        for layer_filename in layer_filenames:
            layer = config_io.load(layer_filename)
            if filenames_and_layers is not None:
                filenames_and_layers.append((layer_filename, layer))
            merge_into_config(config, layer)

    except ruamel.yaml.scanner.ScannerError:
        _report("There was an error while loading the configuration. "
                "Run 'dodo diff' to compare your configuration to the "
                "default one.\n")

    _extend_config(config)
    extra_vars = dict()

    def _load_env(dotenv_file):
        if not os.path.exists(dotenv_file):
            _report("Dotenv file not found: %s\n" % dotenv_file)
        extra_vars.update(dotenv_values(dotenv_file))

    # Call dotenv_values for every item of /ENV/dotenv
    callbacks = {}
    for idx, _ in enumerate(config['ROOT'].get('dotenv_files', [])):
        callbacks['/ROOT/dotenv_files/%d' % idx] = _load_env

    ConfigExpander(extra_vars).run(config, callbacks=callbacks)
    return config


def expand_keys(config, text):
    result = ""
    val_terms = re.split('\$\{([^\}]+)\}', text)
    for idx, term in enumerate(val_terms):
        if idx % 2:
            xpath = [k for k in term.split("/") if k]
            str_rep = json.dumps(Key(config, xpath).get())
            if str_rep.startswith('"') and str_rep.endswith('"'):
                str_rep = str_rep[1:-1]
            result += str_rep
        else:
            result += term
    return result
