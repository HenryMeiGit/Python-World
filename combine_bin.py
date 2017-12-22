# ESP8266 ROM Bootloader Utility
# www.espressif.com
# iot.espressif.cn
# Copyright (C) 2014 Espressif Shanghai
#
# This program is a firmware download tool with a simple graphic user interface.
# Thanks to Fredrik Ahlberg's outstanding work of esptool.py
# Port form XTCOM,which is compiled via visual studio, to python so that it can also be running in linux
# 
# If any bug is figured out ,please send the bug description and console log to wangjialin@espressif.com or wangcostaud@hotmail.com

import sys

VERSION = 'V0.9+'  #used in fdownload_panel_method.py

mode_list=['%c'%0x0,'%c'%0x1,'%c'%0x2,'%c'%0x3]
speed_list=['%c'%0x0,'%c'%0x1,'%c'%0x2,'%c'%0xf]  

size_list=['%c'%0x0,'%c'%0x1,'%c'%0x2,'%c'%0x3,'%c'%0x4,'%c'%0x5,'%c'%0x6,'%c'%0x7]  
crystal_list=['%c'%0x0,'%c'%0x1,'%c'%0x2]

speed_list_d = [0x0,0x1,0x2,0xf]
size_list_d = [0x0,0x1,0x2,0x3,0x4,0x5,0x6,0x7]
crystal_list_d = [0x0,0x1,0x2]


"""combine the detached binary files into one"""
def combineBin(dl,target_name,mode,speed,size,crystal,disable_cfg):
    dl_list = dl
    print "dl_list: \n\r",dl_list
    offset_list = [addr_pair[1] for addr_pair in dl_list]
    offset_list.sort()
    print offset_list
    
    addr_list = [ ]
    for offset in offset_list:
        for addr_pair in dl_list:
            if offset == addr_pair[1]:
                addr_list.append(addr_pair[0])
                break
    print addr_list

    fw=file(target_name,'wb')
    current=0
    for i in range(len(offset_list)):
        print "i: ",i
        for j in range(current,offset_list[i] ):
            fw.write( "%c"%0xff)
        current=offset_list[i]
        fr=open(addr_list[i] , 'rb')
        data=fr.read()
        dlen=len(data)
        fr.close()
        if disable_cfg == 0:
            if offset_list[i]==0x0:
                if VERSION == 'V0.8':
                    data=( data[0:2]+mode_list[mode]+speed_list[speed]+data[4:] )
                elif VERSION == 'V0.9+':
                    size_speed = (size_list_d[size]<<4)|speed_list_d[speed]
                    print "size_speed :",size_speed
                    data=( data[0:2]+mode_list[mode]+'%c'%(size_speed)+data[4:] )
            if 'esp_init_data' in addr_list[i]:
                data = ( data[0:48]+crystal_list[crystal]+data[49:] )
        else:   
            print "========================"
            print "NOTE: BINARY CONFIG DISABLED, "
            print "JUST COMBINE THE ORIGINAL BINARIES"
            print "========================"
        fw.write(data)
        current += dlen
        
    fw.close()
    
 
            
if __name__=="__main__":
    
    spi_speed_dict = {"40m":0,"26.7m":1,"20m":2,"80m":3}
    spi_mode_dict = {"QIO":0,"QOUT":1,"DIO":2,"DOUT":3}
    flash_size_dict = {"4Mbit":0,"2Mbit":1,"8Mbit":2,"16Mbit":3,"32Mbit":4,"16Mbit-C1":5,"32Mbit-C1":6}
    crystal_dict = {"40Mhz":0,"26Mhz":1,"24Mhz":2}
    
    
    file_addr_list = [
            ["../bin/boot_xiaomi_v4_GPIO3.bin",0x0],
            #["../bin/boot_xiaomi_v8.bin",0x0],
            #["../bin/boot_v1.5.bin",0x0],
            #["../bin/boot_xm_150928.bin",0x0],
            #["../bin/boot_v1.4(b1).bin",0x0],
            ["../bin/upgrade/user1.2048.new.5.bin",0x1000],
            ["../bin/blank_16K.bin",0x7c000],
            ["../bin/blank.bin",0x1fe000],
            ["../bin/esp_init_data_default_to_xiaomi_1214.bin",0x1fc000],
            ["../bin/ESP_GPIO_XMQD_26m_115200_20160401.bin",0x101000]
            ]

    print sys.argv[1]
    target_name = "../bin/iflash_yeelink_light_" + sys.argv[1] + "." + sys.argv[2] + ".bin"
    spi_mode = "QIO"
    spi_speed = "40m"
    flash_size = "16Mbit-C1"
    crystal = "26Mhz"
    
    
    combineBin(dl=file_addr_list,#bin-addr-pair list
               target_name=target_name,#target bin name
               mode=spi_mode_dict[spi_mode],#spi read/write mode
               speed=spi_speed_dict[spi_speed],#flash spi clock speed
               size=flash_size_dict[flash_size],#flash size
               crystal=crystal_dict[crystal], #crystal frequency
               disable_cfg=0  #set 1 will disable setting spi configuration
               )
