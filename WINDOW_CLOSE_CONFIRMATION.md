# Window Close Confirmation Implementation

## Overview
This document describes the implementation of a confirmation dialog that appears when users try to close the application while the timer is running.

## Implementation Details

1. Added a window reference variable to the Api class to store the window object
2. Implemented an `is_timer_running` method to check if the timer is currently running
3. Implemented a `handle_close_event` method that:
   - Checks if the timer is running
   - Shows a confirmation dialog if the timer is running
   - Stops the timer and updates the session if the user confirms
   - Returns True to allow the window to close or False to prevent it
4. Modified the window creation code to:
   - Set confirm_close=False to disable the default confirmation
   - Store the window reference in the Api instance
   - Set up the on_closing event handler using window.events.closing

## Testing
The implementation was tested and confirmed to be working correctly. When the timer is running and the user tries to close the app, a confirmation dialog appears. If the user confirms, the timer is stopped and the session is updated before the app closes. If the user cancels, the app remains open.

This ensures that users don't accidentally lose their tracking data by closing the app while the timer is running.