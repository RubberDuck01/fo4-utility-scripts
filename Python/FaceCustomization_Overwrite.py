import os
import shutil

def overwrite_textures(src_dir, dst_dir):
    my_textures = [f for f in os.listdir(src_dir) if f.endswith(('_d.dds', '_n.dds', '_s.dds'))]
    
    for subdir, _, files in os.walk(dst_dir):
        for file in files:
            if file.endswith(('_d.dds', '_n.dds', '_s.dds')):
                my_texture = next((t for t in my_textures if file.startswith(t[:-6])), None)
                if my_texture:
                    my_texture_path = os.path.join(src_dir, my_texture)
                    file_path = os.path.join(subdir, file)
                    shutil.copy(my_texture_path, file_path)
                    print(f'Replaced {my_texture_path} with {file_path}')
                    
my_textures_dir = 'MyTextures'
face_customization_dir = 'FaceCustomization'

overwrite_textures(my_textures_dir, face_customization_dir)