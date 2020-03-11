from PIL import Image
from modules.style import Style
import math
from tqdm import tqdm


class Algotythms:
    size = 2
    style_obj = Style()
    radius = 2
    project = None
    statistics = None
    
    def __init__(self, project_obj, statistics_obj):
        self.project = project_obj
        self.statistics = statistics_obj
        
    def upscale_1(self, path_to_image, output_name='output.jpg'):
        old_cache_img = Image.open(path_to_image)
        old_cache_img_width, old_cache_img_height = old_cache_img.size
        old_cache_img_px = old_cache_img.load()
        new_cache_img = Image.new('RGB', (old_cache_img_width * self.size, old_cache_img_height * self.size))
        new_cache_img_width, new_cache_img_height = new_cache_img.size
        new_cache_img_px = new_cache_img.load()
        self.style_obj.paint(new_cache_img.size, 'Tuple of new Image')

        upscale_progress = tqdm(total=(new_cache_img_height * new_cache_img_width),
                                position=0, leave=True, unit=' Pixel')

        self.project.log('Start upscaling of ' + path_to_image)

        for old_w in range(0, new_cache_img_width):
            for old_h in range(0, new_cache_img_height):
                if old_h % 2 == 0 and old_w % 2 == 0:
                    new_cache_img_px[old_w + 1, old_h + 1] = (
                        int((math.ceil(old_cache_img_px[old_w / 2, old_h / 2][0]) +
                             math.floor(old_cache_img_px[old_w / 2, old_h / 2][0])) / 2),
                        int((math.ceil(old_cache_img_px[old_w / 2, old_h / 2][1]) +
                             math.floor(old_cache_img_px[old_w / 2, old_h / 2][1])) / 2),
                        int((math.ceil(old_cache_img_px[old_w / 2, old_h / 2][2]) +
                             math.floor(old_cache_img_px[old_w / 2, old_h / 2][2])) / 2),
                    )
                    new_cache_img_px[old_w, old_h] = (
                        int((math.ceil(old_cache_img_px[old_w / 2, old_h / 2][0]) +
                             math.floor(old_cache_img_px[old_w / 2, old_h / 2][0])) / 2),
                        int((math.ceil(old_cache_img_px[old_w / 2, old_h / 2][1]) +
                             math.floor(old_cache_img_px[old_w / 2, old_h / 2][1])) / 2),
                        int((math.ceil(old_cache_img_px[old_w / 2, old_h / 2][2]) +
                             math.floor(old_cache_img_px[old_w / 2, old_h / 2][2])) / 2),
                    )
                else:
                    new_cache_img_px[old_w, old_h] = old_cache_img_px[old_w / 2, old_h / 2]

            upscale_progress.set_description('Upscaling ' + path_to_image.format(old_w))
            upscale_progress.update(new_cache_img_height)
        upscale_progress.close()
        self.style_obj.paint('data/img/' + output_name, 'Saving')
        new_cache_img.save('data/img/' + output_name)
        self.project.log('Finished upscaling of ' + path_to_image)
        self.project.log('New Image save to data/img/' + output_name)
        self.statistics.update_stat('Calculated Images', '+ 1')
        self.statistics.update_stat('Upscaled Images', '+ 1')
        # new_cache_img.show()

    def improve_1(self, path_to_image, save_name='output.jpg'):
        old_cache_image = Image.open(path_to_image)
        old_cache_image_px = old_cache_image.load()
        old_cache_image_width, old_cache_image_height = old_cache_image.size

        improve_progress = tqdm(total=(old_cache_image_height * old_cache_image_width),
                                position=0, leave=True, unit=' Pixel')

        new_cache_img = Image.new('RGB', (old_cache_image_width, old_cache_image_height))
        new_cache_img_width, new_cache_img_height = new_cache_img.size
        new_cache_img_px = new_cache_img.load()

        self.project.log('Start improving of ' + path_to_image)

        for w in range(0, old_cache_image_width, 2):
            for h in range(0, old_cache_image_height, 2):
                cache_color = [
                    old_cache_image_px[w, h][0] + old_cache_image_px[w + 1, h][0] +
                    old_cache_image_px[w, h + 1][0] + old_cache_image_px[w + 1, h + 1][0],
                    old_cache_image_px[w, h][1] + old_cache_image_px[w + 1, h][1] +
                    old_cache_image_px[w, h + 1][1] + old_cache_image_px[w + 1, h + 1][1],
                    old_cache_image_px[w, h][2] + old_cache_image_px[w + 1, h][2] +
                    old_cache_image_px[w, h + 1][2] + old_cache_image_px[w + 1, h + 1][2]
                ]
                cache_color = [
                    int(cache_color[0] / 4),
                    int(cache_color[1] / 4),
                    int(cache_color[2] / 4)
                ]
                new_cache_img_px[w, h] = (cache_color[0], cache_color[1], cache_color[2])
                new_cache_img_px[w + 1, h] = (cache_color[0], cache_color[1], cache_color[2])
                new_cache_img_px[w, h + 1] = (cache_color[0], cache_color[1], cache_color[2])
                new_cache_img_px[w + 1, h + 1] = (cache_color[0], cache_color[1], cache_color[2])
                # print(cache_color)
            improve_progress.set_description('Improving ' + path_to_image.format(w))
            improve_progress.update(old_cache_image_height * 2)
        improve_progress.close()
        self.style_obj.paint(save_name, 'Saving')
        self.project.log('Finished improving of ' + path_to_image)
        self.project.log('New Image save to ' + save_name)
        new_cache_img.save(save_name)
        self.statistics.update_stat('Calculated Images', '+ 1')
        self.statistics.update_stat('Improved Images', '+ 1')
        # new_cache_img.show()
