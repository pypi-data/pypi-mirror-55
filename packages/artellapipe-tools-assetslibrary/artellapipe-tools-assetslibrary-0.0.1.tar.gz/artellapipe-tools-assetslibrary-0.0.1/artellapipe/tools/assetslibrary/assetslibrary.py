#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool that allow artists to load assets into DCC scenes
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import logging
import traceback
from functools import partial

from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *

import tpDccLib as tp
from tpQtLib.core import qtutils
from tpQtLib.widgets import splitters

import artellapipe
from artellapipe.core import asset, tool
from artellapipe.utils import resource

LOGGER = logging.getLogger()


class ArtellaAssetsLibraryWidget(QWidget, object):
    def __init__(self, project, supported_files=None, parent=None):

        self._supported_files = supported_files if supported_files else dict()
        self._project = project
        super(ArtellaAssetsLibraryWidget, self).__init__(parent=parent)

        self.ui()
        self.resize(150, 800)

        self._assets_viewer.update_assets()
        self._menu = self._create_contextual_menu()

    def ui(self):

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self._main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self._main_widget.setLayout(main_layout)
        self.main_layout.addWidget(self._main_widget)

        self._assets_viewer = artellapipe.AssetsViewer(
            project=self._project,
            column_count=2,
            parent=self
        )
        self._assets_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._top_layout = QHBoxLayout()
        self._top_layout.setContentsMargins(0, 0, 0, 0)
        self._top_layout.setSpacing(2)
        self._top_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(self._top_layout)

        self._categories_menu_layout = QHBoxLayout()
        self._categories_menu_layout.setContentsMargins(0, 0, 0, 0)
        self._categories_menu_layout.setSpacing(5)
        self._categories_menu_layout.setAlignment(Qt.AlignTop)
        self._top_layout.addLayout(self._categories_menu_layout)

        self._categories_btn_grp = QButtonGroup(self)
        self._categories_btn_grp.setExclusive(True)

        main_layout.addWidget(self._assets_viewer)

        self._supported_types_layout = QHBoxLayout()
        self._supported_types_layout.setContentsMargins(2, 2, 2, 2)
        self._supported_types_layout.setSpacing(2)
        self._supported_types_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(self._supported_types_layout)

        self._supported_types_btn_grp = QButtonGroup(self)
        self._supported_types_btn_grp.setExclusive(True)

        self._fit_camera_cbx = QCheckBox('Fit Camera')
        self.main_layout.addLayout(splitters.SplitterLayout())
        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.setContentsMargins(5, 5, 5, 5)
        checkboxes_layout.setSpacing(2)
        self.main_layout.addLayout(checkboxes_layout)
        checkboxes_layout.addWidget(self._fit_camera_cbx)
        checkboxes_layout.addItem(QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.main_layout.addLayout(splitters.SplitterLayout())

        self._assets_viewer.assetAdded.connect(self._on_asset_added)

        self.update_asset_categories()
        self.update_supported_types()

    def contextMenuEvent(self, event):
        if not self._menu:
            return
        self._menu.exec_(event.globalPos())

    def update_asset_categories(self, asset_categories=None):
        """
        Updates current categories with the given ones
        :param asset_categories: list(str)
        """

        if not asset_categories:
            asset_categories = self._get_asset_categories()

        for btn in self._categories_btn_grp.buttons():
            self._categories_btn_grp.removeButton(btn)

        qtutils.clear_layout(self._categories_menu_layout)

        all_asset_categories = [asset.ArtellaAssetFileStatus.ALL]
        all_asset_categories.extend(asset_categories)
        for category in all_asset_categories:
            new_btn = QPushButton(category)
            new_btn.setMinimumWidth(QFontMetrics(new_btn.font()).width(category) + 10)
            new_btn.setIcon(resource.ResourceManager().icon(category.lower()))
            new_btn.setCheckable(True)
            self._categories_menu_layout.addWidget(new_btn)
            self._categories_btn_grp.addButton(new_btn)
            if category == asset.ArtellaAssetFileStatus.ALL:
                new_btn.setIcon(resource.ResourceManager().icon('home'))
                new_btn.setChecked(True)
            new_btn.toggled.connect(partial(self._change_category, category))

    def update_supported_types(self):
        """
        Updates current supported types
        """

        for btn in self._supported_types_btn_grp.buttons():
            self._supported_types_btn_grp.removeButton(btn)

        qtutils.clear_layout(self._supported_types_layout)

        if not self._supported_files:
            LOGGER.warning('No Supported Files for AssetsLibrary!')
            return

        total_buttons = 0
        for type_name, type_extension in self._supported_files.items():
            new_btn = QPushButton(type_name.title())
            new_btn.setIcon(resource.ResourceManager().icon(type_name.lower()))
            new_btn.setCheckable(True)
            new_btn.extension = type_extension
            self._supported_types_layout.addWidget(new_btn)
            self._supported_types_btn_grp.addButton(new_btn)
            if total_buttons == 0:
                new_btn.setChecked(True)
            total_buttons += 1

    def _change_category(self, category, flag):
        """
        Internal function that is called when the user presses an Asset Category button
        :param category: str
        """

        if flag:
            self._assets_viewer.change_category(category=category)

    def _setup_asset_signals(self, asset_widget):
        """
        Internal function that sets proper signals to given asset widget
        This function can be extended to add new signals to added items
        :param asset_widget: ArtellaAssetWidget
        """

        asset_widget.clicked.connect(self._on_asset_clicked)

    def _create_contextual_menu(self):
        """
        Returns custom contextual menu
        :return: QMenu
        """

        new_menu = QMenu(self)
        get_thumbnails_action = QAction(
            resource.ResourceManager().icon('picture'), 'Update Thumbnails', new_menu)
        get_thumbnails_action.triggered.connect(self._on_update_thumbnails)
        new_menu.addAction(get_thumbnails_action)

        return new_menu

    def _on_update_thumbnails(self):
        """
        Internal callback function that is called when Update Thumbnails action is triggered
        """

        self._assets_viewer.update_assets_thumbnails(force=True)

    def _on_asset_added(self, asset_widget):
        """
        Internal callback function that is called when a new asset widget is added to the assets viewer
        :param asset_widget: ArtellaAssetWidget
        """

        if not asset_widget:
            return

        self._setup_asset_signals(asset_widget)

    def _get_asset_categories(self):
        """
        Returns a list with the asset categories supported
        :return: list(str)
        """

        return artellapipe.AssetsMgr().config.get('types') or list()

    def _on_asset_clicked(self, asset_widget):
        """
        Internal callback function that is called when an asset button is clicked
        :param asset_widget: ArtellaAssetWidget
        """

        if not asset_widget:
            return

        for btn in self._supported_types_btn_grp.buttons():
            if btn.isChecked():
                try:
                    res = asset_widget.asset.reference_file_by_extension(
                        extension=btn.extension)
                    if res:
                        if self._fit_camera_cbx.isChecked():
                            try:
                                tp.Dcc.select_object(res)
                                tp.Dcc.fit_view(True)
                                tp.Dcc.clear_selection()
                            except Exception as exc:
                                LOGGER.warning('Impossible to fit camera view to referenced objects!')
                except Exception as e:
                    LOGGER.warning('Impossible to reference asset!')
                    LOGGER.error('{} | {}'.format(e, traceback.format_exc()))
                finally:
                    return


class ArtellaAssetsLibrary(tool.Tool, object):

    LIBRARY_WIDGET = ArtellaAssetsLibraryWidget

    def __init__(self, project, config):
        super(ArtellaAssetsLibrary, self).__init__(project=project, config=config)

    def ui(self):
        super(ArtellaAssetsLibrary, self).ui()

        supported_files = self.config.get('supported_files')
        self._library_widget = self.LIBRARY_WIDGET(project=self._project, supported_files=supported_files)
        self.main_layout.addWidget(self._library_widget)
