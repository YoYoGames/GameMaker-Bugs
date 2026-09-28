---
layout: home
---
# GMRT 0.22.0 

[Setup and installation guide](https://github.com/YoYoGames/GMRT-Beta/blob/main/docs/introduction/GMRT-intro-and-setup-instructions.md)

This version of GMRT brings with it some fixes, 3D Physics and shadowmapping. We strongly encourage you to upgrade to this version and try out any previously non-functioning projects you may have, as well as checking out some of the new features that have been included.

GMRT is incomplete, lots of work is still to be done but we are very keen to get your opinions early to make sure things are on the right track as we go forward. Please report issues and improvements you would like to see on new features (or old)
<hr>

### New GMRT Features Added

- **3D Physics**
    - You can get a sample that shows the functions and usage, as well as the documentation from [here](https://github.com/YoYoGames/GM3D-Samples/tree/develop)
	- This utilises [JoltPhysics](https://github.com/jrouwe/joltphysics)
		- Collisions
		- Trigger shapes
		- Rigid Bodies
		- Vehicles		
    - Currently there is no in-IDE syntax help, so the functions will not be present in autocomplete and there will be no parameter help or syntax highlighting
    
- **Shadowmapping**
	- You can get a sample that shows the functions and usage, as well as the documentation from [here](https://github.com/YoYoGames/GM3D-Samples/tree/develop)
		- Stable directional shadows for GM3D scenes, including support for static, skinned, and instanced meshes.
<br>



### Known Incompatibilities with GMS2 runtimes

- Prefabs
- Video playback (All platforms except Windows)
- SVG Assets
- flexpanel_node_get_measure() / flexpanel_node_set_measure()
- vertex_buffer_exists() / vertex_format_exists()
- application_surface_is_draw_enabled()


<br>

### Bugs Fixed

Public Milestone Changelog is [HERE](https://github.com/YoYoGames/GameMaker-Bugs/issues?q=is%3Aissue%20milestone%3A%22GMRT%200.22.0%22) for the complete list.
Some issues are detailed below:
- [Android] Exiting an app from an Android device does not stop sound and no longer crashes afterwards [#15389](https://github.com/YoYoGames/GameMaker-Bugs/issues/15389)
- Building Projects: [Android GMRT] is now able to run from Mac IDE when using v0.22.x [#15832](https://github.com/YoYoGames/GameMaker-Bugs/issues/15832)
- [Mac ARM] Fixed that macOS SDK path is not detected correctly [#15383](https://github.com/YoYoGames/GameMaker-Bugs/issues/15383)
- Fixed exceptions not listing line number [#12379](https://github.com/YoYoGames/GameMaker-Bugs/issues/12379)
- Fixed that debug overlays get squashed to the right side [#15360](https://github.com/YoYoGames/GameMaker-Bugs/issues/15360)
- Fixed that imGUI "ConfigFlagsGet" function misspelled [#15491](https://github.com/YoYoGames/GameMaker-Bugs/issues/15491)
- Using the new ImGui functions that create windows or other on-screen items in the create event results in a no longer crashes without error [#15452](https://github.com/YoYoGames/GameMaker-Bugs/issues/15452)
- In-Game (GMS2 and GMRT): Fixed that structs can take array literals as valid keys, which is rather cursed [#7473](https://github.com/YoYoGames/GameMaker-Bugs/issues/7473)
- Fixed [Android] Game does not use any of the images set in game options [#15394](https://github.com/YoYoGames/GameMaker-Bugs/issues/15394)
- Addressed using application_surface manual draw and image_xscale = -1 causing sprite to be not visible [#13242](https://github.com/YoYoGames/GameMaker-Bugs/issues/13242)
- Fixed `temp_directory`, `program_directory`, and `cache_directory` result different things compared to GMS2 RTs [#13984](https://github.com/YoYoGames/GameMaker-Bugs/issues/13984)
- In-Game: [GMRT] Fixed that sequences with "Unknown track type" leads to assertion failure [#14300](https://github.com/YoYoGames/GameMaker-Bugs/issues/14300)
- In-Game: [Windows GMRT] Layer element having a null Sprite causes no longer crashes in attached project [#14387](https://github.com/YoYoGames/GameMaker-Bugs/issues/14387)
- Fixed gpu_set_scissor errors [#15476](https://github.com/YoYoGames/GameMaker-Bugs/issues/15476)
- In-Game: [GMRT VM] no longer crashes when an instance inherits parent Step logic, is hidden every frame by another instance, and focus changes after a new instance is created [#15121](https://github.com/YoYoGames/GameMaker-Bugs/issues/15121)
- In-Game: [GMRT] Fixed that error message for read out of bounds DS grids is stating 'writing' not 'reading' [#15514](https://github.com/YoYoGames/GameMaker-Bugs/issues/15514)
- In-Game: [Windows GMRT] Corrected built-in 'room' variable returning 'false' when compared to its corresponding room asset [#14770](https://github.com/YoYoGames/GameMaker-Bugs/issues/14770)
- In-Game: [Windows GMRT] `dbg_add_font_glyphs()` fixed adding Chinese characters to debug overlays all show as "?" [#15126](https://github.com/YoYoGames/GameMaker-Bugs/issues/15126)
- Fixed `ds_list_destroy()` when the list contains a ds_map marked as a map no longer destroys the map [#14258](https://github.com/YoYoGames/GameMaker-Bugs/issues/14258)
- In-Game: [Ubuntu GMRT] `file_text_open_write()` fixed failed to create directory, due to "Read-only file system" error [#15333](https://github.com/YoYoGames/GameMaker-Bugs/issues/15333)
- `flexpanel_create_node()` resolved not support all the available properties, causing project builds to fail [#15245](https://github.com/YoYoGames/GameMaker-Bugs/issues/15245)
- `http_request()` buffer body can now be deleted in the HTTP Async event, differs from VM/YYC [#14224](https://github.com/YoYoGames/GameMaker-Bugs/issues/14224)
- `imgui.SelectionStorageSize()` fixed will error when "undefined" is used as second argument [#15447](https://github.com/YoYoGames/GameMaker-Bugs/issues/15447)
- `is_...()` fixed and `typeof()` methods return different results vs GMS2 [#11835](https://github.com/YoYoGames/GameMaker-Bugs/issues/11835)
- In-Game: [GMRT] `particle_get_info()` fixed output only -1 when asset is invalid instead of ref <asset> -1 [#15740](https://github.com/YoYoGames/GameMaker-Bugs/issues/15740)
- `sprite_add()` no longer crashes when given a base64 data URL [#15528](https://github.com/YoYoGames/GameMaker-Bugs/issues/15528)
- In-Game: [GMRT] `sprite_set_offset()` resolved not apply changes on the X Axis [#15365](https://github.com/YoYoGames/GameMaker-Bugs/issues/15365)
- In-Game: [Windows GMRT] `string_split()` no longer crashes when using "remove empty" option [#15236](https://github.com/YoYoGames/GameMaker-Bugs/issues/15236)
- In-Game: [Windows GMRT] `window_set_fullscreen()` fixed offsets window off screen with large resolutions [#14748](https://github.com/YoYoGames/GameMaker-Bugs/issues/14748)
- Fixed that calling room_restart or game_restart makes the whole window turn black for one frame [#7405](https://github.com/YoYoGames/GameMaker-Bugs/issues/7405)
- GMRT compat: Resolved rotated instances in flex panels not appear correctly [#15359](https://github.com/YoYoGames/GameMaker-Bugs/issues/15359)
- GMRT Compat: UI Layers no longer breaks depth-sorting [#15354](https://github.com/YoYoGames/GameMaker-Bugs/issues/15354)
- Fixed that `flexpanel_create_node()` with "display" set to none and containing a "layerElements" entry still triggers "error drawing sprite" messages [#14858](https://github.com/YoYoGames/GameMaker-Bugs/issues/14858)
- asset_add/`get()` corrected returning empty if an optional asset type is required [#15385](https://github.com/YoYoGames/GameMaker-Bugs/issues/15385)
- Fixed that std::filesystem::path struggles to deal with trailing \\ causing the correct path not to be returned [#15350](https://github.com/YoYoGames/GameMaker-Bugs/issues/15350)
- In-Game: [GMRT] Resolved debug information not output essential code location from the stack [#15423](https://github.com/YoYoGames/GameMaker-Bugs/issues/15423)

<br>