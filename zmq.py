import zmq
import json

from radar_display import DETECTED_DRONES

RADAR_IP = "192.168.1.50"
RADAR_PORT = 5555

def receive_frames():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{RADAR_IP}:{RADAR_PORT}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    print("Connected to PlutoSDR!")

    while True:
        try:
            message = socket.recv_string()
            frame = json.loads(message)     
            process_frame(frame)            # place maybe dummy data?
        except Exception as e:
            print("Error:", e)


def process_frame(frame):
    frame_id = frame["frame_id"]
    timestamp = frame["timestamp_unix_s"]
    range_bin = frame["range_bin_m"]
    doppler_bin = frame["doppler_bin_mps"]
    azimuth_bin = frame["azimuth_bin_deg"]
    fc = frame["fc_hz"]
    bw = frame["bw_hz"]
    chirp_T = frame["chirp_T_s"]
    frame_rate = frame["frame_rate_hz"]
    detections = frame["detections"]

    # TODO: put this in a CSV file probably
    # We're also super reliant on the DSP Team to give us the JSON file -Calla
    # Create CSV File; the above strings (e.g., frame_id) should be column headers in the CSV
    # Should propagate CSV file with new row every time process_frame is called

    DETECTED_DRONES.clear()
    for drone_data in detections:
        DETECTED_DRONES.append(DroneObject(drone_data))


