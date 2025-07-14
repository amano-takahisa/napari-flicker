import numpy as np
from qtpy.QtWidgets import QCheckBox, QPushButton, QVBoxLayout
from qtpy.QtCore import QTimer

from napari_flicker._widget import FlickerWidget


def test_flicker_widget_initialization(make_napari_viewer):
    """Test FlickerWidget initializes correctly with required components."""
    viewer = make_napari_viewer()
    widget = FlickerWidget(viewer)

    # Test basic widget properties
    assert widget.viewer is viewer
    assert hasattr(widget, 'flicker_timer')
    assert isinstance(widget.flicker_timer, QTimer)
    assert widget.flicker_timer.interval() == 500
    assert not widget.flicker_timer.isActive()

    # Test UI components exist
    assert hasattr(widget, 'toggle_button')
    assert isinstance(widget.toggle_button, QPushButton)
    assert widget.toggle_button.text() == 'Start Flicker'

    assert hasattr(widget, 'layer_checkboxes')
    assert isinstance(widget.layer_checkboxes, list)

    # Test layout
    assert isinstance(widget.layout(), QVBoxLayout)


def test_flicker_widget_layer_detection(make_napari_viewer):
    """Test layer detection and filtering for Image/Labels only."""
    viewer = make_napari_viewer()

    # Add different types of layers
    viewer.add_image(np.random.random((100, 100)), name='Image 1')
    viewer.add_labels(np.random.randint(0, 5, (100, 100)), name='Labels 1')
    viewer.add_points(np.random.random((10, 2)), name='Points 1')

    widget = FlickerWidget(viewer)

    # Test _get_supported_layers method
    supported_layers = widget._get_supported_layers()
    assert len(supported_layers) == 2
    assert supported_layers[0].name == 'Labels 1'
    assert supported_layers[1].name == 'Image 1'


def test_flicker_widget_ui_update(make_napari_viewer):
    """Test UI updates when layers are added/removed."""
    viewer = make_napari_viewer()
    widget = FlickerWidget(viewer)

    # Initially no layers
    assert len(widget.layer_checkboxes) == 0

    # Add layers
    viewer.add_image(np.random.random((100, 100)), name='Image 1')
    viewer.add_labels(np.random.randint(0, 5, (100, 100)), name='Labels 1')

    # Update UI
    widget._update_layer_list()

    # Check checkboxes created
    assert len(widget.layer_checkboxes) == 2
    assert all(isinstance(cb, QCheckBox) for cb in widget.layer_checkboxes)
    assert widget.layer_checkboxes[0].text() == 'Labels 1'
    assert widget.layer_checkboxes[1].text() == 'Image 1'


def test_flicker_widget_toggle_button(make_napari_viewer):
    """Test start/stop toggle button functionality."""
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((100, 100)), name='Image 1')

    widget = FlickerWidget(viewer)
    widget._update_layer_list()

    # Initially stopped
    assert widget.toggle_button.text() == 'Start Flicker'
    assert not widget.flicker_timer.isActive()

    # Select a layer and start
    widget.layer_checkboxes[0].setChecked(True)
    widget._toggle_flicker()

    # Should be started
    assert widget.toggle_button.text() == 'Stop Flicker'
    assert widget.flicker_timer.isActive()

    # Stop again
    widget._toggle_flicker()
    assert widget.toggle_button.text() == 'Start Flicker'
    assert not widget.flicker_timer.isActive()


def test_flicker_widget_layer_visibility_toggle(make_napari_viewer):
    """Test layer visibility toggle logic."""
    viewer = make_napari_viewer()
    img_layer = viewer.add_image(np.random.random((100, 100)), name='Image 1')
    label_layer = viewer.add_labels(
        np.random.randint(0, 5, (100, 100)), name='Labels 1'
    )

    widget = FlickerWidget(viewer)
    widget._update_layer_list()

    # Select both layers
    widget.layer_checkboxes[0].setChecked(True)
    widget.layer_checkboxes[1].setChecked(True)

    # Initial visibility
    initial_img_visible = img_layer.visible
    initial_label_visible = label_layer.visible

    # Toggle visibility
    widget._flicker_tick()

    # Check visibility was toggled
    assert img_layer.visible != initial_img_visible
    assert label_layer.visible != initial_label_visible

    # Toggle again
    widget._flicker_tick()

    # Should be back to original state
    assert img_layer.visible == initial_img_visible
    assert label_layer.visible == initial_label_visible


def test_flicker_widget_no_layers_selected(make_napari_viewer):
    """Test behavior when no layers are selected."""
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((100, 100)), name='Image 1')

    widget = FlickerWidget(viewer)
    widget._update_layer_list()

    # Don't select any layers
    widget._toggle_flicker()

    # Should not start flicker
    assert widget.toggle_button.text() == 'Start Flicker'
    assert not widget.flicker_timer.isActive()


# Legacy test for compatibility
def test_flicker_widget(make_napari_viewer, capsys):
    """Legacy test for compatibility."""
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((100, 100)))

    my_widget = FlickerWidget(viewer)

    # This test may need updating based on new implementation
    # For now, just test that widget can be created
    assert my_widget.viewer is viewer
