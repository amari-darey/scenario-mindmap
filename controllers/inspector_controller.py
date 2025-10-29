from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QColorDialog

from core.node import NodeItem
from core.commands_node import ChangeColorCommand


class InspectorController:
    def __init__(self, ui, scene, command_stack):
        self.ui = ui
        self.scene = scene
        self.command_stack = command_stack
        self._sidebar_updating = False

        self.connect()

    def connect(self):
        self.scene.selectionChanged.connect(self.on_selection_changed)
        self.ui.note_edit.textChanged.connect(self.on_note_changed)
        self.ui.color_btn.clicked.connect(self.on_choose_color)
        self.ui.font_combo.currentFontChanged.connect(self.on_font_changed)
        self.ui.font_size.valueChanged.connect(self.on_font_changed)
        self.ui.bold_chk.stateChanged.connect(self.on_font_changed)
        self.ui.italic_chk.stateChanged.connect(self.on_font_changed)
        self.ui.apply_attr_btn.clicked.connect(self.apply_attributes_to_selected)

    def get_single_selected_node(self):
        nodes = [it for it in self.scene.selectedItems() if isinstance(it, NodeItem)]
        return nodes[0] if len(nodes) == 1 else None

    def on_selection_changed(self):
        node = self.get_single_selected_node()
        self._sidebar_updating = True
        ui = self.ui
        if node:
            ui.note_edit.setPlainText(node.note)
            color = node.color
            ui.color_btn.setStyleSheet(f"background-color: rgb({color.red()},{color.green()},{color.blue()});")
            font = node.text_item.font()
            ui.font_combo.setCurrentFont(font)
            ui.font_size.setValue(font.pointSize())
            ui.bold_chk.setChecked(font.bold())
            ui.italic_chk.setChecked(font.italic())
        else:
            ui.note_edit.setPlainText('')
            ui.color_btn.setStyleSheet('')
            ui.font_combo.setCurrentFont(QFont())
            ui.font_size.setValue(12)
            ui.bold_chk.setChecked(False)
            ui.italic_chk.setChecked(False)
        self._sidebar_updating = False

    def on_note_changed(self):
        if self._sidebar_updating:
            return
        node = self.get_single_selected_node()
        if node:
            node.note = self.ui.note_edit.toPlainText()

    def on_choose_color(self):
        node = self.get_single_selected_node()
        initial = node.color if node else QColor(255,255,200)
        color = QColorDialog.getColor(initial, title='Select node color')
        if not color.isValid(): return

        if isinstance(node, NodeItem):
            self.command_stack.push(ChangeColorCommand(node, color))
        self.ui.color_btn.setStyleSheet(f"background-color: rgb({color.red()},{color.green()},{color.blue()});")

    def on_font_changed(self, *args):
        if self._sidebar_updating:
            return
        self.apply_attributes_to_selected()

    def apply_attributes_to_selected(self):
        nodes = [it for it in self.scene.selectedItems() if isinstance(it, NodeItem)]
        if not nodes:
            return
        fam = self.ui.font_combo.currentFont().family()
        size = self.ui.font_size.value()
        bold = self.ui.bold_chk.isChecked()
        italic = self.ui.italic_chk.isChecked()
        for node in nodes:
            font = node.text_item.font()
            font.setFamily(fam)
            font.setPointSize(size)
            font.setBold(bold)
            font.setItalic(italic)
            node.text_item.setFont(font)
