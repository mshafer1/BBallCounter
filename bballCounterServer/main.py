__author__ = 'Matthew'
import networking

if __name__ == '__main__':
    #post ip address to nirvana
    ip = networking.getIP()

    try:
        with open(r'\\nirvana.natinst.com\users\mshafer\bballCounterServer.ip','w') as confi_file:
            confi_file.write(ip)
    except IOError as e:
        print e
        # raise

    server = networking.server()
    server.run()