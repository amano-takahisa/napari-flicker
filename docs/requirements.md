# napari-flicker Plugin Requirements Specification

## Overview
The napari-flicker plugin provides a simple layer visibility toggle functionality that allows users to create a "flicker" effect by rapidly switching the visibility of selected layers at fixed intervals.

## Functional Requirements

### FR1: Layer Selection
- **FR1.1**: The plugin shall display a list of all loaded layers in the napari viewer
- **FR1.2**: Users shall be able to select multiple layers for flickering using checkboxes
- **FR1.3**: Only Image and Labels layer types shall be supported
- **FR1.4**: The layer list shall automatically update when layers are added or removed from the viewer

### FR2: Flicker Control
- **FR2.1**: Users shall be able to start flickering by clicking a "Start Flicker" button
- **FR2.2**: Users shall be able to stop flickering by clicking the same button (toggle behavior)
- **FR2.3**: The button text shall change to indicate current state ("Start Flicker" / "Stop Flicker")
- **FR2.4**: Flickering shall only affect layers that are currently selected via checkboxes

### FR3: Timing Behavior
- **FR3.1**: The flicker interval shall be fixed at 0.5 seconds (500ms)
- **FR3.2**: The flicker effect shall toggle layer visibility (on/off) at each interval
- **FR3.3**: All selected layers shall flicker simultaneously
- **FR3.4**: Flickering shall continue until manually stopped by the user

### FR4: User Interface
- **FR4.1**: The plugin shall be implemented as a napari widget
- **FR4.2**: The widget shall contain:
  - A scrollable list of layer checkboxes
  - A start/stop toggle button
- **FR4.3**: The interface shall be intuitive for general napari users
- **FR4.4**: The widget shall update automatically when napari layers change

## Non-Functional Requirements

### NFR1: Performance
- **NFR1.1**: The plugin shall not significantly impact napari performance
- **NFR1.2**: Flicker timing shall be accurate and consistent
- **NFR1.3**: The plugin shall handle up to 50 layers without performance degradation

### NFR2: Compatibility
- **NFR2.1**: The plugin shall be compatible with napari 0.6.x
- **NFR2.2**: The plugin shall work on Linux, Windows, and macOS
- **NFR2.3**: The plugin shall support Python 3.10+

### NFR3: Usability
- **NFR3.1**: The plugin interface shall be self-explanatory
- **NFR3.2**: The plugin shall provide visual feedback for user actions
- **NFR3.3**: The plugin shall handle edge cases gracefully (e.g., no layers selected)

## Technical Specifications

### Widget Architecture
- **Widget Type**: QWidget-based implementation for maximum control
- **Timer Implementation**: QTimer for precise interval control
- **Layer Management**: Direct napari viewer layer access
- **State Management**: Simple boolean state tracking for flicker status

### Layer Support
- **Supported Layer Types**:
  - `napari.layers.Image`
  - `napari.layers.Labels`
- **Unsupported Layer Types**:
  - Points, Shapes, Tracks, Vectors, Surface layers

### User Interface Components
- **Layer Selection**: QCheckBox widgets in a scrollable area
- **Control Button**: QPushButton with toggle behavior
- **Layout**: Vertical layout with grouped components

## Acceptance Criteria

### AC1: Basic Functionality
- [ ] User can select multiple Image/Labels layers using checkboxes
- [ ] Selected layers flicker (visibility toggle) at 0.5-second intervals
- [ ] Flicker can be started and stopped using a single button
- [ ] Unselected layers remain unaffected during flickering

### AC2: User Interface
- [ ] Layer list updates automatically when layers are added/removed
- [ ] Button text changes to reflect current state
- [ ] Interface is responsive and intuitive
- [ ] Plugin loads as a napari widget

### AC3: Edge Cases
- [ ] No error when no layers are selected and flicker is started
- [ ] Flicker stops gracefully when all selected layers are removed
- [ ] Plugin handles empty layer list appropriately
- [ ] Performance remains stable with multiple layers

### AC4: Integration
- [ ] Plugin integrates seamlessly with napari
- [ ] No conflicts with other napari functionality
- [ ] Plugin can be loaded via napari menu or command line

## Out of Scope

The following features are explicitly out of scope for the initial implementation:
- Adjustable flicker timing/speed
- Animation effects or transitions
- Frame-by-frame stepping
- Export functionality
- Synchronization with napari timeline
- Support for other layer types (Points, Shapes, etc.)
- Advanced timing controls (pause/resume separately)
- Memory of previous flicker sessions
- Keyboard shortcuts
- Multi-viewer support

## Future Enhancements

Potential future enhancements that could be considered:
- Adjustable flicker speed/timing
- Support for additional layer types
- Export flicker as animation
- Keyboard shortcuts for quick access
- Group-based layer management
- Preset flicker patterns
