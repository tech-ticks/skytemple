#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from enum import Enum
from typing import TYPE_CHECKING, Type, Union, Optional

from gi.repository import Gtk

from skytemple.core.module_controller import AbstractController
from skytemple.core.string_provider import StringType
from skytemple.core.ui_utils import glib_async, builder_get_assert, iter_tree_model
from skytemple_files.common.i18n_util import f, _
from skytemple_files.data.md.protocol import PokeType
from skytemple_files.hardcoded.dungeons import (
    TilesetMapColor,
    TilesetStirringEffect,
    TilesetBaseEnum,
    TilesetSecretPowerEffect,
    TilesetNaturePowerMoveEntry,
    TilesetWeatherEffect,
    TilesetProperties,
)

if TYPE_CHECKING:
    from skytemple.module.dungeon_graphics.module import DungeonGraphicsModule

DUNGEON_GRAPHICS_NAME = _("Dungeon Graphics")


class MainController(AbstractController):
    def __init__(self, module: "DungeonGraphicsModule", *args):
        self.module = module

        self.builder: Gtk.Builder = None  # type: ignore
        self.lst = self.module.get_tileset_properties()

    def get_view(self) -> Gtk.Widget:
        self.builder = self._get_builder(__file__, "main.glade")
        assert self.builder

        self._init_combo_stores()
        self._init_values()

        self.builder.connect_signals(self)
        return builder_get_assert(self.builder, Gtk.Widget, "box_list")

    @glib_async
    def on_cr_map_color_changed(
        self, widget: Gtk.CellRendererCombo, path, new_iter, *args
    ):
        store = builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        cb_store = widget.props.model

        store[path][2] = cb_store[new_iter][0]
        store[path][9] = cb_store[new_iter][1]
        self._save_list()

    @glib_async
    def on_cr_stirring_effect_changed(
        self, widget: Gtk.CellRendererCombo, path, new_iter, *args
    ):
        store = builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        cb_store = widget.props.model

        store[path][3] = cb_store[new_iter][0]
        store[path][10] = cb_store[new_iter][1]
        self._save_list()

    @glib_async
    def on_cr_secret_power_effect_changed(
        self, widget: Gtk.CellRendererCombo, path, new_iter, *args
    ):
        store = builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        cb_store = widget.props.model

        store[path][4] = cb_store[new_iter][0]
        store[path][11] = cb_store[new_iter][1]
        self._save_list()

    @glib_async
    def on_cr_camouflage_type_changed(
        self, widget: Gtk.CellRendererCombo, path, new_iter, *args
    ):
        store = builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        cb_store = widget.props.model

        store[path][5] = cb_store[new_iter][0]
        store[path][12] = cb_store[new_iter][1]
        self._save_list()

    @glib_async
    def on_cr_nature_power_move_entry_changed(
        self, widget: Gtk.CellRendererCombo, path, new_iter, *args
    ):
        store = builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        cb_store = widget.props.model

        store[path][6] = cb_store[new_iter][0]
        store[path][13] = cb_store[new_iter][1]
        self._save_list()

    @glib_async
    def on_cr_weather_effect_changed(
        self, widget: Gtk.CellRendererCombo, path, new_iter, *args
    ):
        store = builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        cb_store = widget.props.model

        store[path][7] = cb_store[new_iter][0]
        store[path][14] = cb_store[new_iter][1]
        self._save_list()

    def on_cr_full_water_floor_toggled(self, widget: Gtk.CellRendererToggle, path):
        store = builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        store[path][8] = not widget.get_active()
        self._save_list()

    def _init_combo_stores(self):
        # cr_map_color
        self._create_for_enum(
            builder_get_assert(self.builder, Gtk.CellRendererCombo, "cr_map_color"),
            TilesetMapColor,
        )
        # cr_stirring_effect
        self._create_for_enum(
            builder_get_assert(
                self.builder, Gtk.CellRendererCombo, "cr_stirring_effect"
            ),
            TilesetStirringEffect,
        )
        # cr_secret_power_effect
        self._create_for_enum(
            builder_get_assert(
                self.builder, Gtk.CellRendererCombo, "cr_secret_power_effect"
            ),
            TilesetSecretPowerEffect,
        )
        # cr_camouflage_type
        self._create_for_enum_with_strings(
            builder_get_assert(
                self.builder, Gtk.CellRendererCombo, "cr_camouflage_type"
            ),
            PokeType,
            StringType.TYPE_NAMES,
        )
        # cr_nature_power_move_entry
        self._create_for_enum(
            builder_get_assert(
                self.builder, Gtk.CellRendererCombo, "cr_nature_power_move_entry"
            ),
            TilesetNaturePowerMoveEntry,
        )
        # cr_weather_effect
        self._create_for_enum(
            builder_get_assert(
                self.builder, Gtk.CellRendererCombo, "cr_weather_effect"
            ),
            TilesetWeatherEffect,
        )

    def _create_for_enum(self, cr: Gtk.CellRendererCombo, en: type[Enum]):
        store = Gtk.ListStore(int, str)  # id, name
        cr.props.model = store
        for e in en:
            store.append([e.value, e.print_name])  # type: ignore

    def _create_for_enum_with_strings(
        self, cr: Gtk.CellRendererCombo, en: type[Enum], string_type: StringType
    ):
        store = Gtk.ListStore(int, str)  # id, name
        cr.props.model = store
        for e in en:
            store.append([e.value, self.module.project.get_string_provider().get_value(string_type, e.value)])  # type: ignore

    def _init_values(self):
        from skytemple.module.dungeon_graphics.module import NUMBER_OF_TILESETS

        store = builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        for i, v in enumerate(self.lst):
            store.append(
                [
                    str(i),
                    (
                        f"{_('Tileset')} {i}"
                        if i < NUMBER_OF_TILESETS
                        else f"{_('Background')} {i}"
                    ),
                    v.map_color.value,
                    v.stirring_effect.value,
                    v.secret_power_effect.value,
                    v.camouflage_type.value,
                    v.nature_power_move_entry.value,
                    v.weather_effect.value,
                    v.full_water_floor,
                    v.map_color.print_name,
                    v.stirring_effect.print_name,
                    v.secret_power_effect.print_name,
                    self.module.project.get_string_provider().get_value(
                        StringType.TYPE_NAMES, v.camouflage_type.value
                    ),
                    v.nature_power_move_entry.print_name,
                    v.weather_effect.print_name,
                ]
            )

    def _save_list(self):
        self.lst = []
        for row in iter_tree_model(
            builder_get_assert(self.builder, Gtk.ListStore, "list_tree_store")
        ):
            self.lst.append(
                TilesetProperties(
                    TilesetMapColor(row[2]),  # type: ignore
                    TilesetStirringEffect(row[3]),  # type: ignore
                    TilesetSecretPowerEffect(row[4]),  # type: ignore
                    PokeType(row[5]),
                    TilesetNaturePowerMoveEntry(row[6]),  # type: ignore
                    TilesetWeatherEffect(row[7]),  # type: ignore
                    bool(row[8]),
                )
            )

        self.module.set_tileset_properties(self.lst)
