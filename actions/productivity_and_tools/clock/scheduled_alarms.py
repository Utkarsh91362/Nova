import time
import logging
from datetime import datetime
import pygame
import os
from plyer import notification
from actions.productivity_and_tools.clock.alarm_utils import load_alarms, save_alarms

# 🔧 Configure logging to a file in project root
logging.basicConfig(
    filename="scheduled_alarm_log.txt",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

CHECK_INTERVAL = 30  # seconds

# 🚧 Initialize pygame mixer
pygame.mixer.init()

def trigger_alarm(alarm):
    message = f"Nova Alarm: {alarm.get('label', 'Wake up!')}"
    print("⏰ Triggering alarm:", message)

    # 🔔 System notification
    notification.notify(
        title="Nova Alarm",
        message=message,
        timeout=10  # in seconds
    )

    # 🎵 Play alarm.wav
    try:
        sound_path = os.path.join("actions", "productivity_and_tools", "clock", "alarm.wav")
        if os.path.exists(sound_path):
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        else:
            logging.warning(f"alarm.wav not found at: {sound_path}")
    except Exception as e:
        logging.warning(f"Failed to play sound: {e}")

def monitor_alarms():
    logging.info("🔁 Nova alarm monitor started.")
    while True:
        try:
            alarms = load_alarms()
            now = datetime.now().replace(second=0, microsecond=0)

            updated_alarms = []
            for alarm in alarms:
                alarm_time = datetime.strptime(alarm['time'], "%Y-%m-%d %H:%M")
                if alarm_time <= now and not alarm.get("triggered", False):
                    trigger_alarm(alarm)
                    alarm["triggered"] = True
                    logging.info(f"Triggered alarm at {alarm_time}")
                updated_alarms.append(alarm)

            save_alarms(updated_alarms)
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            logging.error(f"Alarm Monitor Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_alarms()
