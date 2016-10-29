__author__ = 'Matthew'
import socket
import googleForm
import timestamp
import datetime


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ip = (s.getsockname()[0])
    s.close()
    return ip

class server():
    MY_HOST = getIP()
    MY_PORT = 1005

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "TCP target IP:", server.MY_HOST
        print "TCP target port:", server.MY_PORT

        self.s.bind((server.MY_HOST,server.MY_PORT))
        self.s.listen(1)

    def run(self):
        while True:
            try:
                connection, address = self.s.accept()
                address = address[0]
                print '{0}: Connection from: {1}'.format(timestamp.timeStamp(), address)
                data = connection.recv(255)
                print "{0} Receiving\n\tFrom: {1}\n\tData: {2}".format(timestamp.timeStamp(), address, data)
                if data[:12] == 'BBallCounter':
                    #post to google form
                    if data[13:].strip().upper() == "UPDATE":
                        pass # always updates
                    elif(self._should_update(address)):
                        if data[13:].strip().upper() == googleForm.FormConstants.YES.upper():
                            googleForm.post(googleForm.FormConstants.YES)
                        elif data[13:].strip().upper() == googleForm.FormConstants.YES_LATE.upper():
                            googleForm.post(googleForm.FormConstants.YES_LATE)
                        elif data[13:].strip().upper() == googleForm.FormConstants.MAYBE.upper():
                            googleForm.post(googleForm.FormConstants.MAYBE)
                        elif data[13:].strip().upper() == googleForm.FormConstants.NO.upper():
                            googleForm.post(googleForm.FormConstants.NO)
                        else:
                            print '{0}: Ignoring message: {1}'.format(timestamp.timeStamp(), data[13:])
                    else:
                        print '{0}: Ignoring update from: {0}'.format(timestamp.timeStamp(), address)


                    #get google form data
                    count = googleForm.get()
                    message = "BBallCounter:{0}".format(count)
                    print '{0}: Sending: {1}'.format(timestamp.timeStamp(), message)
                    connection.send(message)
                else:
                    print "{0}: Ignoring\n\tFrom: {1}\n\tData: {2}".format(timestamp.timeStamp(), address, data)
            except Exception as e:
                print e

    def _should_update(self, ip):
        this_player = player(ip)
        print "{0}: Investigatin Player\n\t{1}".format(timestamp.timeStamp(), this_player)
        result = updateRoster(this_player) # true if new date
        return result
server.roster = {}




class player():
    def __init__(self, ip):
        self.ip = ip
        self.last_update = datetime.datetime.now().date()

    def __str__(self):
        return 'Player:{' + 'IP: {0}, Updated: {1}'.format(self.ip, self.last_update) + '}'

def updateRoster(player):
    result = True
    if player.ip in server.roster:
        if server.roster[player.ip] >= datetime.datetime.now().date():
            print '{0}: Ignoring update from Player({1})\n\tOld Date: {2}\n\tNew Date: {3}'.format(timestamp.timeStamp(), player.ip, server.roster[player.ip], player.last_update)
            result = False
        else:
            print '{0}: Updating Player({1})\n\tOld Date: {2}\n\tNew Date: {3}'.format(timestamp.timeStamp(), player.ip, server.roster[player.ip], player.last_update)
            server.roster[player.ip] = player.last_update
    else:
        print '{0}: Adding New Player({1})\n\tNew Date: {2}'.format(timestamp.timeStamp(), player.ip, player.last_update)
        server.roster[player.ip] = player.last_update
    return result

if __name__ == '__main__':
    # print getIP()
    p = player('127.0.0.1')
    print p
    # print p.last_update
    print updateRoster(p)
    # print roster
    p.last_update +=  datetime.timedelta(days=1)
    print p
    print updateRoster(p)
    # print roster
    print p
    print updateRoster(p)