import itertools
import statistics
import imagehash
import os
from PIL import Image

# Function to calculate Hamming distance
def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def compute_distances(hash_list):
    # Generate all pairs of strings
    pairs = itertools.combinations(hash_list, 2)

    distances = []
    equal_count = 0
    hamming_one_count = 0
    hamming_two_count = 0
    # Calculate the Hamming distance for each pair
    for pair in pairs:
        distance = hamming_distance(*pair)
        distances.append(distance)

        # Count distances that are equal or have a Hamming distance of 1
        if distance == 0:
            equal_count += 1
        elif distance == 1:
            hamming_one_count += 1
        elif distance == 2:
            hamming_two_count += 1

    return distances, equal_count, hamming_one_count, hamming_two_count

# Function to calculate summary statistics
def compute_statistics(distances):
    # Calculate mean, median, and standard deviation
    mean_distance = statistics.mean(distances)
    median_distance = statistics.median(distances)
    std_dev_distance = statistics.stdev(distances)
    
    return mean_distance, median_distance, std_dev_distance

# Test
# Iterate over all files in the subdirectory
hashes = []
for file in os.scandir('./0'):
    if file.is_file() and file.name.endswith(('.png', '.jpg', '.jpeg')):
        with Image.open(file.path) as img:
            # Compute the perceptual hash of the image
            hash = imagehash.average_hash(img)
            hash_str = str(hash)
            hashes.append(hash_str)

distances, equal_count, hamming_one_count, hamming_two_count = compute_distances(hashes)
mean_distance, median_distance, std_dev_distance = compute_statistics(distances)
print(f"Mean: {mean_distance}, Median: {median_distance}, Std Dev: {std_dev_distance}")
print(f"Equal count: {equal_count}, Hamming distance of 1 count: {hamming_one_count}, hamming 2 count: {hamming_two_count}")
print(f'Num of comparisons {len(distances)} number of hashes {len(hashes)}')
