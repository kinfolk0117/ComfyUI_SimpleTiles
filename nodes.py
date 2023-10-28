import sys
import os

import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))


IMAGE_SIZE = 1472
TILE_SIZE = 768

# Splits an image in four tiles and returns them as a list
class TileSplit:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
            "image": ("IMAGE", ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "split"
    CATEGORY = "utils"

    def split(self, image):

        height, width = IMAGE_SIZE, IMAGE_SIZE

        tile_height, tile_width = TILE_SIZE, TILE_SIZE
        overlap = 64

        tiles = []
        for y in range(0, height-tile_height+1, tile_height-overlap):
            for x in range(0, width-tile_width+1, tile_width-overlap):
                tile = image[:, y:y+tile_height, x:x+tile_width, :]
                tiles.append(tile)

        # Convert tiles list to a tensor if needed
        tiles_tensor = torch.stack(tiles).squeeze(1)



        return  [tiles_tensor]

class TileMerge:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
            "images": ("IMAGE", ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "blend_tiles"
    CATEGORY = "utils"
    def blend_tiles(self, images):
        tiles = images
        overlap = 64
        tile_height = TILE_SIZE
        tile_width = TILE_SIZE
        # original_shape  (1, 3072, 2048, 3)
        original_shape = (1, IMAGE_SIZE, IMAGE_SIZE, 3)



        batch, height, width, channels = original_shape
        output = torch.zeros(original_shape, dtype=tiles.dtype)
        count = torch.zeros(original_shape, dtype=tiles.dtype)
        
        idx = 0
        for y in range(0, height-tile_height+1, tile_height-overlap):
            for x in range(0, width-tile_width+1, tile_width-overlap):
                tile = tiles[idx]
                
                # Create a weight matrix for blending
                weight_matrix = torch.ones((tile_height, tile_width, channels))
                for i in range(overlap):
                    weight = float(i) / overlap
                    weight_matrix[i, :, :] *= weight  # Top rows
                    weight_matrix[-(i + 1), :, :] *= weight  # Bottom rows
                    weight_matrix[:, i, :] *= weight  # Left columns
                    weight_matrix[:, -(i + 1), :] *= weight  # Right columns
                
                # Update the output and count tensors
                output[:, y:y+tile_height, x:x+tile_width, :] += tile * weight_matrix
                count[:, y:y+tile_height, x:x+tile_width, :] += weight_matrix
                
                idx += 1
        
        # Blend the output
        output /= count
        
        return [output]




NODE_CLASS_MAPPINGS = {
    "TileSplit": TileSplit,
    "TileMerge": TileMerge,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TileSplit": "TileSplit",
    "TileMerge": "TileMerge",
}
