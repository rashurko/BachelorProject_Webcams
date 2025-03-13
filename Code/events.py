import cv2
import glob
from skimage import measure
import numpy as np
import os
import sys

threshold = 1

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

def process_folder(folder, dark_current_image, save_folder, type, output):
    files = sorted(glob.glob(folder + '/*.' + type))

    # Create results folder in the output directory with the combined folder name
    parent_folder_name = os.path.basename(os.path.dirname(folder))
    folder_name = os.path.basename(folder)
    combined_folder_name = f"{parent_folder_name}"
    results_folder = os.path.join(save_folder, combined_folder_name)
    os.makedirs(results_folder, exist_ok=True)

    f_out = open(os.path.join(results_folder, output), 'w')
    f_out.write('# frame\tevent\tcm_x\tcm_y\tsize\tsize_r\tsize_g\tsize_b\tsum\tsum_r\tsum_g\tsum_b\n')

    n_frame = 0

    for img in files:
        if not img.endswith(type):
            continue

        print('\r' + str(n_frame) + ' / ' + str(len(files)), end="")
        data = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)

        # Subtract the dark current image from the current frame
        data = cv2.subtract(data, dark_current_image)

        clusters = find_clusters(data)
        n_cluster = 0
        for cluster in clusters:
            f_out.write(f'{n_frame}\t{n_cluster}')
            for i in range(len(cluster)):
                f_out.write(f'\t{cluster[i]}')
            f_out.write('\n')
            n_cluster += 1

        n_frame += 1

    f_out.close()
    print('')

def process_folders(base_folder, save_folder, type, output):
    folders = sorted(glob.glob(base_folder + '/*' + '/*'))

    for folder in folders:
        if os.path.basename(folder) != "Result":
            continue

        print(folder)

        # Load the average dark current image from the results folder
        parent_folder_name = os.path.basename(os.path.dirname(folder))
        combined_folder_name = f"{parent_folder_name}"
        results_folder = os.path.join(save_folder, combined_folder_name)
        dark_current_image_path = os.path.join(results_folder, 'average_darkcurrent.png')
        dark_current_image = cv2.imread(dark_current_image_path)
        if dark_current_image is None:
            raise ValueError(f"Error: Could not open or find the dark current image at {dark_current_image_path}")
        dark_current_image = cv2.cvtColor(dark_current_image, cv2.COLOR_BGR2RGB)

        process_folder(folder, dark_current_image, save_folder, type, output)


