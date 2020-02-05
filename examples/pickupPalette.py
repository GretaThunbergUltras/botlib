from botlib.bot import Bot
import cv2 as cv
from controller import Controller
import time

bot = Bot()
last_detected = 0


def main():
    global bot
    global last_detected
    print("calibrating...")
    bot.calibrate()
    time.sleep(1)
    print("forklift down...")
    bot._forklift._height_motor.change_power(-100)
    # Falls Gabel aufsetzt Sleep verkürzen
    time.sleep(1.6)
    bot._forklift._height_motor.change_power(0)

    print("Forklift frontwards")
    bot._forklift._rotate_motor.change_power(-100)
    time.sleep(3)
    bot._forklift._rotate_motor.change_power(0)
    print("run")
    print("starting detection...")
    while True:
        objects = bot.detectObject("../classifiers/palette.xml")
        ret, frame = bot.getCap().read()
        if len(objects):
            global last_detected
            last_detected = time.localtime().tm_sec
            for (x, y, w, h) in objects:
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                cv.putText(frame, str((x + w / 2) / frame.shape[1]), (x, y + 20), cv.FONT_HERSHEY_SIMPLEX, 1, 255)
                steer = round((x + w / 2) / frame.shape[1] * 150, 0)
                if steer > 90:
                    steer = steer * 1.3
                elif steer < 60:
                    steer = steer / 1.3
                if steer > 150:
                    steer = 150
                print(steer)
                controller = Controller(bot)
                controller.controll(steer)
            bot.drive_power(20)
        else:
            bot.drive_power(0)
            bot.drive_steer(0)
            if last_detected != 0 and time.localtime().tm_sec - last_detected >= 3:
                # Forklift up + rotate
                print("Drive")
                bot.drive_power(30)
                time.sleep(.5)
                bot.drive_power(0)
                print("Forklift backwards")
                bot._forklift._rotate_motor.change_power(100)
                time.sleep(3)
                bot._forklift._rotate_motor.change_power(0)

                # bot.drive_steer(-1)
                print("Forklift up")
                bot._forklift._height_motor.change_power(100)
                time.sleep(1.6)
                bot._forklift._height_motor.change_power(0)
                break
        cv.imshow("Object Detection", frame)
        if cv.waitKey(1) == 27:
            break

    print("Palette wurde aufgehoben")


if __name__ == '__main__':
    main()

