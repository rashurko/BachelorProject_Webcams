import cv2
import glob
from skimage import measure
import numpy as np
import sys

#base_folder = sys.argv[1]
base_folder = "Code/frames"
type = "png"
output = "clusters.dat"

threshold = 4


def find_clusters(data):
    clusters = []
    n_event = 0

    gray = cv2.cvtColor(data, cv2.COLOR_RGB2GRAY)
    gray = np.where(gray > (threshold * 3), gray, 0).reshape(data.shape[0], data.shape[1])

    labeled = measure.label(gray > threshold, background=False, connectivity=2)
    regions = measure.regionprops(labeled)

    for region in regions:
        # cm_x, cm_y, count, count_r, count_g, count_b, sum, sum_r, sum_g, sum_b
        '''
        cm_x = x coordinate of the center of mass of a cluster
        cm_y = y coordinate of the center of mass of a cluster
        count = area = total amount of pixels in a cluster (x2??)
        count_r = number of red pixels in a cluster
        count_g = number of green pixels in a cluster
        count_b = number of blue pixels in a cluster
        sum = total sum of pixel values in a cluster
        sum_r = total sum of red pixel values in a cluster
        sum_g = total sum of green pixel values in a cluster
        sum_b = total sum of blue pixel values in a cluster
        '''
        cluster = [0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0]
        cluster[2] = region.area
        for px in region.coords:
            y, x = px
            val = np.sum(data[y, x, :])
            cluster[0] += val * x
            cluster[1] += val * y

            # gray
            cluster[2] += 1
            cluster[6] += val

            # rgb
            if data[y, x, 0] > threshold:
                cluster[3] += 1
                cluster[7] += data[y, x, 0]
            if data[y, x, 1] > threshold:
                cluster[4] += 1
                cluster[8] += data[y, x, 1]
            if data[y, x, 2] > threshold:
                cluster[5] += 1
                cluster[9] += data[y, x, 2]

        cluster[0] /= cluster[6]
        cluster[1] /= cluster[6]
        clusters.append(cluster)

    return np.array(clusters)

folders = sorted(glob.glob(base_folder + '/*'))

for folder in folders:
    print(folder)

    files = sorted(glob.glob(folder + '/*.' + type))

    f_out = open(folder + '/' + output, 'w')
    f_out.write('# frame\tevent\tcm_x\tcm_y\tsize\tsize_r\tsize_g\tsize_b\tsum\tsum_r\tsum_g\tsum_b\n')

    n_frame = 0

    #events = []
    for img in files:
        if not img.endswith(type):
            continue

        print('\r' + str(n_frame) + ' / ' + str(len(files)), end="")
        data = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)

        clusters = find_clusters(data)
        n_cluster = 0
        for cluster in clusters:
            f_out.write(f'{n_frame}\t{n_cluster}')
            for i in range(len(cluster)):
                f_out.write(f'\t{cluster[i]}')
            f_out.write('\n')
            n_cluster += 1

        n_frame += 1
        #events.append(clusters[:,6])

    f_out.close()
    print('')
