import smtplib
import csv
import sys
import argparse
import traceback


def get_args():
    parser = argparse.ArgumentParser(
        description='Script para comprobar STARTTLS en servidor smtp \nBy @z3r082')
    parser.add_argument('-i', type=str,
                        required=False, default='servidores.txt', help='File smtp servers')
    return parser.parse_args()


def checktls(args):
    with open(args.i, 'r') as servernames:
        for servername in servernames.readlines():
            servername = servername.rstrip('\n')
            serverport = 25
            checkstarttls = ''

            if serverport:
                serverport = int(serverport)
            else:
                serverport = 25

            try:
                print('starting with a secure connection')
                server = smtplib.SMTP_SSL(servername, serverport)
            except Exception as e:
                print("Error secureconnection:", e)
                print('starting with a insecure connection')
                server = smtplib.SMTP(servername, serverport)

            try:
                server.set_debuglevel(True)

                # identify ourselves, prompting server for supported features
                server.ehlo()

                if server.has_extn('STARTTLS'):
                    print('(starting TLS)')
                    if server.starttls():
                        checkstarttls = True
                    else:
                        checkstarttls = False

                else:
                    print('(no STARTTLS)')
                    checkstarttls = False
            finally:
                server.quit()
            # server.quit()
            exportcsv(servername, checkstarttls)


def exportcsv(servername, checkstarttls):
    f = csv.writer(open('mailstarttls.csv', 'a', newline=''))
    f.writerow([servername, checkstarttls])


if __name__ == '__main__':
    try:
        args = get_args()
        checktls(args)
    except Exception:
        print("Error launch:")
        traceback.print_exc()
