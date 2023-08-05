"""SPORTCARSBRAND9 small images classification dataset.
"""
import os
import shutil
import tarfile
import time

from keras.utils.data_utils import get_file


def load_data(target_dir='sport_cars_brand'):
    """Loads SPORTCARSBRAND9 dataset.
    # Returns
        Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.
    """
    dirname = '/tmp/sport-cars-brand-9'
    origin = 'https://sport-cars.s3-us-west-2.amazonaws.com/sport-cars-brand-9.tar.gz'

    st = time.time()
    path = get_file(dirname, origin=origin, untar=True)

    def tar_member(members):
        for tarinfo in members:
            yield tarinfo

    tar = tarfile.open(path + '.tar.gz')
    tar.extractall(members=tar_member(tar))
    tar.close()

    if os.path.isdir(target_dir):
        print('Deleting {} ...'.format(target_dir))
        shutil.rmtree(target_dir)
    if target_dir != 'sport_cars_brand':
        shutil.move('sport_cars_brand', target_dir)
    et = time.time()
    print('`sport_cars_brand` dataset downloaded to {}. Elapsed time: {} secs'.format(target_dir, (et - st)))
