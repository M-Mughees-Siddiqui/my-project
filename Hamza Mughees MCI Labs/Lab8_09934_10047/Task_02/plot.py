from optparse import Values
import serial
import matplotlib.pyplot as plt
from drawnow import *

# === Setup Serial ===
sinWaveData = serial.Serial('/dev/ttyACM0', 115200)
plt.ion()  # Enable interactive mode

tempValues = []
time_ms = []
cnt = 0  # Time index (1 ms steps)

# === Plotting Function ===
def makeFig():
    plt.clf()
    plt.title('Live Room temperature Data')
    plt.grid(True)
    plt.xlabel('Time (ms)')
    plt.ylabel('Temperature (°C)')
    plt.ylim(10, 30)  # Adjust range as needed
    plt.plot(time_ms, tempValues, 'r.-', label='Temperature')
    plt.legend(loc='upper left')

# === Main Loop ===
while True:
    while sinWaveData.inWaiting() == 0:
        pass  # Wait for data

    try:
        line = sinWaveData.readline().decode().strip()
        values = line.split(',')

        if len(values) == 1:
            temp = int(values[0])
            
            tempValues.append(temp)
            time_ms.append(cnt)
            cnt += 1

            drawnow(makeFig)
            plt.pause(0.0001)

            # Keep only last 500 samples
            if len(tempValues) > 500:
                tempValues.pop(0)
                time_ms.pop(0)

    except Exception as e:
        print("Error:", e)
