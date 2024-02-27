import os

from flask import *
from collections import defaultdict
import statistics
import csv
import  matplotlib
matplotlib.use('Agg')  # Flask ile uyumsuzlukları gidermek için
from fixation import screen_find_element, compute_metrics,ivt,idt

import matplotlib.pyplot as plt

# Cell koordinatları
cell_coordinates = {
    1: {'left': 0, 'right': 219.4250030517578, 'top': 0, 'bottom': 106.05000305175781},
    2: {'left': 219.4250030517578, 'right': 438.8500061035156, 'top': 0, 'bottom': 106.05000305175781},
    3: {'left': 438.8500061035156, 'right': 658.2750091552734, 'top': 0, 'bottom': 106.05000305175781},
    4: {'left': 658.2750244140625, 'right': 877.7125244140625, 'top': 0, 'bottom': 106.05000305175781},
    5: {'left': 877.7125244140625, 'right': 1097.1375274658203, 'top': 0, 'bottom': 106.05000305175781},
    6: {'left': 1097.1375732421875, 'right': 1316.5625762939453, 'top': 0, 'bottom': 106.05000305175781},
}

cell_coordinates[7] = {'left': 1316.5625, 'right': 1536, 'top': 0, 'bottom': 106.05000305175781}
cell_coordinates[8] = {'left': 0, 'right': 219.4250030517578, 'top': 106.05000305175781, 'bottom': 212.1125030517578}
cell_coordinates[9] = {'left': 219.4250030517578, 'right': 438.8500061035156, 'top': 106.05000305175781, 'bottom': 212.1125030517578}
cell_coordinates[10] = {'left': 438.8500061035156, 'right': 658.2750091552734, 'top': 106.05000305175781, 'bottom': 212.1125030517578}
cell_coordinates[11] = {'left': 658.2750244140625, 'right': 877.7125244140625, 'top': 106.05000305175781, 'bottom': 212.1125030517578}
cell_coordinates[12] = {'left': 877.7125244140625, 'right': 1097.1375274658203, 'top': 106.05000305175781, 'bottom': 212.1125030517578}
cell_coordinates[13] = {'left': 1097.1375732421875, 'right': 1316.5625762939453, 'top': 106.05000305175781, 'bottom': 212.1125030517578}
cell_coordinates[14] = {'left': 1316.5625, 'right': 1536, 'top': 106.05000305175781, 'bottom': 212.1125030517578}
cell_coordinates[15] = {'left': 0, 'right': 219.4250030517578, 'top': 212.1125030517578, 'bottom': 318.1625061035156}
cell_coordinates[16] = {'left': 219.4250030517578, 'right': 438.8500061035156, 'top': 212.1125030517578, 'bottom': 318.1625061035156}
cell_coordinates[17] = {'left': 438.8500061035156, 'right': 658.2750091552734, 'top': 212.1125030517578, 'bottom': 318.1625061035156}
cell_coordinates[18] = {'left': 658.2750244140625, 'right': 877.7125244140625, 'top': 212.1125030517578, 'bottom': 318.1625061035156}
cell_coordinates[19] = {'left': 877.7125244140625, 'right': 1097.1375274658203, 'top': 212.1125030517578, 'bottom': 318.1625061035156}
cell_coordinates[20] = {'left': 1097.1375732421875, 'right': 1316.5625762939453, 'top': 212.1125030517578, 'bottom': 318.1625061035156}
cell_coordinates[21] = {'left': 1316.5625, 'right': 1536, 'top': 212.1125030517578, 'bottom': 318.1625061035156}
cell_coordinates[22] = {'left': 0, 'right': 219.4250030517578, 'top': 318.1625061035156, 'bottom': 424.2250061035156}
cell_coordinates[23] = {'left': 219.4250030517578, 'right': 438.8500061035156, 'top': 318.1625061035156, 'bottom': 424.2250061035156}
cell_coordinates[24] = {'left': 438.8500061035156, 'right': 658.2750091552734, 'top': 318.1625061035156, 'bottom': 424.2250061035156}
cell_coordinates[25] = {'left': 658.2750244140625, 'right': 877.7125244140625, 'top': 318.1625061035156, 'bottom': 424.2250061035156}
cell_coordinates[26] = {'left': 877.7125244140625, 'right': 1097.1375274658203, 'top': 318.1625061035156, 'bottom': 424.2250061035156}
cell_coordinates[27] = {'left': 1097.1375732421875, 'right': 1316.5625762939453, 'top': 318.1625061035156, 'bottom': 424.2250061035156}
cell_coordinates[28] = {'left': 1316.5625, 'right': 1536, 'top': 318.1625061035156, 'bottom': 424.2250061035156}
cell_coordinates[29] = {'left': 0, 'right': 219.4250030517578, 'top': 424.2250061035156, 'bottom': 530.2750091552734}
cell_coordinates[30] = {'left': 219.4250030517578, 'right': 438.8500061035156, 'top': 424.2250061035156, 'bottom': 530.2750091552734}
cell_coordinates[31] = {'left': 438.8500061035156, 'right': 658.2750091552734, 'top': 424.2250061035156, 'bottom': 530.2750091552734}
cell_coordinates[32] = {'left': 658.2750244140625, 'right': 877.7125244140625, 'top': 424.2250061035156, 'bottom': 530.2750091552734}
cell_coordinates[33] = {'left': 877.7125244140625, 'right': 1097.1375274658203, 'top': 424.2250061035156, 'bottom': 530.2750091552734}
cell_coordinates[34] = {'left': 1097.1375732421875, 'right': 1316.5625762939453, 'top': 424.2250061035156, 'bottom': 530.2750091552734}
cell_coordinates[35] = {'left': 1316.5625, 'right': 1536, 'top': 424.2250061035156, 'bottom': 530.2750091552734}
cell_coordinates[36] = {'left': 0, 'right': 219.4250030517578, 'top': 530.2750091552734, 'bottom': 636.3375091552734}
cell_coordinates[37] = {'left': 219.4250030517578, 'right': 438.8500061035156, 'top': 530.2750091552734, 'bottom': 636.3375091552734}
cell_coordinates[38] = {'left': 438.8500061035156, 'right': 658.2750091552734, 'top': 530.2750091552734, 'bottom': 636.3375091552734}
cell_coordinates[39] = {'left': 658.2750244140625, 'right': 877.7125244140625, 'top': 530.2750091552734, 'bottom': 636.3375091552734}
cell_coordinates[40] = {'left': 877.7125244140625, 'right': 1097.1375274658203, 'top': 530.2750091552734, 'bottom': 636.3375091552734}
cell_coordinates[41] = {'left': 1097.1375732421875, 'right': 1316.5625762939453, 'top': 530.2750091552734, 'bottom': 636.3375091552734}
cell_coordinates[42] = {'left': 1316.5625, 'right': 1536, 'top': 530.2750091552734, 'bottom': 636.3375091552734}
cell_coordinates[43] = {'left': 0, 'right': 219.4250030517578, 'top': 636.3375091552734, 'bottom': 742.3875122070312}
cell_coordinates[44] = {'left': 219.4250030517578, 'right': 438.8500061035156, 'top': 636.3375091552734, 'bottom': 742.3875122070312}
cell_coordinates[45] = {'left': 438.8500061035156, 'right': 658.2750091552734, 'top': 636.3375091552734, 'bottom': 742.3875122070312}
cell_coordinates[46] = {'left': 658.2750244140625, 'right': 877.7125244140625, 'top': 636.3375091552734, 'bottom': 742.3875122070312}
cell_coordinates[47] = {'left': 877.7125244140625, 'right': 1097.1375274658203, 'top': 636.3375091552734, 'bottom': 742.3875122070312}
cell_coordinates[48] = {'left': 1097.1375732421875, 'right': 1316.5625762939453, 'top': 636.3375091552734, 'bottom': 742.3875122070312}
cell_coordinates[49] = {'left': 1316.5625, 'right': 1536, 'top': 636.3375091552734, 'bottom': 742.3875122070312}


