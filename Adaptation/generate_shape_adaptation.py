import os
from options.test_options import TestOptions
from data import CreateDataLoader
from models import create_model
from util.visualizer import save_images
from util import html


if __name__ == '__main__':
    opt = TestOptions().parse()
    opt.num_threads = 1   # test code only supports num_threads = 1
    opt.batch_size = 1  # test code only supports batch_size = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip
    opt.display_id = -1  # no visdom display
    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()
    model = create_model(opt)
    model.setup(opt)
    # create website
    web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.epoch))
    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))
    # test
    # Set eval mode.
    # This only affects layers like batch norm and dropout. But we do use batch norm in pix2pix.
    model.eval()
    for i, data in enumerate(dataset):
        if i >= opt.num_test:
            break
        #model.set_input(data, i)
        model.set_input_helen(data, i)
        model.test()
        img_path = model.get_image_paths()
        if i % 5 == 0:
            print('processing (%04d)-th image... %s' % (i, img_path))
