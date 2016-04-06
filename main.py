#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import Spider
import IO
import os
import atexit
import signal
import codecs


def daemonize(pidfile, *, stdin='/dev/null',
              stdout='/dev/null',
              stderr='/dev/null'):


    if os.path.exists(pidfile):
        raise RuntimeError('Already running')

    # First fork (detaches from parent)
    try:
        if os.fork() > 0:
            raise SystemExit(0)  # Parent exit
    except OSError as e:
        raise RuntimeError('fork #1 failed.')

    # os.chdir('/')
    os.umask(0)
    os.setsid()
    # Second fork (relinquish session leadership)
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')

    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Replace file descriptors for stdin, stdout, and stderr
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Write the PID file
    with open(pidfile, 'w') as f:
        print(os.getpid(), file=f)

    # Arrange to have the PID file removed on exit/signal
    atexit.register(lambda: os.remove(pidfile))


# Signal handler for termination (required)
def sigterm_handler(signo, frame):
    raise SystemExit(1)


signal.signal(signal.SIGTERM, sigterm_handler)



def startSpider():
    print('WhiteList spider started!')
    try:
        daemonize(PIDFILE,
                  stdout='/tmp/daemon.log',
                  stderr='/tmp/dameon.log')
    except RuntimeError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1)
    io = IO.IO()
    spider = Spider.Spider(io)
    spider.start()



def status():
    io = IO.IO()
    list = io.getList()
    if os.path.exists(PIDFILE):
        print('Spider is running.\n')
    else:
        print('Spider is not running.\n')
    print('Now we have '+str(len(list))+' whitelist item!\n',)
    print('Top 10 here:\n')
    i = 0
    for row in list:
        i += 1
        print(row[1]+', count: '+str(row[0]))
        if i > 9: break


def help():
    print('GFW domain whitelist spider v0.1 alpha 3\n'
          'To start sprider you need edit sql server infomation first.\n\n'
          'main.py [start|stop|restart|status|list|help]\n\n'
          '------------------\n\n'
          'start    start spider\n'
          'stop     stop spider\n'
          'restart  restart spider\n'
          'status   check list status\n'
          'list     get whitelist top 10000\n'
          'help     show this page\n')

def stop():
    if os.path.exists(PIDFILE):
        with open(PIDFILE) as f:
            os.kill(int(f.read()), signal.SIGTERM)
        print('WhiteList spider stopped!')
    else:
        print('Not running', file=sys.stderr)
        raise SystemExit(1)

def outPutList():
    count = 10000
    io = IO.IO()
    list = io.getList()
    f = codecs.open('./whitelist.txt','w','utf-8')
    print('Output top 10000 domains in whitelist.txt\n', )
    i = 0
    for item in list:
        i += 1
        f.write(item[1]+'\n')
        if i == 10000: break
    print('done! got '+str(i)+' domains.')


def main():
    if len(sys.argv) == 1:
        help()
        return
    if sys.argv[1] == 'start':
        startSpider()

    elif sys.argv[1] == 'status':
       status()

    elif sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'restart':
        stop()
        startSpider()
    elif sys.argv[1] == 'list':
        outPutList()
    elif sys.argv[1] == 'help':
        help()
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)


if __name__=='__main__':
    PIDFILE = '/tmp/GFW-White-Domain-List-daemon.pid'
    main()