def find_cell(gaze_point, cells):
    x, y = gaze_point

    for cell_id, cell in cells.items():
        if cell['left'] <= x <= cell['right'] and cell['top'] <= y <= cell['bottom'] :
            return cell_id
    return None


def calculate_cell_ratios(ourResult, start_time, end_time):
    cell_ratios = defaultdict(float)

    for cell, time in ourResult:
        if start_time <= time <= end_time:
            cell_ratios[cell] += 1

    total = sum(cell_ratios.values())
    cell_ratios = {key: value / total for key, value in cell_ratios.items()}

    return cell_ratios

def calculate_average_ratios(ourResult, intervals):
    average_ratios = {}

    for start, end in intervals:
        cell_ratios = calculate_cell_ratios(ourResult, start, end)
        average_ratios[f"{start}s - {end}s"] = cell_ratios

    return average_ratios


def plot_pie_chart(cell_ratios, interval):
    labels = list(cell_ratios.keys())
    sizes = list(cell_ratios.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Kaydedilecek grafik dosyasının adını oluştur
    chart_file = f"pie_charts/pie_chart_{interval.replace(' ', '_')}.png"

    # Grafik dosyasını kaydet
    fig.savefig(chart_file)
    plt.close(fig)  # Close the figure to free up resources

    return chart_file


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('calibration.html')


@app.route("/mainHTML")
def mainHTML():
    return render_template("mainHTML.html")

@app.route('/save_data', methods=['GET','POST'])
def save_data():

    data = request.get_json()
    eye_tracking_data = data['eyeTrackingData']

    print(eye_tracking_data)

    print("///")
    print("///")

    fixationAlgorithmData = data['eyeTrackingData']
    fixationAlgorithmData = fixationAlgorithmData[1:]



    pairs = idt(fixationAlgorithmData,20,100)


    print("///")
    print("///")

    finalFixationList = []

    for liste in pairs:
        x, y, time, count = liste

        for _ in range(count):
            newList = [x, y, time]
            finalFixationList.append(newList)


    print(finalFixationList)





    values = []

    for data_point in eye_tracking_data:
        values.extend(data_point)

    lst = []
    for i in range(0, len(values), 3):
        tempTuple = (values[i], values[i + 1])
        lst.append(tempTuple)

    result = [(point, find_cell(point, cell_coordinates)) for point in lst]

    index = -1
    for i, (inner_tuple, value) in enumerate(result):
        if value == 1:
            index = i
            break

    result = result[index:]
    result_with_time = [(cell_id, time / 1000) for (point, cell_id), time in
                        zip(result, [data_point[2] for data_point in eye_tracking_data])]

    firstLookTime = result_with_time[1][1]

    for index, (cell_id, time) in enumerate(result_with_time):
        result_with_time[index] = (cell_id, time - firstLookTime)

    ourResult = result_with_time[1:]
    #print(ourResult)

    lst = []
    timeCount = 5
    checkIndex = 1

    # calculate_average_ratios fonksiyonunu kullanarak her bir time aralığındaki hücrelere bakma oranlarının aritmetik ortalamasını hesapla
    intervals = [(0, 5), (5, 10), (10, 15), (15, 20),
                 (20, 25),(25, 30),(30, 35),(35, 40),(40, 45),
                 (45, 50),(50,55),(55, 60),(60, 65),(65, 70),(75, 80),(80, 85),(85,90),
                 (90,95),(95,100), (100,105),(105,110),(110,115),(115,120),(120,125),(125,130),
                 (130,135),(135,140),(140,145),(145,150),(150,155),(155,160),(160,165),(165,170),
                 (170,175),(175,180),(180,185),(185,190),(190,195),(195,200),(200,205),(205,210),
                 (210,215),(215,220),(220,225),(225,230),(230,235),(235,240)]

    average_ratios = calculate_average_ratios(ourResult, intervals)

    for interval, cell_ratios in average_ratios.items():
        """print(f"{interval}: {cell_ratios}")"""

    systemAverageValue = []

    # Elde edilen sonuçları yazdır
    for interval, cell_ratios in average_ratios.items():
        if interval == '0s - 5s':
            if 1  in cell_ratios:
                systemAverageValue.append(cell_ratios[1])
            else:
                systemAverageValue.append(0)

        if interval == '5s - 10s':
            if 2 in cell_ratios:
                systemAverageValue.append(cell_ratios[2])
            else:
                systemAverageValue.append(0)

        if interval == '10s - 15s':
            if 3 in cell_ratios:
                systemAverageValue.append(cell_ratios[3])
            else:
                systemAverageValue.append(0)

        if interval == '15s - 20s':
            if 4 in cell_ratios:
                systemAverageValue.append(cell_ratios[4])
            else:
                systemAverageValue.append(0)

        if interval == '20s - 25s':
            if 5 in cell_ratios:
                systemAverageValue.append(cell_ratios[5])
            else:
                systemAverageValue.append(0)

        if interval == '25s - 30s':
            if 6 in cell_ratios:
                systemAverageValue.append(cell_ratios[6])
            else:
                systemAverageValue.append(0)

        if interval == '30s - 35s':
            if 7 in cell_ratios:
                systemAverageValue.append(cell_ratios[7])
            else:
                systemAverageValue.append(0)



        if interval == '35s - 40s':
            if 8 in cell_ratios:
                systemAverageValue.append(cell_ratios[8])
            else:
                systemAverageValue.append(0)

        if interval == '40s - 45s':
            if 9 in cell_ratios:
                systemAverageValue.append(cell_ratios[9])
            else:
                systemAverageValue.append(0)
        if interval == '45s - 50s':
            if 10 in cell_ratios:
                systemAverageValue.append(cell_ratios[10])
            else:
                systemAverageValue.append(0)
        if interval == '50s - 55s':
            if 11 in cell_ratios:
                systemAverageValue.append(cell_ratios[11])
            else:
                systemAverageValue.append(0)
        if interval == '55s - 60s':
            if 12 in cell_ratios:
                systemAverageValue.append(cell_ratios[12])
            else:
                systemAverageValue.append(0)
        if interval == '60s - 65s':
            if 13 in cell_ratios:
                systemAverageValue.append(cell_ratios[13])
            else:
                systemAverageValue.append(0)
        if interval == '65s - 70s':
            if 14 in cell_ratios:
                systemAverageValue.append(cell_ratios[14])
            else:
                systemAverageValue.append(0)

        if interval == '70s - 75s':
            if 15 in cell_ratios:
                systemAverageValue.append(cell_ratios[15])
            else:
                systemAverageValue.append(0)


        if interval == '75s - 80s':
            if 16 in cell_ratios:
                systemAverageValue.append(cell_ratios[16])
            else:
                systemAverageValue.append(0)
        if interval == '80s - 85s':
            if 17 in cell_ratios:
                systemAverageValue.append(cell_ratios[17])
            else:
                systemAverageValue.append(0)
        if interval == '85s - 90s':
            if 19 in cell_ratios:
                systemAverageValue.append(cell_ratios[19])
            else:
                systemAverageValue.append(0)

        if interval == '90s - 95s':
            if 20 in cell_ratios:
                systemAverageValue.append(cell_ratios[20])
            else:
                systemAverageValue.append(0)

        if interval == '95s - 100s':
            if 21 in cell_ratios:
                systemAverageValue.append(cell_ratios[21])
            else:
                systemAverageValue.append(0)

        if interval == '100s - 105s':
            if 22 in cell_ratios:
                systemAverageValue.append(cell_ratios[22])
            else:
                systemAverageValue.append(0)

        if interval == '105s - 110s':
            if 23 in cell_ratios:
                systemAverageValue.append(cell_ratios[23])
            else:
                systemAverageValue.append(0)

        if interval == '110s - 115s':
            if 24 in cell_ratios:
                systemAverageValue.append(cell_ratios[24])
            else:
                systemAverageValue.append(0)

        if interval == '115s - 120s':
            if 25 in cell_ratios:
                systemAverageValue.append(cell_ratios[25])
            else:
                systemAverageValue.append(0)

        if interval == '120s - 125s':
            if 26 in cell_ratios:
                systemAverageValue.append(cell_ratios[26])
            else:
                systemAverageValue.append(0)

        if interval == '125s - 130s':
            if 27 in cell_ratios:
                systemAverageValue.append(cell_ratios[27])
            else:
                systemAverageValue.append(0)

        if interval == '130s - 135s':
            if 28 in cell_ratios:
                systemAverageValue.append(cell_ratios[28])
            else:
                systemAverageValue.append(0)

        if interval == '135s - 140s':
            if 29 in cell_ratios:
                systemAverageValue.append(cell_ratios[29])
            else:
                systemAverageValue.append(0)

        if interval == '140s - 145s':
            if 30 in cell_ratios:
                systemAverageValue.append(cell_ratios[30])
            else:
                systemAverageValue.append(0)

        if interval == '145s - 150s':
            if 31 in cell_ratios:
                systemAverageValue.append(cell_ratios[31])
            else:
                systemAverageValue.append(0)

        if interval == '150s - 155s':
            if 32 in cell_ratios:
                systemAverageValue.append(cell_ratios[32])
            else:
                systemAverageValue.append(0)

        if interval == '155s - 160s':
            if 33 in cell_ratios:
                systemAverageValue.append(cell_ratios[33])
            else:
                systemAverageValue.append(0)

        if interval == '160s - 165s':
            if 34 in cell_ratios:
                systemAverageValue.append(cell_ratios[34])
            else:
                systemAverageValue.append(0)

        if interval == '165s - 170s':
            if 35 in cell_ratios:
                systemAverageValue.append(cell_ratios[35])
            else:
                systemAverageValue.append(0)

        if interval == '170s - 175s':
            if 36 in cell_ratios:
                systemAverageValue.append(cell_ratios[36])
            else:
                systemAverageValue.append(0)

        if interval == '175s - 180s':
            if 37 in cell_ratios:
                systemAverageValue.append(cell_ratios[37])
            else:
                systemAverageValue.append(0)

        if interval == '180s - 185s':
            if 38 in cell_ratios:
                systemAverageValue.append(cell_ratios[38])
            else:
                systemAverageValue.append(0)

        if interval == '185s - 190s':
            if 39 in cell_ratios:
                systemAverageValue.append(cell_ratios[39])
            else:
                systemAverageValue.append(0)

        if interval == '190s - 195s':
            if 40 in cell_ratios:
                systemAverageValue.append(cell_ratios[40])
            else:
                systemAverageValue.append(0)

        if interval == '195s - 200s':
            if 41 in cell_ratios:
                systemAverageValue.append(cell_ratios[41])
            else:
                systemAverageValue.append(0)

        if interval == '200s - 205s':
            if 42 in cell_ratios:
                systemAverageValue.append(cell_ratios[42])
            else:
                systemAverageValue.append(0)

        if interval == '205s - 210s':
            if 43 in cell_ratios:
                systemAverageValue.append(cell_ratios[43])
            else:
                systemAverageValue.append(0)

        if interval == '210s - 215s':
            if 44 in cell_ratios:
                systemAverageValue.append(cell_ratios[44])
            else:
                systemAverageValue.append(0)

        if interval == '215s - 220s':
            if 45 in cell_ratios:
                systemAverageValue.append(cell_ratios[45])
            else:
                systemAverageValue.append(0)

        if interval == '220s - 225s':
            if 46 in cell_ratios:
                systemAverageValue.append(cell_ratios[46])
            else:
                systemAverageValue.append(0)

        if interval == '225s - 230s':
            if 47 in cell_ratios:
                systemAverageValue.append(cell_ratios[47])
            else:
                systemAverageValue.append(0)

        if interval == '230s - 235s':
            if 48 in cell_ratios:
                systemAverageValue.append(cell_ratios[48])
            else:
                systemAverageValue.append(0)



    #print(systemAverageValue)

    system_accuracy = sum(systemAverageValue) / len(systemAverageValue)
    #print("System performence accuracy is:", system_accuracy)

    # Pie chart'ın kaydedileceği klasörü belirtin
    chart_folder = 'static/pie_charts/'

    # Eğer klasör mevcut değilse oluşturun
    if not os.path.exists(chart_folder):
        os.makedirs(chart_folder)

    # Grafik dosyalarını kaydet ve dosya adlarını listeye ekle
    # Grafik dosyalarını kaydet ve dosya adlarını listeye ekle
    chart_files = []  # Buraya eklendi
    for interval, cell_ratios in average_ratios.items():
        labels = list(cell_ratios.keys())
        sizes = list(cell_ratios.values())

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Daireyi çiz

        # Grafik başlığı ve açıklama
        plt.title(f'Pie Chart for {interval}')

        # Kaydet ve dosya adını listeye ekle
        chart_file = f"{chart_folder}pie_chart_{interval.replace(' ', '_')}.png"
        fig1.savefig(chart_file)
        plt.close(fig1)

        chart_files.append(chart_file)

    # HTML sayfasına dosya adlarını ve diğer verileri gönder
    return render_template('result.html', chart_files=chart_files, average_ratios=average_ratios,
                           system_accuracy=system_accuracy), 200


if __name__ == "__main__":

    app.run()