
# Obstacle detection
# This module contains a set of functions for processing data obtained from lidar.
# 01.01.2022 Kamil Sikora <kamil.sikora@student.po.edu.pl>


from math  import  sin, radians

def conversion(tab_cov,dig,case,split):
    tab_cm = [0] * len(tab_cov)
    k = 0

    for i in tab_cov:
        tab_cm[k] = i / split
        k += 1

    #rounding
    round_to_tenths = [round(num, dig) for num in tab_cm]
    if case == 1 :
        return round_to_tenths
    else:
        return tab_cm

def check_angle(high_lidr,dist_lidr):
    for i in range (20,70):
        dist = (high_lidr/(sin(radians(90-i))))
        if abs(dist-dist_lidr) <1:
            print('result at '+str(dist)+ ' : '+str(i))
            break





def generuj_tablice(kat_p=345,kat_k=300,od_k=210.0,step=2):
    '''
    The function generate arrays from the range given by the user

    :param kat_p:
    :param kat_k:
    :param od_k:
    :param step:
    :return:
    '''

    range = abs(kat_p-kat_k)
    k=-(range/2)
    print(range,k+'\n')
    tab_test=[0]*range
    for i in range(range):
        if k <= 0 :
            od_k -=step
            tab_test[i] = od_k
        else:
            od_k +=step
            tab_test[i] = od_k
        k+=1
    return tab_test


def write_tab(tab):
    '''
    Function write values from list
    :param tab: list to pirnt
    :return:
    '''
    for i in range(len(tab)):
        print('probe nr :'+str(i)+ ' value : '+str(tab[i]))


def average_r(tab):
    '''
    Function return av. of the distance from all values in the array

    :param tab: list with probe
    :return: av. difference between probe
    '''
    difference=[]
    sum = 0
    for i in range(len(tab)-1):
        difference.append(abs(round((tab[i]-tab[i+1]),2)))
    for i in difference:
        sum+=i
    print(difference)
    result = (sum/len(difference))
    return round(result,2)


def Detect_OBST(tab_z,tab_b,r_p):
    '''
    Obstacle qualifying function
    :param tab_z: list with wrong probe
    :param tab_b: list with wrong distance
    :param r_p: type of obstacle
    :return: inforamtion about obstacle
    '''

    #type  0-obstacle ,1-hole
    #high  0-low, 1-high, 2-very high
    #width  0-very smool, 1-small, 2-medium, 3-duza

    object ={'type':False,'high':0,'width':0 }
    obstacle = []
    # very small<1m,  low , 1m - 600cm  high , very high,
    obst_size = []
    for i in tab_z:
        obst_size.append(len(i))

    print(obst_size)

    tab_avg = []
    i=0
    k=0
    c=0
    for i in tab_b:

        for c in i:
            k+=c
        tab_avg.append(round( k / len(i)))
        k=0
    print(tab_avg)

    print('\nhigh obstacles')
    i=0
    k=0
    for i in tab_avg:

        if r_p[k]:
            if i > 134:
                print('przeszkoda nr : ' + str(k+1) + '  jest niska')
                object['high'] = 0
            elif i <134 and i > 60:
                print('przeszkoda nr : '+str(k+1)+'  jest wysoka ')
                object['high'] = 1
            else :
                print('przeszkoda nr : '+str(k+1)+'  jest bardzo wysoka i bardzo blisko')
                object['high'] = 2
        else:
            if i < 180:
                print('dziura nr : ' + str(k+1) + '  jest plytka')
                object['high'] = 0
            elif i <200 and i > 180:
                print('dziura nr : '+str(k+1)+'  jest gleboka ')
                object['high'] = 1
            else :
                print('dziura nr : '+str(k+1)+'  jest bardzo gleboka')
                object['high'] = 2
        k += 1
        obstacle.append(dict(object))

    print('\nwidth obstacles')
    k=0
    for k in range (len(obst_size)):

        if obst_size[k] != 0 :
            if obst_size[k] > 0 and obst_size[k] <= 2 :
                print("przeszkoda nr :" + str(k+1) + "  jest bardzo mala ")   #3,3cm , possible a disturbance
                (obstacle[k])['width'] = 0
            elif obst_size[k]> 2 and obst_size[k]<=4:
                print("przeszkoda nr :" + str(k+1) + "  jest mala ")          #estimated 10cm
                (obstacle[k])['width'] =1
            elif obst_size[k]> 4 and obst_size[k]<10:
                print("przeszkoda nr :" + str(k+1) + "  jest srednia ")       #estimated od 10cm do 30cm
                (obstacle[k])['width'] = 2
            elif obst_size[k] > 10 :
                print("przeszkoda nr :" + str(k+1) + "  jest duza ")          #above 1cm
                (obstacle[k])['width'] =3
    k=0

    print('\ntype')
    for p in r_p:
        k+=1
        if p:
            print('object is {} obstacle'.format(str(k)))
            (obstacle[k - 1])['type'] = p
        else:
            print('object is {} hole'.format(str(k)))
            (obstacle[k-1])['type'] = p

    return obstacle



