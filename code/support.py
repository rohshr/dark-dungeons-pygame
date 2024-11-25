from csv import reader
from os import walk
import pygame
# import pytmx
# from pytmx.util_pygame import load_pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []
    
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
            
    return surface_list

def get_image_surfaces(paths):
    surface_list = []
    
    for path in paths:
        image_surf = pygame.image.load(path).convert_alpha()
        surface_list.append(image_surf)
    
    return surface_list

# def get_layer(tmx_data):
#     # tile_images = []
#     for layer in tmx_data.visible_layers:
#         print(layer)
#         # if layer.name == layer_name and isinstance(layer, pytmx.TiledTileLayer):
#         #         # for x, y, gid in layer:
#         #         #     img = tmx_data.get_tile_image_by_gid(gid)
#         #         #     if img:
#         #         #         tile_images.append(img)
    
#         #     return layer 

