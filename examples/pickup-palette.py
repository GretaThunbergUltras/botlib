#!/usr/bin/python3

from botlib.bot import Bot
import cv2 as cv

def main():
    bot = Bot()

    print('calibrating...')
    bot.calibrate()

    bot.forklift()._height_motor.change_power(-10)
    cv.waitKey(1000)
    bot.forklift()._height_motor.change_power(0)

    print('run')
    print('starting detection...')

    while True:
        objects = bot.objectdetector().detect('../classifiers/palette.xml')
        frame = bot.camera().get_capture().read()

        if len(objects) != 0:
            bot.drive_power(30)

            for x, y, w, h in objects:
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                cv.putText(frame, str((x + w / 2) / frame.shape[1]), (x, y + 20), cv.FONT_HERSHEY_SIMPLEX, 1, 255)
                steer = round((x + w / 2) / frame.shape[1] * 150, 0)

                if steer > 100:
                    steer = steer * 1.8
                if steer < 50:
                    steer = steer / 1.8
                if steer > 150:
                    steer = 150

                bot.drive_steer(steer)

        else:
            bot.drive_power(0)

        cv.imshow('Object Detection', frame)
        if cv.waitKey(1) == 27:
            break

if __name__ == '__main__':
    main()
