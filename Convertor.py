from PIL import Image
import os

for i in range(6):
    for j in range(13):
        for k in range(13):
            old_path = os.path.join('images', 'room_{}'.format(i), 'wall_{}'.format(j), '{}.png'.format(k))
            new_path = os.path.join('images', 'room_{}'.format(i), 'wall_{}'.format(j), '{}.jpg'.format(k))
            im = Image.open(old_path)
            print("Opened ", old_path)
            rgb_im = im.convert('RGB')
            rgb_im.save(new_path)
            print("Saved ", new_path)
            os.system("rm {}".format(old_path))
            print("Deleted ", old_path)
