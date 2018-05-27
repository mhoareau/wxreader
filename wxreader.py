#Program to read weewx and output Arne Henrikson format for Xastir or other apps
#Written by Stephen Hamilton

import socket
import sys
import time
import mysql.connector

def main():
    #Xastir client ip address
    xastir_addr = ('192.168.1.11', 8888)
    # Create a TCP/IP socket
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    # Bind the socket to the port
    server_address = ('localhost', 8888)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    sock.listen(1)
    connection, client_address = sock.accept()
    data = connection.recv(4096)
    print >>sys.stderr, 'received "%s"' % data
    while True:
        #print "Sending output"
        data = getweatherpacket()
        
        print ("Waiting to receive")
        #data, server = sock.recvfrom(4096)
        
        print >>sys.stderr, 'Sending "%s"' % data
        connection.sendall(data)
        #sent = sock.sendto(data)
        time.sleep(5) 
        

def getweatherpacket():
    #MySQL String
    cnx = mysql.connector.connect(user='weewx', database='weewx', host='ipa', password='')
    cursor = cnx.cursor()
    sqlstring = "select outTemp, windSpeed, windGust, windDir, rainRate, rain, outHumidity, barometer, pressure from archive order by dateTime desc limit 1;"
    #Replace with mysql command to get latest weather
    #Format:
    #temp(C), maxT(C), minT(c), wd->anem_mps, wd->anem_gust /*peak_speedMS*/,
    #wd->anem_speed_max * 0.447040972 /*max_speedMS*/,
    #wd->vane_bearing - 1 /*current_dir*/,
    #wd->vane_mode /*max_dir*/,
    #wd->rain_rate /*rain_rateI*/,                                   #H
    #            T    MT   mT    spd   #b                              #H
    swxstring = "17.7 38.7 19.7 .44704 .70 30.0 4 5 30.0 40.0 50.0 60.0 24 2 3 4 5 6 7 8 9 10\r\n"
    #print("Sample\n")
    wxstring = ""
    #print swxstring
    cursor.execute(sqlstring)
    row = cursor.fetchone()
    
    # Modified by Mickael Hoareau for Enzo Becamel
    sql_rain = "select sum from archive_day_rain order by dateTime desc limit 1;"
    cursor.execute(sql_rain)
    row_rain = cursor.fetchone()
    
    #print (row)
    temp = (row[0]-32)*5/9
    wxstring = '{:03.1f}'.format(temp) #outside temp
    wxstring = wxstring + " " + '{:03.1f}'.format(temp) #max temp
    wxstring = wxstring + " " + '{:03.1f}'.format(temp) #min temp

    wxstring = wxstring + " " + '{:03.1f}'.format(row[1]*1.609/3.66) #speed
    wxstring = wxstring + " " + '{:03.1f}'.format(row[2]*1.609/(3.66)) #gust
    if (row[3] == None):
        winddir = 0
    else:
        winddir = int((row[3]/22.5)+.5)
    wxstring = wxstring + " 0.0 " + str(winddir) #maxspeed (unused), bearing
    wxstring = wxstring + " 1 " + '{:03.3f}'.format(row[4]) #max_dir (unused), rainrate
    wxstring = wxstring + " " + '{:02.2f}'.format(row_rain[0]) #rain
    wxstring = wxstring + " 6.0 5.0 " + '{:03.3f}'.format(row[6]) #outHumidity
    wxstring = wxstring + " 1.0 1.0 " + '{:03.3f}'.format(row[7]) #RHmax (unused), rhmin(unused), barometer    print ("sending %s" % wxstring)
    wxstring = wxstring + " 1.0 1.0 1.0 1.0 1.0 1.0 1.0\r\n"
    cursor.close()
    return wxstring


if __name__ == "__main__":
    main()
