import sys
from pluginbase import PluginBase


plugin_base = PluginBase(package='kakeibox_core.plugins')
plugins = plugin_base.make_plugin_source(searchpath=sys.path)
