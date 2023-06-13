import os
from PIL import Image
import imagehash
from collections import Counter
import matplotlib.pyplot as plt
import time
import hashlib

def check_image_hashes(directory):
    methods = [imagehash.phash, imagehash.dhash, imagehash.average_hash, imagehash.colorhash]
    #methods = [imagehash.average_hash]
    method_names = ['phash', 'dhash', 'average_hash', 'colorhash']
    #method_names = ['average_hash']

    for method, method_name in zip(methods, method_names):
        print(f'Using {method_name}:')
        start_time = time.time()
        all_distances = []
        md5_hashes = [] 
        totalimages = 0
        totaloutliers = 0
        avghamming = 0.0
        # Iterate over all subdirectories in the directory
        for subdir in os.scandir(directory):
            if subdir.is_dir():
                hashes = []
                # Iterate over all files in the subdirectory
                for file in os.scandir(subdir.path):
                    if file.is_file() and file.name.endswith(('.png', '.jpg', '.jpeg')):
                        with open(file.path, 'rb') as f:
                            data = f.read()
                            md5_hash = hashlib.md5(data).hexdigest()  # Compute the MD5 hash
                            if md5_hash in md5_hashes:
                                print(f'Duplicate image found: {file.path}')
                            else:
                                md5_hashes.append(md5_hash)
                        # Open the image file
                        with Image.open(file.path) as img:
                            # Compute the perceptual hash of the image
                            hash = method(img)
                            hashes.append(hash)
                            totalimages = totalimages + 1
                # Skip subdirectories that don't contain any image files
                if not hashes:
                    continue
                counter = Counter(hashes)
                # Find the most common hash and its count
                common_hash, common_count = counter.most_common(1)[0]
                # The number of outliers is the total number of images minus the count of the most common hash
                outliers = len(hashes) - common_count
                if outliers > 0:
                    print(f'There are {outliers} outliers in {subdir.path}.')
                    # Calculate the Hamming distance between the most common hash and each of the other hashes
                    distances = [common_hash - hash for hash in hashes if hash != common_hash]
                    all_distances.extend(distances)  # Add the distances to the list of all distances
                    for hash in hashes:
                        if hash != common_hash:
                            distance = common_hash - hash
                            totaloutliers = totaloutliers + 1
                            avghamming = avghamming + distance
                            print(f'Hamming distance between common hash and outlier: {distance}')
                            print(f'Common hash {common_hash}, outlier hash {hash}')

        # Create a histogram of all the Hamming distances
        plt.hist(all_distances, bins='auto')
        plt.title(f'Histogram of Hamming distances ({method_name})')
        plt.xlabel('Hamming distance')
        plt.ylabel('Frequency')

        # Save the plot as an image
        plt.savefig(f'histogram_{method_name}.png')
        plt.clf()  # Clear the current figure for the next plot
        end_time = time.time()
        print(f'Time taken by {method_name}: {end_time - start_time} seconds')
        print(f'Total images {totalimages} and total outliers {totaloutliers}, average hamming = {avghamming/totaloutliers}')


# Use the function on your directory
check_image_hashes('./')
