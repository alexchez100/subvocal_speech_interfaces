# Visual Word Sequence Application

This application is designed for visual word presentation with light sequence indicators. It's part of a subvocal speech interface research project.

## Features
- Sequential light activation with 6 indicator lights
- Random word display from a predefined word list
- CSV logging of all events with timestamps
- Skip functionality for marking specific trials
- Dark mode interface for better visibility
- Centered word display with large font

## Technical Details
- Built with Python and tkinter
- CSV output format: time, word, status
- Configurable display timing (currently 800ms between lights)
- Full screen display with Windows title bar

## Interface
- Word button: Starts new sequence
- Skip button: Marks last trial as skipped (status = 0)
- Light indicators: Gray → Green → Red sequence

😊

## Usage
1. Run the program
2. Enter file name when prompted
3. Press "Word" to start sequence
4. Use "Skip" if needed to mark trial