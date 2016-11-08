__author__ = 'Matthew'
import networking
from sendBBallEmail import EMAIL_LIST_FILE as main_email_ist
from sendBBallSummaryEmail import EMAIL_LIST_FILE as summary_email_ist


if __name__ == '__main__':
    #setup config files
    open(main_email_ist, 'a').close()
    open(summary_email_ist, 'a').close()

    #post ip address to nirvana
    ip = networking.getIP()

    try:
        with open(r'//nirvana.natinst.com/users/mshafer/bballCounterServer.ip','w') as confi_file:
            confi_file.write(ip)
    except IOError as e:
        print e
        # raise

    server = networking.server()
    server.run()
