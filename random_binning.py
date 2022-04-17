import sys
import numpy as np
import time
import json
from math import ceil, log, floor


def compute_shift(n, coordinates, bit):
    length = len(coordinates)
    if bit == "all_ones":
        a = np.ones(length, dtype=int)
    else:
        a = np.arange(length)
        a = np.floor(a / (2 ** bit))
        a = (1 - (-1) ** a) / 2
        a = a.astype(int)
    shift = np.zeros(n, dtype=int)
    shift[coordinates] = a
    return shift


if __name__ == "__main__":
    n, no_bins, no_iterations, degree, try_number = [int(sys.argv[j]) for j in [1, 2, 3, 5, 6]]
    ratio = float(sys.argv[4])

    np.random.seed(try_number)
    # First we set up the measurement matrix
    # List of all the measurements to be put into the measurement matrix
    measurements = []
    # A dictionary format of the measurements to be used in the recovery process
    recovery_dict = {}
    B = no_bins
    # Index keeps track of the number of the current measurement
    index = 0
    coord_map = {}
    for iter in range(no_iterations):
        recovery_dict[iter] = {}
        # hash coordinates to bins
        coord_map[iter] = {}
        for j in range(n):
            bin = np.random.randint(0, B)
            try:
                coord_map[iter][bin].append(j)
            except KeyError:
                coord_map[iter][bin] = [j]
                recovery_dict[iter][bin] = []
        for bin, coordinates in coord_map[iter].items():
            # Subsample Signal #
            # This coressponds to running a binary search on the coordinates
            # in the given bin
            bitRange = list(range((int(ceil(log(len(coordinates), 2))))))
            bitRange.append("all_ones")
            for bit in bitRange:
                # bit refers to which bit of the location
                # of the single 1 this binary search will specify
                shift = compute_shift(n, coordinates, bit)
                measurements.append(shift)
                recovery_dict[iter][bin].append((index, bit))
                index += 1
        B = ceil(B / ratio)

    # Construct measurement matrix
    no_binary_measurements = len(measurements)
    measurement_matrix = np.zeros((no_binary_measurements, n), dtype=int)
    for row in range(no_binary_measurements):
        measurement_matrix[row, :] = measurements[row]

    times = []
    equality = []
    for _ in range(100):
        # Cosntruct a test frequency
        frequency = np.array([0] * n, dtype=int)
        # Frequency might not actually be degree exactly 4 since we are doing sampling with replacement
        support = np.array([np.random.randint(0, n) for _ in range(degree)], dtype=int)
        frequency[support] = 1
        measurement_binary = np.dot(measurement_matrix, frequency) % 2
        # Recover the frequency

        start_time = time.time()
        current_estimate = np.zeros(n, dtype=int)
        for iter in range(no_iterations):
            residual_estimate = np.zeros(n, dtype=int)
            for bin in recovery_dict[iter]:
                coordinates = coord_map[iter][bin]
                recovered_bit_index = 0
                for index, bit in recovery_dict[iter][bin]:
                    residual_measurement = (measurement_binary[index] + np.dot(measurement_matrix[index],
                                                                               current_estimate)) % 2
                    if bit == "all_ones":
                        all_ones_bit = residual_measurement
                        continue
                    recovered_bit_index += (2 ** bit) * residual_measurement
                cond_1 = (recovered_bit_index == 0)
                cond_2 = (all_ones_bit == 1)
                if cond_1 and cond_2:
                    residual_estimate[coordinates[0]] = 1
                    # print("Enterd if")
                elif not cond_1:
                    try:
                        residual_estimate[coordinates[recovered_bit_index]] = 1
                    except IndexError:
                        None
                # print("residual_estimate=", residual_estimate)
            current_estimate = (current_estimate + residual_estimate) % 2

        end_time = time.time()
        times.append(end_time - start_time)
        equality.append(np.array_equal(current_estimate, frequency))
    p_success = sum([1 if equality[i]==True else 0 for i in range(100)])/100
    result = {"p_success": p_success , "time_median": np.median(times), \
              "times_mean": np.median(times), "times_std": np.std(times),
              "n": n, "no_bins": no_bins, "no_iterations": no_iterations, "ratio": ratio, "d": degree, \
              "measurements": no_binary_measurements, "try_number": try_number}
    print(result)
    with open(f"results2/n={n}_nobins={no_bins}_no_iter={no_iterations}_ratio={ratio}_d={degree}_{try_number}.json",
              "w") as f:
        json.dump(result, f)
