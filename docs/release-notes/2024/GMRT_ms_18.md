---
layout: home
---
# GMRT Milestone 18

To access GMRT 0.18 you will need to download its packages inside `Package Manager` in the IDE. For more information on how to do this, please see [this guide on setting up for GMRT](https://github.com/YoYoGames/GMRT-Beta/blob/main/docs/introduction/GMRT-beta-intro-and-setup-instructions.md)

<br>

## Known Incompatibilities:

{% include important.html content="GMRT does handle types differently to the GMS2 runtimes - for example, if you are relying on true/false being 1/0 as a string you will encounter problems." %}

Additonally, projects which contain any of these features or functions will either not run or will cause a runtime error while running:

 - SVG Assets
 - UI Layers
 - Video
 - game_save()/game_load() (these two will never be implemented in GMRT)
 - show_debug_log()/show_message_asnyc()/show_question_async()
 - sphere_is_visible()
 - flexpanel_node_get_measure() / flexpanel_node_set_measure()
 - vertex_buffer_exists() / vertex_format_exists()
 - application_surface_is_draw_enabled()

<br>

## Added Support For These Features:

 - Collision functions now accept Objects, Instances, Tilemaps, and arrays containing any of these three, as a parameter
 - Text Layers in rooms
 - Gamepad input now accepted (gamepad_enumerate has not been implemented as it's legacy and Android-only)

<br>

## Added Support For These Functions:
 - `dbg_*` functions
   - while most functions are implemented, the views for Textures, Texturegroups, Flexpanels, Log and Memory are not yet implemented
 - `gc_*` functions
   - gc_get_stats is displayed in the game window. Note that the 'Collection time' stat will only ever be 0us as it measures the time taken by the separate collection thread, which is temporarily disabled in GMRT (where collection is, for now, performed on the main thread).
 - Open and save filename functions 
 - `file_*` functions (as mentioned above already, game_save/load() are legacy and will NOT be implemented in GMRT)
 - Added newer `physics_*` functions - physics_debug and physics_raycast
 - Added remaining `struct_*` functions struct_exists_from_hash and struct_remove_from_hash
 - SDF font rendering and its associated functions 
 - `scheduler_resolution_*` functions 
 - `external_*` functions 
 - `skeleton_*` functions
 - `sprite_add_*` functions 
 - `handle_*` functions 
 - `layer_text_*` functions 
 - `zip_*` functions 
 - `gif_*` functions
 - `screen_save_*` functions 
 - sprite_get_convex_hull()
 - buffer_get_used_size() 
 - http_set_connect_timeout()
 - timeline_moment_add_script()

<br>

## Misc Other Fixes:

 - Configurations were not being recognised
 - Corrected window size to match what the GMS2 runtime uses
 - Failing to render overriden objects with `sequence_instance_override_object()` [10898](https://github.com/YoYoGames/GameMaker-Bugs/issues/10898)
 - Tilemap collisions causing crashes [10904](https://github.com/YoYoGames/GameMaker-Bugs/issues/10904)
 - `image_index` not incremented for instances without sprites [11410](https://github.com/YoYoGames/GameMaker-Bugs/issues/11410)
 - `json_encode()` serialises ref as string instead of descending into provided map 
 - `os_get_info()` returns an empty map [10988](https://github.com/YoYoGames/GameMaker-Bugs/issues/10988)
 - Instance creation code does not work in Room Sub-Layers [11281](https://github.com/YoYoGames/GameMaker-Bugs/issues/11281)
 - Textures in dynamic texture groups do not get prefetched [11862](https://github.com/YoYoGames/GameMaker-Bugs/issues/11862)
 - `object_get_parent()` now functions in line with the documentation [11375](https://github.com/YoYoGames/GameMaker-Bugs/issues/11375)

<br>
