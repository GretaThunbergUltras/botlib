from botlib.bot import bot

def main():
    bot = Bot()
    bot.setup_sonar()

    try:
        while True:
            distance = bot._sonar.get_distance()
            print('left:', distance[0], 'left45:', distance[1], 'left_front:', distance[2], 'right_front:', distance[3], 'right45:', distance[4], 'right:', distance[5], 'back:', distance[6])
    except KeyboardInterrupt:
        print('ende')

if __name__ == '__main__':
    main()