def pre_detection(tab,ref_tab,u_scope=7.5):
    '''
    Obstacle detection function based on the sample list

    :param tab: list of samples
    :param ref_tab: ref list of samples
    :param range from which an obstacle is detected
    :return: detected obstacle data
    '''



    zero_probe = []
    scope = u_scope
    child_p = ref_tab[0]
    falg = 0
    falga_2 = 0
    last_ok_p=0
    wrong_probes = []
    tab_wrong = []
    tab_measurement_errors = []

    wrong_dist = []
    tab_wrong_dist = []
    obst_hole = False
    r_obst = []

    if (abs(child_p - tab[0]) > scope):
        falg = 1
        falga_2 = 1

    # main loop
    for i in range(len(tab)):
        print('\n beginning of the loop')
        if i < (len(tab))-1:
            print('probe nr. {}' .format(i))
            print('condiction')
            war= round((abs(tab[i]-tab[i+1])),2)
            print(war)


            if ((war<scope)and falg == 0):
                print('probe nr. {}  its ok  ' .format(i+1))

            elif ((war>=scope)or falg != 0):
                print('probe nr. {} could be wrong '.format(i+1))
                falg = 1
                if i == 0 :
                    last_ok_p = child_p

                elif last_ok_p == 0:
                    last_ok_p= tab[i]

                elif (i < (int(len(tab)*(1/3)))) and (i < (int(len(tab)/2))):
                     last_ok_p -= 1.4
                elif(i < (int(len(tab)*(2/3)))) and (i < (int(len(tab)/2))):
                     last_ok_p -= 0.5
                elif (i < (int(len(tab)*(2/3)))) and (i > (int(len(tab)/2))):
                     last_ok_p += 0.5
                elif (i > (int(len(tab)*(2/3)))) and (i > (int(len(tab)/2))):
                     last_ok_p += 1.4
                print('prediction {}'.format(last_ok_p))
                print(round( abs(tab[i+1] - last_ok_p),2))
                war2 =round((abs(tab[i+1] - last_ok_p)),2)
                if (tab[i+1] == 0):
                    print('next probe have value {}' . format(str(tab[i+1])))
                    print('wrong measu. quali')
                    if i == 0 and tab[i]==0:
                        zero_probe.append(i+1)
                    elif i == 0 and tab[i]!=0 and falga_2 == 1 :
                        wrong_probes.append(i+1)
                        wrong_dist.append(tab[i])


                    zero_probe.append(i+2)

                elif round((abs(tab[i+1] - last_ok_p)),2)  >= scope:
                    print('last war. if done - probe nr, {}  its wrong'.format(i+1))
                    if i == 0 and tab[i]==0:
                        zero_probe.append(i+1)
                    elif i == 0 and tab[i]!=0 and falga_2 == 1:
                        wrong_probes.append(i+1)
                        wrong_dist.append(tab[i])

                    wrong_probes.append(i+2)
                    wrong_dist.append(tab[i+1])
                    #test after first probe
                    if last_ok_p < tab[i+1]:
                        obst_hole = False
                    else: obst_hole =True
                else:
                    falg = 0
                    falga_2 = 0
                    last_ok_p = 0
                    print('first was ok -flag set at 0')
                    print(zero_probe,'\n',wrong_probes)
                    if len(zero_probe) != 0 :
                        tab_measurement_errors.append(list(zero_probe))
                        zero_probe.clear()
                    else:
                        print('there were no zero samples')

                    if len(wrong_probes) != 0 :
                        tab_wrong.append(list(wrong_probes))
                        wrong_probes.clear()

                        tab_wrong_dist.append(list(wrong_dist))
                        wrong_dist.clear()
                        r_obst.append(obst_hole)
                    else:
                        print('there were no erroneous measurements')
            else:
                print('something was wrorng at probe {} it has not entered into any condition'.format(str(i)))
        else:
            print('LAST PROBE SAVE')

            falg = 0
            falga_2 = 0
            last_ok_p = 0
            print('probe was oke, flag set on 0')
            print(zero_probe,'\n',wrong_probes)
            # if (int(tab[i+1]) == 0 or int(tab[i]) == 0):
            #
            #     tab_bledy_pomiarowe.append(list(zle_probki))
            #     tab_bledy_pomiarowe_2.append(list(bledne_odl))
            #     zle_probki.clear()
            #     bledne_odl.clear()
            # else
            if len(zero_probe) != 0:
                tab_measurement_errors.append(list(zero_probe))
                zero_probe.clear()
            else:
                print('there were no zero samples')

            if len(wrong_probes) != 0:
                tab_wrong.append(list(wrong_probes))
                wrong_probes.clear()

                tab_wrong_dist.append(list(wrong_dist))
                wrong_dist.clear()
                r_obst.append(obst_hole)
            else:
                print('there were no erroneous measurements')

    # writing out the results & identifying the obstacle
    if tab_wrong != [] or tab_measurement_errors !=[]:
        print('\ntype of obstacle')
        print(r_obst)
        print('\nWRONG PROBE & DISTANCES')
        print(tab_wrong)
        print(tab_wrong_dist)
        print('number of detected obstacles:'+str(len(tab_wrong)))
        print('errors detected on the samples')
        print(tab_measurement_errors)
        return Detect_OBST(tab_wrong,tab_wrong_dist,r_obst) , tab_wrong
    else:
        print('RESULT: NO OBSTACLES DETECTED')
        print("\n\nALGORITHM NR.1")


