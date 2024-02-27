import numpy as np

prev = "empty"

import numpy as np
from collections import Counter


x = 0
y = 1
timestamp = 2


def ivt(data, v_threshold):
    data = np.array(data)

    times = data[:, timestamp]

    ts = []

    for t in times:
        ts.append(float(t) / 1000.0)

    times = ts  # TOD0: CHECK if times in sec

    Xs = data[:, x]
    Ys = data[:, y]

    difX = []
    difY = []
    tdif = []

    for i in range(len(data) - 1):
        difX.append(float(Xs[i + 1]) - float(Xs[i]))
        difY.append(float(Ys[i + 1]) - float(Ys[i]))
        tdif.append(float(times[i + 1]) - float(times[i]))



    dif = np.sqrt(np.power(difX, 2) + np.power(difY, 2))  # in pix

    velocity = dif / tdif

    # print velocity in pix/sec
    # print tdif

    mvmts = []  # length is len(data)-1

    for v in velocity:
        if (v < v_threshold):
            # fixation
            mvmts.append(1)
        # print v, v_threshold
        else:
            mvmts.append(0)

    fixations = []
    fs = []
    for m in range(len(mvmts)):
        if mvmts[m] == 0:
            if len(fs) > 0:
                fixations.append(fs)
                fs = []
        fs.append(mvmts[m])

    if (len(fs) > 0):
        fixations.append(fs)






    total = 0
    for i in fixations:
        for j in i:
            total += 1

    # print fixations
    centroidsX = []
    centroidsY = []
    time0 = []
    time1 = []
    fixation_counts = []


    for f in fixations: #  [ [0,1,2,3,4]    [5,6,7]  [8]   ]
        cX = 0
        cY = 0

        if (len(f) == 1):
            i = f[0]
            cX = (float(data[i][x]) + float(data[i + 1][x])) / 2.0
            cY = (float(data[i][y]) + float(data[i + 1][y])) / 2.0
            t0 = float(data[i][timestamp])
            t1 = float(data[i + 1][timestamp])

        else:
            t0 = float(data[f[0]][timestamp]) # arrayın ilk elamanın timestampı bizim ilk bakma zamanıdır.
            t1 = float(data[f[len(f) - 1] + 1][timestamp]) #

            for e in range(len(f)):
                cX += float(data[f[e]][x])
                cY += float(data[f[e]][y])

            cX += float(data[f[len(f) - 1] + 1][x])
            cY += float(data[f[len(f) - 1] + 1][y])

            cX = cX / float(len(f) + 1)
            cY = cY / float(len(f) + 1)

        centroidsX.append(cX)
        centroidsY.append(cY)
        fixation_counts.append(len(f))
        time0.append(t0)
        time1.append(t1)
    fixation_total = []

    total = 0
    for i in fixation_counts:
        total += i


    for i in range(0,len(centroidsX)):  # x,y, firstime, fixaton count ->
        newList = []

        newList.append(centroidsX[i])
        newList.append(centroidsY[i])
        newList.append(time0[i]/1000)

        newList.append(fixation_counts[i])

        fixation_total.append(newList)

    return fixation_total


def screen_find_element(cordinates, oran, current_file):
    try:
        file_string = "files/" + current_file + ".txt"
        with open(file_string, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            splited_strings = line.split(" ")

            x1 = float(splited_strings[0]) * oran
            y1 = float(splited_strings[2]) * oran
            x2 = (float(splited_strings[0]) + float(splited_strings[1])) * oran
            y2 = (float(splited_strings[2]) + float(splited_strings[3])) * oran

            if x1 <= cordinates[0] <= x2 and y1 <= cordinates[1] <= y2:
                return splited_strings[4]


    except IOError as error:
        print(error)


def compute_metrics(data_eye_track, current_file):
    try:
        file_string = "files/" + current_file + ".txt"
        with open(file_string, "r") as file:
            lines = file.readlines()
        # print(data_eye_track)
        all_elements = {}
        for line in lines:
            line = line.strip()
            element = line.split(" ")[4]

            all_elements[element] = 0

        features = {}
        for eye_values in data_eye_track:
            element = eye_values[6]
            fixation_counts = eye_values[5]
            # marked as seen
            all_elements[element] = 1
            duration = float(eye_values[4])
            first_time_look = float(eye_values[3])

            global prev

            if element in features:
                features[element][0] += duration
                features[element][3] += fixation_counts
                if prev != element:
                    features[element][2] += 1
                prev = element
            elif element is None:
                pass
            else:
                features[element] = []

                features[element].append(duration)
                features[element].append(first_time_look)
                # revisits
                features[element].append(1)
                features[element].append(fixation_counts)
                prev = element

        for element in all_elements.keys():
            if all_elements[element] == 0:
                features[element] = []

                features[element].append(0)
                features[element].append(-1)
                features[element].append(0)
                features[element].append(0)

    except IOError as error:
        print(error)
    return features


import numpy as np

x = 0  # Assuming x is the index for x-coordinate in your data
y = 1  # Assuming y is the index for y-coordinate in your data
timestamp = 2  # Assuming timestamp is the index for timestamp in your data

def idt(data, dis_threshold, dur_threshold):
    data = np.array(data)
    window_range = [0, 0]

    current = 0  # pointer to represent the current beginning point of the window
    last = 0
    # final lists for fixation info
    centroidsX = []
    centroidsY = []
    time0 = []
    time1 = []
    fixation_counts = []

    while current < len(data):

        t0 = float(data[current][timestamp])  # beginning time
        t1 = t0 + float(dur_threshold)  # time after a min. fix. threshold has been observed

        for r in range(current, len(data)):
            if float(data[r][timestamp]) >= t0 and float(data[r][timestamp]) <= t1:
                last = r  # this will find the last index still in the duration threshold

        window_range = [current, last]

        # now check the dispersion in this window
        dispersion = get_dispersion(data[current:last + 1])

        if dispersion <= dis_threshold:
            # add new points
            while dispersion <= dis_threshold and last + 1 < len(data):
                last += 1
                window_range = [current, last]
                dispersion = get_dispersion(data[current:last + 1])

            # dispersion threshold is exceeded
            # fixation at the centroid [current,last]

            cX = 0
            cY = 0

            for f in range(current, last + 1):
                cX += float(data[f][x])
                cY += float(data[f][y])

            cX = cX / float(last - current + 1)
            cY = cY / float(last - current + 1)

            t0 = float(data[current][timestamp])
            t1 = float(data[last][timestamp])

            centroidsX.append(cX)
            centroidsY.append(cY)
            time0.append(t0)
            time1.append(t1)
            fixation_counts.append(len(data[current:last + 1]))

            current = last + 1  # this will move the pointer to a novel window

        else:
            current += 1  # this will remove the first point
            last = current  # this is not necessary

    fixation_total = []

    for i in range(len(centroidsX)):
        newList = []

        newList.append(centroidsX[i])
        newList.append(centroidsY[i])
        newList.append(time0[i])

        newList.append(fixation_counts[i])

        fixation_total.append(newList)




    return fixation_total


def get_dispersion(points):
    argxmin = np.min(points[:, x].astype(float))
    argxmax = np.max(points[:, x].astype(float))

    argymin = np.min(points[:, y].astype(float))
    argymax = np.max(points[:, y].astype(float))

    dispersion = ((argxmax - argxmin) + (argymax - argymin)) / 2


    return dispersion




