import os
import shutil

def overwrite_textures(src_dir, dst_dir):
    texture_types = ['_d.dds', '_msn.dds', '_s.dds']
    
    for subdir, _, files in os.walk(dst_dir):
        for file in files:
            for texture_type in texture_types:
                if file.endswith(texture_type):
                    master_texture = 'basefemalehead' + texture_type
                    master_texture_path = os.path.join(src_dir, master_texture)
                    file_path = os.path.join(subdir, file)
                    shutil.copyfile(master_texture_path, file_path)
                    print(f'Replaced {file} with {master_texture} in {subdir}')
                    
my_textures_dir = 'MyTextures'
face_customization_dir = 'FaceCustomization'

overwrite_textures(my_textures_dir, face_customization_dir)