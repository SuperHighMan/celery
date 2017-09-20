from proj.async import AsyncCheck
import datetime

if __name__ == '__main__':
    args = [['192.168.92.133'], 'uptime']
    begin = datetime.datetime.now()
    check = AsyncCheck(args=args, interval=3, times=2)
    check.run()
    print(check.timeout_result())
    end = datetime.datetime.now()
    print(end - begin)

    begin = datetime.datetime.now()
    check = AsyncCheck(args=args)
    check.run()
    print(check.timeout_result())
    end = datetime.datetime.now()
    print(end - begin)


