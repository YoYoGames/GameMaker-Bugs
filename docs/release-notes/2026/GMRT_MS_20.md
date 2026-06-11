---
layout: home
---
# GMRT 0.20.0 

[Setup and installation guide](https://github.com/YoYoGames/GMRT-Beta/blob/main/docs/introduction/GMRT-intro-and-setup-instructions.md)

This version of GMRT brings with it a lot of fixes, further compatibility with GMS2, a new target platform, and some completely new features. We strongly encourage you to upgrade to this version and try out any previously non-functioning projects you may have, as well as checking out some of the new features that have been included.

These features are incomplete, lots of work is still to be done but we are very keen to get your opinions early to make sure things are on the right track as we go forward.
<hr>

### New GMRT Features Added

- **GM3D Functions**
    - You can get a sample that shows the functions and usage, as well as the documenationt from [here](https://github.com/YoYoGames/GM3D-Samples)
    - This is an incomplete feature and we really want your feedback on this regarding the API, naming, bugs and any other feedback you may have
    - Currently there is no in-IDE syntax help, so the functions will not be present in autocomplete and there will be no parameter help or syntax highlighting
    - This pass introduces the following functionality:
        - 3D Maths
            - Vectors, Matrices, Quaternions
        - Model Loading
            - Mesh, Skinned Meshes, Animations, Skeletal Animations and Materials
            - Only glTF model loading support
        - Scene management
            - Cameras, Lighting and Environment settings
    - The full list of functions, attributes and struct information can be found in the GM3D_API.md file inside the example project

- **Android Target (aarch64 only for now)**
    - This [guide](https://gamemaker.io/en/help/articles/setting-up-for-android) still applies, but it is important to note that you require different SDK values
        - Android SDK 35 (android 15) follow the setup guide for how to use Android Studio to install Android SDKs / NDKs
        - Android NDK - 28.2.13676358
        - Gradle - [8.14.2](https://gradle.org/releases/#8.14.2)
    - You will also need to get the packages via package manager:
        - GMRT Runtime - aarch64-linux-android
        - Gmir2llvm-17.0.3 (you may notice a different gmir2llvm package, you need both for different targets, so do not assume that because you have a higher version you are good)
    - There are some known issues right now, this is not a complete feature and we look forward to feedback from you
        - OS Navigation & Status bar is always visible
        - Games do not display at correct resolution when started in portrait/landscape
        - Multi-touches are not detected
        - Exiting the game may cause an audio crash 

- **Collision functions that return arrays [#12391](https://github.com/YoYoGames/GameMaker-Bugs/issues/12391)**
	- Currently this also has no in IDE syntax help, so the functions will not be present in autocomplete and there will be no parameter help or syntax highlighting
	
<br>

### GMS2 Compatibility features added
- UI Layers
- Video playback (Windows only)
- layer_get_flexpanel_node() and layer_get_type() added
- particle_add and particle_delete functions
- outputting instances to a string will now correctly output the ref
- MRT (multiple render targets) are now handled correctly
- os_type, os_version, os_device and os_get_info() all implemented
- file handling has been improved to reduce platform-dependant issues
- Projects containing Scribble and Input libraries should now compile and run without issue
- More imGUI functions were added:
     - dbg_color / dbg_colour
     - dbg_drop_down
     - dbg_slider
     - dbg_slider_int
     - dbg_text
     - dbg_text_input
     - dbg_text_separator
     - dbg_watch
    

<br>

### Known Incompatibilities with GMS2 runtimes

- Prefabs
- Video playback (other platforms)
- SVG Assets
- flexpanel_node_get_measure() / flexpanel_node_set_measure()
- vertex_buffer_exists() / vertex_format_exists()
- application_surface_is_draw_enabled()
- Lots of error spam from SDL [4980](https://github.com/YoYoGames/GMRT/issues/4980) 

<br>

### Bugs Fixed

Public Milestone Changelog is [HERE](https://github.com/YoYoGames/GameMaker-Bugs/issues?q=is%3Aissue%20milestone%3A%22GMRT%200.20.0%22)
- A selection of fixes is shown below
- Many more fixes are also present, but the information is behind a private repository so a handful have been presented here also
    - Alpha-testing has been disabled by default to match GMS2 Runtime behaviour
    - array_sort is now quicker with large arrays [9448](https://github.com/YoYoGames/GameMaker-Bugs/issues/9448)
    - camera_get_proj_mat() returns correct value
    - direction no longer reset when speed is 0 [15020](https://github.com/YoYoGames/GameMaker-Bugs/issues/15020)
    - ds_grid_copy no longer mirrors the data in the destination grid
    - Filters+Effects:Parallax background now renders
    - GMRT no longer throws an exception after calling a gml function with optional arguments & omitting one or passing undefined
    - Growing a buffer beyond 2GB no longer crashes [14870](https://github.com/YoYoGames/GameMaker-Bugs/issues/14870)
    - gpu_pop_state() affects shader and texture uniforms used
    - gpu_set_cullmode() now implemented
    - Handling of spine textures with premultiplied alpha has been corrected
    - instance_id now returns the same as GMS2 target [14869](https://github.com/YoYoGames/GameMaker-Bugs/issues/14869)
    - legacy "other" behaviour no longer the default [10886](https://github.com/YoYoGames/GameMaker-Bugs/issues/10886)
    - matrix_set() now properly update all matrices
    - Memory leaks in sequence structs have been plugged
    - room_get_info() now returns ParticleSystem Layer element information [15112](https://github.com/YoYoGames/GameMaker-Bugs/issues/15112)
    - room_next() no longer crashes if there is only 1 room [15053](https://github.com/YoYoGames/GameMaker-Bugs/issues/15053)
    - Spine sprites now only use a collision mesh when selected in the sprite editor
    - surface_get_depth_disable() returns the correct value
    - templated strings with escaped brackets no longer cause formatting error [14220](https://github.com/YoYoGames/GameMaker-Bugs/issues/14220)
    - tilemap depth now affected by gpu_set_depth [15023](https://github.com/YoYoGames/GameMaker-Bugs/issues/15023)
    - WASM target now builds AND runs successfully again
    - window_mouse_set now actually moves the mouse position
    - Windows ARM64 machines can now target GMRT
- Multiple project specific issues were addressed, if you had problems running your project on GMRT please try again
