from modules.project import *


# algorythms.improve_1(style.paint(parameter_subject='Path to image', parameter_request_input=True))
algorythms.upscale_1('data/img/yuki_and_kurumi.jpg', 'yuki_and_kurumi_2x.jpg')
algorythms.upscale_1('data/img/yuki_and_kurumi_2x.jpg', 'yuki_and_kurumi_4x.jpg')
algorythms.improve_1('data/img/yuki_and_kurumi_2x.jpg', 'data/img/yuki_and_kurumi_2x_improved.jpg')
algorythms.improve_1('data/img/yuki_and_kurumi_4x.jpg', 'data/img/yuki_and_kurumi_4x_improved.jpg')
