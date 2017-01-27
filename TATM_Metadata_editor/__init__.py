# -*- coding: utf-8 -*-
"""
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
  from Metadata_editor import MainPlugin
  return MainPlugin(iface)
