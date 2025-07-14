# napari-flicker Plugin Development Plan

## Project Overview
This document outlines the development plan for the napari-flicker plugin, a napari widget that provides layer visibility flickering functionality. The project follows Test Driven Development (TDD) methodology to ensure high code quality, maintainability, and comprehensive test coverage.

## Development Methodology

### Test Driven Development (TDD)
All development follows the TDD Red-Green-Refactor cycle:

1. **Red**: Write a failing test that defines the desired functionality
2. **Green**: Write the minimal code to make the test pass
3. **Refactor**: Improve code quality while keeping tests green

### TDD Benefits
- **Higher Code Quality**: Tests drive better design decisions
- **Comprehensive Coverage**: Every feature has corresponding tests
- **Regression Prevention**: Immediate feedback when changes break existing functionality
- **Documentation**: Tests serve as living documentation of expected behavior
- **Confidence**: Safe refactoring with comprehensive test safety net

## Development Phases

### Phase 1: Core Widget Implementation (Priority: High)
**TDD Approach**: Write tests first for each component, then implement functionality.

**Deliverables**:
- Replace template widget with FlickerWidget class
- Implement basic UI components (layer list, toggle button)
- Add QTimer for flicker timing control
- Basic layer visibility toggle functionality

**Key Tasks (TDD Cycle)**:
- [ ] Write test for FlickerWidget class initialization
- [ ] Implement FlickerWidget class in `_widget.py`
- [ ] Write test for layer detection and filtering (Image/Labels only)
- [ ] Implement layer detection and filtering
- [ ] Write test for QCheckBox list for layer selection
- [ ] Implement QCheckBox list for layer selection
- [ ] Write test for start/stop toggle button
- [ ] Implement start/stop toggle button
- [ ] Write test for QTimer with 500ms interval
- [ ] Implement QTimer with 500ms interval
- [ ] Write test for layer visibility toggle logic
- [ ] Implement layer visibility toggle logic

### Phase 2: Integration and Polish (Priority: High)
**TDD Approach**: Write integration tests first, then implement integration features.

**Deliverables**:
- Proper napari plugin integration
- Error handling and edge cases
- UI improvements and responsiveness

**Key Tasks (TDD Cycle)**:
- [ ] Write test for napari.yaml widget configuration
- [ ] Update napari.yaml widget configuration
- [ ] Write tests for error handling edge cases
- [ ] Implement error handling for edge cases
- [ ] Write test for automatic layer list updates
- [ ] Implement automatic layer list updates
- [ ] Write test for user feedback and state indicators
- [ ] Add user feedback and state indicators
- [ ] Clean up template code and imports

### Phase 3: Testing and Validation (Priority: High)
**TDD Approach**: Since tests are written throughout development, this phase focuses on test completion and validation.

**Deliverables**:
- Complete test suite validation
- Performance and edge case testing
- Cross-platform compatibility verification

**Key Tasks**:
- [ ] Review and complete unit test coverage (target >95%)
- [ ] Validate all integration tests with napari
- [ ] Enhance edge case and error condition tests
- [ ] Add performance tests with multiple layers
- [ ] Add cross-platform compatibility tests
- [ ] Verify TDD test quality and maintainability

### Phase 4: Documentation and Cleanup (Priority: Medium)
**Deliverables**:
- Updated README with usage instructions
- Code documentation and comments
- Example usage scenarios

**Key Tasks**:
- [ ] Update README.md with plugin usage
- [ ] Add docstrings to all methods
- [ ] Create usage examples
- [ ] Update napari.yaml descriptions
- [ ] Clean up unused template code

## Technical Architecture

### Code Organization
```
src/napari_flicker/
├── __init__.py           # Plugin entry point
├── _widget.py            # FlickerWidget implementation
├── _version.py           # Version management
├── napari.yaml           # Plugin manifest
└── _tests/
    └── test_flicker.py   # Test suite
```

### Core Components

#### FlickerWidget Class
**File**: `src/napari_flicker/_widget.py`
```python
class FlickerWidget(QWidget):
    """Main widget for napari-flicker plugin."""

    def __init__(self, viewer: napari.viewer.Viewer)
    def _setup_ui(self)                    # UI initialization
    def _update_layer_list(self)           # Layer list management
    def _toggle_flicker(self)              # Start/stop flicker
    def _flicker_tick(self)                # Timer callback
    def _get_supported_layers(self)        # Filter Image/Labels layers
```

#### Key Technical Decisions
- **Widget Framework**: QWidget for maximum control and simplicity
- **Timer Implementation**: QTimer for precise 500ms intervals
- **Layer Management**: Direct napari viewer layer access
- **State Management**: Simple boolean flags for flicker state
- **UI Framework**: PyQt5/PySide2 via qtpy for compatibility

### Data Flow
1. **Initialization**: Widget connects to napari viewer
2. **Layer Detection**: Scan viewer for Image/Labels layers
3. **UI Update**: Populate checkbox list with available layers
4. **User Selection**: User selects layers via checkboxes
5. **Flicker Control**: User starts/stops flicker via button
6. **Timer Loop**: QTimer toggles visibility of selected layers
7. **State Management**: Track flicker state and selected layers

