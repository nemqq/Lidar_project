# This is the main program used in the thesis does test algorithms and lidar library.
# 01.01.2022 Kamil Sikora <kamil.sikora@student.po.edu.pl>


import time
import openpyxl
import openpyxl as xl
import numpy as np

from rplidar import RPLidar
from Modules import eks, lidr, navi


# The functions below are examples of using the rplidar
# library together with the lidar slamtec a1
def reading():
     """
     Function gets data form specific angle range (330 - 30 degree)
     """

     lidar = RPLidar('com3')  # sets port COM
     i = 0
     dist = []
     start_angle = 0
     angle = 0
     p = 0
     print('START\n')

     for measurment in lidar.iter_measurments():
          print('angle : ' + str(measurment[2]))
          print('distance : ')
          print(measurment[3])
          print('this is probe nr. : '+str(i)+'\n')

          if i == 0:
               i += 1
               continue

          if i == 1:
               start_angle = int(measurment[2])
               print('start angle : ' + str(start_angle))
          else:
               angle = measurment[2]

          if start_angle > 330:
               print('execute variant 1')
               if (angle > 330 and i > 59) or (p != 0):  # (kat <30 and i > 59):
                    dist.append(measurment[3])
                    print('var 1 save at probe '+str(i))
                    p += 1
                    if angle > 30 and p > 45:
                         print('var 1 break at ' + str(i))
                         break

          elif start_angle < 30:
               print('execute variant nr. 2')
               if (angle > 330 and i > 29) or (p != 0):  # (kat <30 and i > 29):
                    dist.append(measurment[3])
                    print('var 2 save at probe : ' + str(i))
                    p += 1
                    if angle > 30 and p > 45:
                         print('var 2 break at : ' + str(i))
                         break

          elif (start_angle < 330 and start_angle > 30):
               print('execute variant 3')
               if angle > 330 or p != 0:  # kat <30:
                    print('var 3 save at probe : ' + str(i))
                    dist.append(measurment[3])
                    p += 1
                    if angle > 30 and p > 45:
                         print('var 3 break at : ' + str(i))
                         break

          else:
               print('something went wrong')
               break

          if i == 700:
               break

          else:
               i += 1
     print(str(i))
     print(str(dist))
     return dist


def save_data_to_txt():
     """
     Function save data form lidar to txt file
     """
     amount = 0

     for i in range(10):
          print("error or ? : " + str(i))
          try:
               dist_2 = reading()
               my_tab_1 = (lidr.conversion(dist_2,1,1,10))
               # lidr.save_table("Dane_3.txt",my_tab_1)
               print("save : "+str(i))
               amount += 1
          except:
               print("error ex")
               time.sleep(3)
               continue

     print("records : " + str(amount))
     print('end')


def save_data_to_xlsx(data_1, kol):
     """
     Function save data to excel sheets
     :param data_1:
     :param kol: number od chosen column in data sheet
     """
     try:
          sheet_1 = eks.Excel()
          name_1 = 'Test_14.xlsx'

          if len(data_1) == 1:
               sheet_1.save_data_row(name_1, data_1[0], 1, kol, True)

          elif len(data_1) == 2:
               sheet_1.save_data_row(name_1, data_1[0], 1, kol, True)
               sheet_1.save_data_row(name_1, data_1[1], 20, kol, True)

          elif len(data_1) == 3:
               sheet_1.save_data_row(name_1, data_1[0], 1, kol, True)
               sheet_1.save_data_row(name_1, data_1[1], 20, kol, True)
               sheet_1.save_data_row(name_1, data_1[2], 40, kol, True)

          else:
               print('list is empty')

     except PermissionError:
          print('You have open sheet!! CLOSE TO CONTINUE!!')

     print('\nend')


def standard_run():
     k=0
     try_ok = 0

     for k in range(3):

          try:
               try_ok+=1
               dist_1 = reading()
               my_tab_1 = (lidr.conversion(dist_1,1,1,10))
               # my_tab_ref = [my_tab_1[0],my_tab_1[1],my_tab_1[2]]
               # my_tab_ref = [187,186,183]
               my_tab_ref = [my_tab_1[1],my_tab_1[2],my_tab_1[3]]
               dane = lidr.pre_detection(my_tab_1,my_tab_ref,15)
               lazik = navi.Vehicle()
               lazik.clr_danger(my_tab_1, dane)
               # print(do_zapisu)
               # zapisz_Dane_do_xlsx(do_zapisu,try_ok)

          except:
               print("error ex")
               time.sleep(0.1)
               continue

     print('there was a try : '+str(k))
     print('end')
     print('program end')


def test_modules():
     tab_ref = [205,204,203,202,201,199,198,197,196,195,194,193,192,191,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,210]
     tab_1 =   [205,0,111,111,151,129,128,0,0,195,224,223,192,220,220,221,222,223,224,225,226,227,250,250,190,190,190,190,190,192,293,207,208,209,210,0,205,200,190,192,193,195,198,200,205,180,180,209,210]

     print(str(len(tab_1)) +"  " +str(len(tab_ref)))
     # lidr.detection_tab_ref(tab_1,tab_ref)
     dane = lidr.pre_detection(tab_1, tab_ref, 8)
     # lazik=Vehicle()
     # lazik.clr_danger(tab_1,dane)


# PROGRAM STARTS HERE!
if __name__ == "__main__":

     print('First Line')
     # test_modules()
     # standard_run()








