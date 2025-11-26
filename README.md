# Custom Nautilus (for GNOME 42)
## Features

1.  **Parent Directory Button:**
    *   Restores the classic "Up" arrow button in the main toolbar, allowing one-click navigation to the parent folder.
    *   Placed conveniently next to the Back/Forward buttons.

2.  **Live Session Tracking:**
    *   Automatically tracks the location of every open Nautilus window in real-time.
    *   Enables **View Open Folders** functionality: You can view all your open folders windows and their Workspaces using the included Python script.
    *   Self-cleaning: When you close a window, it is automatically removed from the tracker.

## How to Use

*   **Normal Usage:** Launch Nautilus as usual. The "Up" button will appear automatically.
*   **Display Live Session:** ``` python track_nautilus.py ```
  
## Technical Implementation (Short)

*   **UI Modification:** The "Up" button was injected into `src/resources/ui/nautilus-toolbar.ui`, linking to the internal `win.up` action.
*   **C Code Logic:** `src/nautilus-window-slot.c` was patched to:
    *   **Write:** Save the current X11 Window ID (XID) and Path to a temporary file in `/run/user/$UID/nautilus-tracker/` whenever the folder changes.
    *   **Delete:** Detect when a window (or its last tab) is closing and immediately delete the corresponding tracker file.
*   **Backend:** The application is forced to run with `GDK_BACKEND=x11` to ensure valid Window IDs are available for workspace matching.
*   

# nautilus
[![Pipeline status](https://gitlab.gnome.org/GNOME/nautilus/badges/master/pipeline.svg)](https://gitlab.gnome.org/GNOME/nautilus/commits/master)

This is the project of the [Files](https://wiki.gnome.org/Apps/Files) app, a file browser for
GNOME, internally known by its historical name `nautilus`.

## Supported version
Only latest version of Files as provided upstream is supported. Try out the [Flatpak nightly](https://wiki.gnome.org/Apps/Nightly) installation before filling issues to ensure the installation is reproducible and doesn't have downstream changes on it. In case you cannot reproduce in the nightly installation, don't hesitate to file an issue in your distribution. This is to ensure the issue is well triaged and reaches the proper people.

## Hacking on nautilus

To build the development version of the Files app and hack on the code
see the [general guide](https://wiki.gnome.org/Newcomers/BuildProject)
for building GNOME apps with Flatpak and GNOME Builder.

## Runtime dependencies
- [Bubblewrap](https://github.com/projectatomic/bubblewrap) installed. Used for security reasons.
- [Tracker (including tracker-miners)](https://gitlab.gnome.org/GNOME/tracker) properly set up and with all features enabled. Used for fast search and metadata extraction, starred files and batch renaming.

## Discourse

For more informal discussion we use [GNOME Discourse](https://discourse.gnome.org/tags/nautilus) in the Applications category with the `nautilus` tag. Feel free to open a topic there.

## How to report issues

Report issues to the GNOME [issue tracking system](https://gitlab.gnome.org/GNOME/nautilus/issues).