### Error Handling Strategy
- **No Layers Selected**: Show informative message, no error
- **All Selected Layers Removed**: Gracefully stop flicker
- **Empty Layer List**: Show "No supported layers" message
- **Timer Errors**: Fallback to stop flicker state
- **Layer Access Errors**: Skip problematic layers, continue with others

## Implementation Details

### Layer Management
```python
def _get_supported_layers(self):
    """Get Image and Labels layers from viewer."""
    supported_types = (napari.layers.Image, napari.layers.Labels)
    return [layer for layer in self.viewer.layers
            if isinstance(layer, supported_types)]
```

### Flicker Logic
```python
def _flicker_tick(self):
    """Toggle visibility of selected layers."""
    selected_layers = self._get_selected_layers()
    for layer in selected_layers:
        layer.visible = not layer.visible
```

### UI Layout
```
┌─────────────────────────────────┐
│ napari-flicker                  │
├─────────────────────────────────┤
│ Available Layers:               │
│ ☑ Image Layer 1                │
│ ☐ Labels Layer 1               │
│ ☑ Image Layer 2                │
│ ☐ Labels Layer 2               │
├─────────────────────────────────┤
│ [Start Flicker]                 │
└─────────────────────────────────┘
```

## TDD Testing Strategy

### Test-First Development Approach
Following TDD principles, all code is developed using the Red-Green-Refactor cycle:

#### Red Phase (Write Failing Tests)
- Define expected behavior through tests
- Write minimal test code that fails
- Ensure test failure is for the right reason

#### Green Phase (Make Tests Pass)
- Write the simplest code to make tests pass
- Focus on functionality, not optimization
- Ensure all tests pass

#### Refactor Phase (Improve Code Quality)
- Clean up code while maintaining test coverage
- Optimize performance and readability
- Ensure tests continue to pass

### Test Categories

#### Unit Tests (Written First)
- **Layer Detection**: Test filtering of supported layer types
- **UI Components**: Test checkbox and button functionality
- **Timer Logic**: Test flicker timing and state management
- **Error Handling**: Test edge cases and error conditions
- **State Management**: Test internal state transitions

#### Integration Tests (Written First)
- **Napari Integration**: Test widget loading and viewer interaction
- **Layer Management**: Test with dynamic layer addition/removal
- **State Synchronization**: Test UI state vs actual layer visibility
- **Plugin Lifecycle**: Test plugin initialization and cleanup

#### Test Quality Standards
- **Coverage Target**: >95% line coverage
- **Test Isolation**: Each test is independent and can run alone
- **Fast Execution**: Unit tests complete in <1s, integration tests <5s
- **Clear Naming**: Test names clearly describe what is being tested
- **Documentation**: Tests serve as specification documentation

### TDD Testing Scenarios
1. **Test-Driven Feature Development**: Write test for feature before implementation
2. **Bug-Driven Testing**: Write test that reproduces bug before fixing
3. **Regression Testing**: Existing tests prevent breaking changes
4. **Refactoring Safety**: Tests enable safe code improvements

## Risk Assessment

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Timer precision issues | Low | Medium | Use QTimer, test timing accuracy |
| Layer access errors | Medium | Low | Add error handling, graceful fallback |
| Performance with many layers | Medium | Medium | Optimize layer iteration, add limits |
| napari API changes | Low | High | Pin napari version, monitor updates |

### Development Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | Medium | Medium | Strict adherence to requirements |
| Testing complexity | Low | Medium | Focus on core functionality tests |
| Documentation gaps | Medium | Low | Regular documentation updates |

## Performance Considerations

### Optimization Targets
- **Layer List Updates**: Only update when layers change
- **Timer Efficiency**: Minimize work in timer callback
- **Memory Usage**: Avoid storing unnecessary layer references
- **UI Responsiveness**: Keep UI updates lightweight

### Performance Metrics
- **Flicker Accuracy**: ±10ms timing precision
- **Layer Limit**: Support up to 50 layers without degradation
- **Memory Usage**: <10MB additional memory usage
- **UI Responsiveness**: <100ms response to user actions

## Dependencies

### Required Dependencies
- **napari**: ≥0.6.0 (core napari functionality)
- **qtpy**: (Qt abstraction layer)
- **PyQt5/PySide2**: (GUI framework, via napari)

### Development Dependencies
- **pytest**: Testing framework
- **pytest-qt**: Qt testing utilities
- **pytest-cov**: Coverage reporting
- **pre-commit**: Code formatting and linting


## Success Criteria

### Technical Success
- [ ] All functional requirements implemented using TDD
- [ ] Test coverage >95% (TDD ensures high coverage)
- [ ] No critical bugs or errors
- [ ] Performance meets targets
- [ ] Code follows napari plugin best practices
- [ ] All features developed with test-first approach
- [ ] Comprehensive test suite serves as living documentation

### User Experience Success
- [ ] Intuitive interface requiring no documentation
- [ ] Responsive and reliable flicker functionality
- [ ] Graceful handling of edge cases
- [ ] Seamless integration with napari workflow

## Future Roadmap

### Version 1.1 (Optional)
- Adjustable flicker speed
- Keyboard shortcuts
- Enhanced error messages

### Version 1.2 (Optional)
- Support for additional layer types
- Group-based layer management
- Export flicker as animation

### Version 2.0 (Optional)
- Multi-viewer support
- Advanced timing patterns
- Plugin API for extensibility
