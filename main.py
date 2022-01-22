

# This is the main program used in the thesis does test algorithms and lidar library.
# 01.01.2022 Kamil Sikora <kamil.sikora@student.po.edu.pl>



from rplidar import RPLidar
import lidr
import time
import eks
from navi import Vehicle
import openpyxl as xl
import openpyxl
import numpy as np





def pomiar():
     lidar = RPLidar('com3')
     i = 0
     odleglosc = []
     kat_p = 0
     kat = 0
     p=0
     print('START')
     print()
     for measurment in lidar.iter_measurments():
          #print(measurment)
          print('kat to : '+ str(measurment[2]))
          print('odlegosc to: ')
          print(measurment[3])
          print('to jest probka nr : '+str(i))
          print()

          if i == 0:
               i+=1
               continue

          if i ==1:
               kat_p = int(measurment[2])
               print('kat poczatkowy to '+str(kat_p))
          else:kat=measurment[2]

          if kat_p > 330:
               print('wykonuje wariant 1')
               if (kat >330 and i > 59) or (p != 0): # (kat <30 and i > 59):
                    odleglosc.append(measurment[3])
                    print('wariant 1 zapis na probce '+str(i))
                    p+=1
                    if kat>30 and p > 45:
                         print('wariant 1 break na ' + str(i))
                         break

          elif kat_p < 30:
               print('wykonuje wariant 2')
               if (kat >330 and i > 29) or (p != 0): # (kat <30 and i > 29):
                    odleglosc.append(measurment[3])
                    print('wariant 2 zapis na probce ' + str(i))
                    p+=1
                    if kat > 30 and p >45:
                         print('wariant 2 break na ' + str(i))
                         break
          elif kat_p <330 and kat_p > 30:
               print('wykonuje wariant 3')
               if kat> 330 or p != 0: # kat <30:
                    print('wariant 3 zapis na probce ' + str(i))
                    odleglosc.append(measurment[3])
                    p += 1
                    if kat > 30 and p > 45:
                         print('wariant 3 break na ' + str(i))
                         break

          else:

               print('cos poszlo nie tak ')
               break




          if i==700:

               break
          else:i+=1




     print(str(i))
     print(str(odleglosc))
     return odleglosc

def zapisz_Dane_do_txt():
     ile = 0
     for i in range(10):
          print("blad czy nie : " + str(i))
          try:
               odl = pomiar()
               my_tab_1 = (lidr.conversion(odl,1,1,10))
               lidr.save_table("Dane_3.txt",my_tab_1)
               print("zapis : "+str(i))
               ile += 1
          except:
               print("blad ex")
               time.sleep(3)
               continue
     print("zapisów : " + str(ile))
     print('koniec')


def zapisz_Dane_do_xlsx(dane,kol):
     print('zaczynamy')
     try:

          Arkusz_1 = eks.Eksel()
          nazwa_1 = 'Test_14.xlsx'
          #Arkusz_1.stworz(nazwa_1)


          if len(dane)==1:
               Arkusz_1.zapisz_dane_row(nazwa_1, dane[0], 1, kol, True)

          elif len(dane)==2:
               Arkusz_1.zapisz_dane_row(nazwa_1,dane[0],1,kol,True)
               Arkusz_1.zapisz_dane_row(nazwa_1, dane[1], 20, kol, True)

          elif len(dane)==3:
               Arkusz_1.zapisz_dane_row(nazwa_1,dane[0],1,kol,True)
               Arkusz_1.zapisz_dane_row(nazwa_1,dane[1], 20, kol, True)
               Arkusz_1.zapisz_dane_row(nazwa_1,dane[2], 40, kol, True)
          else:print('tablica jesst pusta')



     except PermissionError:
          print('MASZ OTWARTY ARKUSZ ZAMKNIJ GO ZEBY KONTYNUOWAC !!')

     print()
     print('koniec')




#zapisz_Dane_do_txt()

'''
ile=6


for i in range(5):
     print("blad czy nie : " + str(i))
     try:
          ile += 1
          odl = pomiar()
          my_tab_1 = (lidr.conversion(odl,1,1,10))
          zapisz_Dane_do_xlsx(my_tab_1,ile)
          print("zapis : "+str(i))

     except:
          print("blad ex")
          time.sleep(2)
          continue
'''
'''
k=0
try_ok = 0
for k in range(3):

     try:
          try_ok+=1
          odl = pomiar()

          my_tab_1 = (lidr.conversion(odl,1,1,10))
          #my_tab_ref = [my_tab_1[0],my_tab_1[1],my_tab_1[2]]
          #my_tab_ref = [187,186,183]
          my_tab_ref = [my_tab_1[1],my_tab_1[2],my_tab_1[3]]
          dane = lidr.pre_detection(my_tab_1,my_tab_ref,15)
          lazik = Pojazd()
          lazik.clr_danger(my_tab_1, dane)
          #print(do_zapisu)
          #zapisz_Dane_do_xlsx(do_zapisu,try_ok)

     except:
          print("blad ex")
          time.sleep(0.1)
          continue


print('bylo prob : '+str(k))
print('koniec')

print('koniec programu')

'''
print("hello")