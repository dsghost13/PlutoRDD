import zmq
import json
import os, csv, time, threading
from drone_node import DroneObject
from radar_display import DETECTED_DRONES

RADAR_IP = "192.168.1.50"
RADAR_PORT = 5555

# --- CSV Module ---
LOG_DIR = "logs"
FRAMES_CSV = os.path.join(LOG_DIR, "frames.csv")
DETECTIONS_CSV = os.path.join(LOG_DIR, "detections.csv")

_csv_lock = threading.Lock()
_last_frame_id = None

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

    # ----------------------------
    # CSV logging (Option A)
    #   - logs/frames.csv:     1 row per frame (metadata)
    #   - logs/detections.csv: 1 row per detection (flattened list)
    # ----------------------------
    recv_unix_s = time.time()
    os.makedirs(LOG_DIR, exist_ok=True)

    frames_header = [
        "frame_id", "timestamp_unix_s", "recv_unix_s",
        "fc_hz", "bw_hz", "chirp_T_s", "frame_rate_hz",
        "range_bin_m", "doppler_bin_mps", "azimuth_bin_deg",
        "num_detections", "dropped_frames_since_last"
    ]

    detections_header = [
        "frame_id", "timestamp_unix_s", "recv_unix_s", "det_index",
        # Fields DroneObject expects
        "id", "range_m", "velocity_mps", "power_db", "azimuth_deg", "quality",
        # Forward compatibility if DSP adds fields:
        "det_raw_json"
    ]

    def ensure_header(path, header):
        if (not os.path.exists(path)) or os.path.getsize(path) == 0:
            with open(path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()

    global _last_frame_id
    with _csv_lock:
        ensure_header(FRAMES_CSV, frames_header)
        ensure_header(DETECTIONS_CSV, detections_header)

        # Dropped frame estimate (only works if frame_id is numeric / increasing)
        dropped = ""
        try:
            curr = int(frame_id)
            if _last_frame_id is not None:
                dropped = max(0, curr - int(_last_frame_id) - 1)
            _last_frame_id = curr
        except Exception:
            dropped = ""

        # frames.csv -> one row per frame
        frame_row = {
            "frame_id": frame_id,
            "timestamp_unix_s": timestamp,
            "recv_unix_s": recv_unix_s,
            "fc_hz": fc,
            "bw_hz": bw,
            "chirp_T_s": chirp_T,
            "frame_rate_hz": frame_rate,
            "range_bin_m": range_bin,
            "doppler_bin_mps": doppler_bin,
            "azimuth_bin_deg": azimuth_bin,
            "num_detections": len(detections) if isinstance(detections, list) else 0,
            "dropped_frames_since_last": dropped,
        }
        with open(FRAMES_CSV, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=frames_header).writerow(frame_row)

        # detections.csv -> one row per detection
        if isinstance(detections, list):
            with open(DETECTIONS_CSV, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=detections_header)
                for i, det in enumerate(detections):
                    if isinstance(det, dict):
                        det_row = {
                            "frame_id": frame_id,
                            "timestamp_unix_s": timestamp,
                            "recv_unix_s": recv_unix_s,
                            "det_index": i,
                            "id": det.get("id", ""),
                            "range_m": det.get("range_m", ""),
                            "velocity_mps": det.get("velocity_mps", ""),
                            "power_db": det.get("power_db", ""),
                            "azimuth_deg": det.get("azimuth_deg", ""),
                            "quality": det.get("quality", ""),
                            "det_raw_json": json.dumps(det, separators=(",", ":")),
                        }
                    else:
                        det_row = {
                            "frame_id": frame_id,
                            "timestamp_unix_s": timestamp,
                            "recv_unix_s": recv_unix_s,
                            "det_index": i,
                            "id": "",
                            "range_m": "",
                            "velocity_mps": "",
                            "power_db": "",
                            "azimuth_deg": "",
                            "quality": "",
                            "det_raw_json": json.dumps(det, separators=(",", ":")),
                        }
                    writer.writerow(det_row)

    DETECTED_DRONES.clear()
    for drone_data in detections:
        DETECTED_DRONES.append(DroneObject(drone_data))