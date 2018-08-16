import os

def getRSSI(interface):
        dic_rssi = {}
        file_in, file_out, file_error = os.popen3('iw dev ' + interface + ' station dump')
        if file_error.read():
                print 'Help > Check wlan interface name'
                return True, dic_rssi
        else:
                str_result = file_out.read().split('\n')
                str_addr = ''
                for str_line in str_result:
                        if str_line.find('Station') >= 0:
                                str_addr = str_line.split(' ')[1]
                        if str_line.find('signal') >= 0:
                                dic_rssi[str_addr] = str_line.split('\t')[2].split(' ')[0]
                return False, dic_rssi
