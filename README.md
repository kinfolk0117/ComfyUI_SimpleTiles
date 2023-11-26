
# SimpleTiles

## TileSplit
Splits image into tiles. Overlap value decides how much overlap there is between tiles on y axis, x axis is calculated to have the same ratio to image height as y axis.

## TileMerge
Merge tiles into image. 

**Overlap** value decides how much overlap there is between tiles on y axis, x axis is calculated to have the same ratio to image height as y axis. Should be set to same value as used in TileSplit.

**Blend** value decides how many pixels the blending is done over. Should be less than overlap value. Blending is done linearly from 0 to 1 over the blend distance.

## TileCalc

Util to calculate final image size based on tile sizes and overlaps. 


