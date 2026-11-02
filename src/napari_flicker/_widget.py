"""
This module contains the Flicker Widget.

References:
- Widget specification: https://napari.org/stable/plugins/building_a_plugin/guides.html#widgets
"""

from typing import TYPE_CHECKING, Dict, List

from qtpy.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QCheckBox,
    QScrollArea,
    QLabel,
)
from qtpy.QtCore import QTimer

if TYPE_CHECKING:
    import napari


class FlickerWidget(QWidget):
    """Main widget for napari-flicker plugin."""

    def __init__(self, viewer: 'napari.viewer.Viewer'):
        super().__init__()
        self.viewer = viewer
        self.layer_checkboxes: List[QCheckBox] = []

        # Layer visibility captured when flicker starts, restored on stop
        self._initial_visibility: Dict['napari.layers.Layer', bool] = {}

        # Setup timer for flicker functionality
        self.flicker_timer = QTimer()
        self.flicker_timer.setInterval(500)  # 500ms interval
        self.flicker_timer.timeout.connect(self._flicker_tick)

        # Setup UI components
        self._setup_ui()

        # Connect to layer events for automatic updates
        self.viewer.layers.events.inserted.connect(self._on_layers_changed)
        self.viewer.layers.events.removed.connect(self._on_layers_changed)

        # Initial layer list update
        self._update_layer_list()

    def _setup_ui(self):
        """Initialize the user interface components."""
        layout = QVBoxLayout()

        # Title
        title_label = QLabel('napari-flicker')
        layout.addWidget(title_label)

        # Layer selection area
        layers_header = QHBoxLayout()
        layers_header.addWidget(QLabel('Available Layers:'))
        self.refresh_button = QPushButton('Refresh Layers')
        self.refresh_button.setToolTip('Reload the layer list from the viewer')
        self.refresh_button.clicked.connect(self._update_layer_list)
        layers_header.addWidget(self.refresh_button)
        layout.addLayout(layers_header)

        # Scrollable area for layer checkboxes
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(2)  # Reduce spacing between items
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Toggle button
        self.toggle_button = QPushButton('Start Flicker')
        self.toggle_button.clicked.connect(self._toggle_flicker)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)

    def _get_supported_layers(self):
        """Get Image, Labels, Shapes and Points layers in reverse order."""
        import napari

        supported_types = (
            napari.layers.Image,
            napari.layers.Labels,
            napari.layers.Shapes,
            napari.layers.Points,
        )
        return [
            layer
            for layer in reversed(self.viewer.layers)
            if isinstance(layer, supported_types)
        ]

    def _update_layer_list(self):
        """Update the layer checkbox list, keeping checked layers checked."""
        checked_names = {
            checkbox.text()
            for checkbox in self.layer_checkboxes
            if checkbox.isChecked()
        }

        # Clear existing checkboxes
        for checkbox in self.layer_checkboxes:
            checkbox.setParent(None)
            checkbox.deleteLater()
        self.layer_checkboxes.clear()

        # Add checkboxes for supported layers
        supported_layers = self._get_supported_layers()
        for layer in supported_layers:
            checkbox = QCheckBox(layer.name)
            checkbox.setChecked(layer.name in checked_names)
            self.layer_checkboxes.append(checkbox)
            self.scroll_layout.addWidget(checkbox)

    def _on_layers_changed(self, event):
        """Handle layer list changes."""
        self._update_layer_list()

    def _get_selected_layers(self):
        """Get layers that are currently selected via checkboxes."""
        selected_layers = []
        supported_layers = self._get_supported_layers()

        for i, checkbox in enumerate(self.layer_checkboxes):
            if checkbox.isChecked() and i < len(supported_layers):
                selected_layers.append(supported_layers[i])

        return selected_layers

    def _toggle_flicker(self):
        """Toggle the flicker functionality on/off."""
        if self.flicker_timer.isActive():
            # Stop flicker and restore the visibility captured at start
            self.flicker_timer.stop()
            self._restore_visibility()
            self.toggle_button.setText('Start Flicker')
        else:
            # Start flicker only if layers are selected
            selected_layers = self._get_selected_layers()
            if selected_layers:
                self._initial_visibility = {
                    layer: layer.visible for layer in selected_layers
                }
                self.flicker_timer.start()
                self.toggle_button.setText('Stop Flicker')
            # If no layers selected, do nothing (button stays "Start Flicker")

    def _restore_visibility(self):
        """Restore layer visibility captured when flicker started."""
        for layer, visible in self._initial_visibility.items():
            if layer in list(self.viewer.layers):
                layer.visible = visible
        self._initial_visibility = {}

    def _flicker_tick(self):
        """Toggle visibility of selected layers."""
        selected_layers = self._get_selected_layers()
        for layer in selected_layers:
            layer.visible = not layer.visible
