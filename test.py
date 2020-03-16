import catch as catch
from PIL import Image
from modules.project import Style

style = Style()

frame = style.paint(parameter_subject='Frame Number', parameter_request_input=True)

list_x = eval(open('data/neural_network_data/training_data_0.2-Build-51/training_data_0.2-Build-51_input' +
                   '/training_data_0.2-Build-51_frame_' + style.fit_number(frame, 10) +
                   '.nntd').read())
list_y = eval(open('data/neural_network_data/training_data_0.2-Build-51/training_data_0.2-Build-51_output' +
                   '/training_data_0.2-Build-51_frame_' + style.fit_number(frame, 10) +
                   '.nntd').read())

cache = 0

im_x = Image.new('RGB', (16, 16))
im_x_px = im_x.load()
for x in range(16):
    for y in range(16):
        im_x_px[x, y] = list_x[cache]
        cache += 1

cache = 0

im_y = Image.new('RGB', (32, 32))
im_y_px = im_y.load()
for x in range(32):
    for y in range(32):
        im_y_px[x, y] = list_y[cache]
        cache += 1

im_x.show()
im_y.show()