import imageio
import glob
import os
import ntpath
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

class ImageUtil:
    
    @staticmethod
    def convert_images_to_gif(path, duration):
        """
        Constructs an animated gif from the list of static images.

        :parameters:
            path (string): path to the file
            duration (int): the duration between frame in milliseconds
        """
        files = []
        filenames = os.listdir(path)
        filenames = [os.path.join(path, f) for f in filenames]
        filenames.sort(key=lambda x: os.path.getmtime(x))
        for a_file in filenames:
            if a_file.endswith(('.jpeg', '.png', '.gif')):
                files.append(a_file)
        
        images = list(map(lambda image: imageio.imread(image), files))

        outputfile = 'heatmaps_over.gif'
        imageio.mimsave(outputfile, images, duration=duration/1000)
        return outputfile
    
    @staticmethod
    def convert_images_to_gif_2(path, duration):
        image_folder = os.fsencode(path)
        filenames = []
        for filename in os.listdir(image_folder):
            filename = os.fsdecode(filename)
            if filename.endswith( ('.jpeg', '.png', '.gif') ):
                filename = os.path.join(path, filename)
                filenames.append(filename)
        
        days = ['Saturday, April 07 2012', 'Sunday, April 08 2012', 'Monday, April 09 2012', 'Tuesday, April 10 2012', 'Wednesday, April 11 2012', 'Thursday, April 12 2012', 'Friday, April 13 2012']
        indices = range(0, len(filenames))
        for image, index in zip(filenames, indices):
            img = Image.open(image)
            draw = ImageDraw.Draw(img)

            image_name ='{0}    Hour: {1}'.format(days[(int)(index / 24)], index % 24)
            print(image_name)

            draw.text((0, 30), image_name, (0,0,0), font=ImageFont.truetype("arial", size=44))
            img.save(image, 'png')
        
        outputfile = 'heatmaps_over.gif'
        imageio.mimsave(outputfile, filenames, duration=duration/1000)
        return outputfile
