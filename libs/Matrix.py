from multiprocessing.shared_memory import SharedMemory
from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time
def Matrix():
    key = SharedMemory(name="Memory", create=False)
    col_pins = [20, 26, 21]
    row_pins = [16, 7, 8, 25]
    keys = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [30, 0, 40]
    ]
    col_outputs = [DigitalOutputDevice(pin=pin,active_high=False) for pin in col_pins]
    row_inputs = [DigitalInputDevice(pin=pin ,active_state=False, pull_up=None) for pin in row_pins]
    try:
        while True:
            # Scan each column
            for i, col_output in enumerate(col_outputs):
                col_output.on()
                # Check each row input
                for j, row_input in enumerate(row_inputs):
                    if row_input.is_active:
                        time.sleep(0.02)
                        start_time = time.time()
                        row_input.wait_for_inactive()
                        stop_time = time.time()
                        pressed_time = stop_time - start_time
                        if pressed_time >= 0.03:
                            # print(f"Key pressed: {keys[j][i]}")
                            key.buf[0] = int(keys[j][i])
                        else: 
                            continue
                col_output.off()
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")
    finally:
        # Clean up GPIO resources on exit
        key.buf[0] = 11
        key.unlink()
        for col_output in col_outputs:
            col_output.close()
        for row_input in row_inputs:
            row_input.close()
