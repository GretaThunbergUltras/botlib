from botlib.bot import Bot

# checks if the motors are coupled up correctly

if __name__ == '__main__':
    print('stopping all...')
    Bot().stop_all()
    print('done...')
