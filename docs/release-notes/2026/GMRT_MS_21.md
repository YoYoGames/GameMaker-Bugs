---
layout: home
---
# GMRT 0.21.0 

[Setup and installation guide](https://github.com/YoYoGames/GMRT-Beta/blob/main/docs/introduction/GMRT-intro-and-setup-instructions.md)

This version of GMRT brings with it some fixes, and a huge improvement on our Dear IMGui implementation. We strongly encourage you to upgrade to this version and try out any previously non-functioning projects you may have, as well as checking out some of the new features that have been included.

GMRT is incomplete, lots of work is still to be done but we are very keen to get your opinions early to make sure things are on the right track as we go forward. Please report issues and improvements you would like to see on new features (or old)
<hr>

### New GMRT Features Added

- **ImGUI suite based on ImGM**
    - You can get a sample project that shows the functions and usage, as well as the documentation from [here](https://github.com/YoYoGames/ImGUI-Sample)
	- Some highlights:
		- Dockable windows
		- Trees
		- Tabs
		- Tables
		- Tooltips
		- Popups
		- Styling functions
		- Many more, there are about 200 new functions with this feature
    - Currently there is no in-IDE syntax help, so the functions will not be present in autocomplete and there will be no parameter help or syntax highlighting
    
<br>



### Known Incompatibilities with GMS2 runtimes

- Prefabs
- Video playback (other platforms)
- SVG Assets
- flexpanel_node_get_measure() / flexpanel_node_set_measure()
- vertex_buffer_exists() / vertex_format_exists()
- application_surface_is_draw_enabled()


<br>

### Bugs Fixed

Public Milestone Changelog is [HERE](https://github.com/YoYoGames/GameMaker-Bugs/issues?q=is%3Aissue%20milestone%3A%22GMRT%200.21.0%22)
- A sample of issues are listed here:
	- Various fixes to Android target
	- rectangle_in_rectangle() incorrectly returned 0 when the source rect is fully overlapped by the destination rect 
	- part_system_get_info() did not include "angle" or "colour"
	- A few project specific issues were addressed, please do report any issue you have with projects not working in GMRT
