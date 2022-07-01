import numpy as np
from PIL import Image
from tqdm import tqdm
from modules.Zest.Zest_Network import Zest_Network

class Zest_ImageProcessing(Zest_Network):

    square_size_HQ = 32
    square_size_LQ = 16

    def __init__(self, x, y) -> None:
        super().__init__(x, y)
    
    def process_image(self, image_path = None, image_pillow_obj = None):

        image_to_process = None
        image_to_output  = None

        # Prepare Image Object
        if image_path is not None:
            image_to_process = Image.open(image_path)
        elif image_pillow_obj is not None:
            if isinstance(image_pillow_obj, Image):
                image_to_process = image_pillow_obj
            else:
                # No Pillow Object
                return None
        else:
            # Nothing to work on
            return None

        # Start Processing Image

        # Crop image to fix the 16 x 16 squares
        image_to_process = image_to_process.crop(
            (
                0,
                0,
                (image_to_process.size[0] // 16) * 16,
                (image_to_process.size[1] // 16) * 16
            )
        )

        # Create a blank image to output the pixels
        image_to_output = Image.new(
            'RGB',
            (
                image_to_process.size[0] * 2,
                image_to_process.size[1] * 2
            )
        )

        for img_x in range(0, image_to_process.size[0], self.square_size_LQ):
            for img_y in range(0, image_to_process.size[1], self.square_size_LQ):
                # Convert Square Area to an readable array for the Network
                cache_square_LQ = []

                for square_x in range(img_x, (img_x) + 16):
                    for square_y in range(img_y, (img_y) + 16):
                        for color_value in image_to_process.getpixel((square_x, square_y)):
                            cache_square_LQ.append(color_value / 255)
                
                self.feed_forward(cache_square_LQ)
                # print(self.output.sum() / self.output.size, self.output.max())
                for pixel_color in range(0, len(self.output), 3):
                    # Recalculate where to put the pixel
                    pixel_y = ((pixel_color / 3) // self.square_size_HQ)
                    pixel_x = (pixel_color // 3) - (pixel_y * self.square_size_HQ)

                    # print(pixel_color, pixel_x, pixel_y, len(self.output), image_to_output.size, self.output[pixel_color])

                    image_to_output.putpixel(
                        (int(img_x * 2 + pixel_x), int(img_y * 2 + pixel_y)),
                        (
                            int(self.output[pixel_color]     * 255),
                            int(self.output[pixel_color + 1] * 255),
                            int(self.output[pixel_color + 2] * 255)
                        )
                    )
                # image_to_output.save('D:\\#Data\\shiro-output\\steps\\' + str(img_x) + '-' + str(img_y) + '.jpg')
        # input('hi')
        return image_to_output


        
