## Misc New Functions

- `asset_get_ids(asset_type)` - This function returns an array containing IDs of all existing assets of given type.
- `buffer_copy_stride(src_buffer,src_offset,src_size,src_stride,src_count,dest_buffer,dest_offset,dest_stride)` - This function can be used to copy multiple data entries from one buffer to another, with the ability to specify different strides between individual entries in both the source and the destination buffers. The function takes into account the types of both buffers. If a buffer has a fixed size or is not a wrap buffer, the copying process will stop when the read or write position exceeds the buffer's range. Initial read and write positions can be negative, in which case they are computed from the end of given buffer.
- `particle_exists(ind)` - With this function you can check to see if a particle system asset with the given index exists or not.
- `part_system_get_info(partsys)` - This function is used to retrieve information for the given particle system instance. You supply a particle system instance created with part_system_create() and the function returns a struct with the following variables:
- `vertex_update_buffer_from_buffer(dest_vbuff,dest_offset,src_buffer,[src_offset],[src_size])` - This function updates contents of a vertex buffer using data from a regular buffer. The vertex buffer must not be frozen!
- `vertex_update_buffer_from_vertex(dest_vbuff,dest_vert,src_vbuff,[src_vert],[src_vert_num])` - This function updates contents of a vertex buffer using contents of another vertex buffer. The vertex buffers must not be frozen!
- `vertex_format_get_info(format_id)` - This function is used to retrieve information for the given vertex format. You supply a vertex format index and the function returns a struct with the following variables:

## Misc New Variables

- `cache_directory` - This can be used to return the cache directory created for your game (including trailing  "\"). This directory will hold files and can be accessed while the game is running, but it may be removed by the system later.

## Misc New Structs

```
VertexFormatInfo { 
	stride : ,
	num_elements : ,
	elements : 
} 
```
	
``` 
VertexElementInfo { 
	usage : ,
	type : ,
	size : ,
	offset : 
} 
``` 
	
``` 
TileSetInfo { 
	width : The width of the whole tile set texture (in pixels).,
	height : The height of the whole tile set texture (in pixels).,
	texture : The texture ID.,
	tile_width : The width of a single tile (in pixels).,
	tile_height : The height of a single tile (in pixels).,
	tile_horizontal_separator : The number of pixels horizontally on each side of each tile (making the space between two tiles 2 * tile_horizontal_separator).,
	tile_vertical_separator : The number of pixels vertically on each side of each tile (making the space between two tiles 2 * tile_vertical_separator),
	tile_columns : The number of columns on each row of the tile set.,
	tile_count : The number of tiles.,
	frame_count : The number of frames of animation per animation.,
	frame_length_ms : The number of milliseconds for frame animation.,
	frames : A struct containing all the animation frames. Each tile number has a key in the struct, each entry is an array of the frames to use (each array should be frame_count long).
}
``` 

## Misc Changed Structs

```
TextTrack {  
	text : ,
	[new] wrap : ,
	[new] alignmentV : ,
	[new] alignmentH : ,
	[new] fontIndex : ,
	[new] effectsEnabled : ,
	[new] glowEnabled : ,
	[new] outlineEnabled : ,
	[new] dropShadowEnabled : 
}
```
```
ActiveTrack {  
	activeTracks : , 
	matrix : , 
	posx : , 
	posy : , 
	scalex : , 
	scaley : , 
	xorigin : , 
	yorigin : , 
	gain : , 
	pitch : , 
	width : , 
	height : , 
	imageindex : , 
	imagespeed : , 
	colorMultiply : , 
	colourMultiply : , 
	emitterIndex : , 
	track : , 
	parent : , 
	frameSizeX : , 
	frameSizeY : , 
	characterSpacing : , 
	lineSpacing : , 
	paragraphSpacing : ,
	[new] thickness : ,
	[new] coreColor : ,
	[new] coreColour : ,
	[new] glowStart : ,
	[new] glowEnd : ,
	[new] glowColor : ,
	[new] glowColour : ,
	[new] outlineDist : ,
	[new] outlineColor : ,
	[new] outlineColour : ,
	[new] shadowSoftness : ,
	[new] shadowOffsetX : ,
	[new] shadowOffsetY : ,
	[new] shadowColor : ,
	[new] shadowColour : ,
	[new] effectsEnabled : ,
	[new] glowEnabled : ,
	[new] outlineEnabled : ,
	[new] dropShadowEnabled : 
}
```

## Misc New Functions

- `xboxone_gamedisplayname_for_user(user)` - This function returns the "classic gamertag" of a locally signed in user or a player in the current game session. Replaced by xboxone_classic_gamertag_for_user().
- `xboxlive_gamedisplayname_for_user(user)` - This function returns the "classic gamertag" of a locally signed in user or a player in the current game session. Replaced by xboxone_classic_gamertag_for_user().
- `xboxlive_gamertag_for_user(user)` - This function returns the "classic gamertag" of a locally signed in user or a player in the current game session. Replaced by xboxone_classic_gamertag_for_user().
- `xboxone_classic_gamertag_for_user(user)` - This function returns the "classic gamertag" of a locally signed in user or a player in the current game session.
- `xboxone_modern_gamertag_for_user(user)` - This function returns the "modern gamertag" (excluding suffix) of a locally signed in user or a player in the current game session. If the player does not have a modern gamertag, the classic gamertag is returned instead.
- `xboxone_modern_gamertag_suffix_for_user(user)` - This function returns the "modern gamertag suffix" of a locally signed in user or a player in the current game session (e.g. "#1234"). If the player does not have a modern gamertag or the modern gamertag does not include a suffix, an emptry string is returned.
- `xboxone_unique_modern_gamertag_for_user(user)` - This function returns the "modern gamertag" (including suffix) of a locally signed in user or a player in the current game session. If the player does not have a modern gamertag, the classic gamertag is returned instead.
