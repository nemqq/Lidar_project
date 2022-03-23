# Avoiding obstacles
# This module contains a set of functions for processing data obtained from lidar.
# 01.01.2022 Kamil Sikora <kamil.sikora@student.po.edu.pl>


class Vehicle:

    def __init__(self, track_width=50, ground_clearance=20, v_width=70, wheel_width=10, v_length=100):
        self.wheel_offset = track_width
        self.heigh = ground_clearance
        self.width = v_width
        self.wheel_width = wheel_width
        self.length = v_length

    def clr_danger(self, tab, data):
        # step 1
        dl_point = 170 / len(tab)
        print(dl_point)
        print(len(tab))
        print(data)
        vehicle_width = round(self.width / dl_point)
        wheel_offset_p = round(self.wheel_offset/dl_point)
        wheel_width_p = round(self.wheel_width/dl_point)
        print('wheel')
        print(wheel_width_p)
        main_probe = []
        print('width')
        print(vehicle_width)
        print(wheel_offset_p)
        for n in range(len(tab)):
            main_probe.append(n+1)
        main_probe_copy = main_probe.copy()
        obstacle_inf = data[0]
        probe = data[1]
        holes = []
        obstacles = []

        # selection for holes and obstacles
        for count, tt in enumerate(obstacle_inf):
            if not tt['type']:
                holes.append(list(probe[count]))
            else: obstacles.append(list(probe[count]))

        print('data at selection for holes and obstacles ')
        print(obstacles)
        print(holes)

        # checking which hole is passable
        to_remove2 = []
        to_remove = []
        test_tab = []
        for c, a in enumerate(holes):
            if len(a) > wheel_offset_p:
                print(str(len(a)) + 'hole is at first condition')
                to_remove2.append(False)
            elif len(a) < wheel_offset_p and len(a) < wheel_width_p:
                print(str(len(a)) + 'hole is small vehicel can drive')
                to_remove2.append(True)
            else:
                print(str(len(a)) + 'hole is large vehicle cant drive')
                to_remove2.append(True)
                to_remove.append(list(holes[c]))
                print(to_remove)
        print('to_remove2  : '+str(list(to_remove2)))

        # checking that the ground clearance is high enough to drive
        c = 0
        cl = 0
        for t in obstacle_inf:
            if t['type']:
                if t['high'] == 0:
                    # print(probe[c])
                    print(probe)
                    probe.pop(c)
                else:
                    c += 1
            else:
                if to_remove2[cl]:
                    print(probe)
                    probe.pop(c)
                else:
                    c += 1
                cl += 1

        print('probe after checking that the ground clearance is high enough to drive')
        print(probe)
        varr = []
        varr2 = []
        for k in probe:
            for p in k:
                varr.append(p)
        for element in varr:
            if element in main_probe:
                main_probe.remove(element)
        main_probe_end = main_probe.copy()
        for jj in to_remove:
            for clear in jj:
                varr2.append(clear)
        for el in varr2:
            if el in main_probe_end:
                main_probe_end.remove(el)
        # checking if it is possible to run through the hole
        print('checking')
        print(main_probe)
        print(main_probe_end)

        # finding space to travel
        goout = 0
        start = 0
        result = []

        f = False
        for i in range(len(main_probe_end)-1):
            if (main_probe_end[i+1] - main_probe_end[i]) == 1:
                goout += 1
                if start == 0 and i == 0:
                    start = 0
                    f = True
                elif start == 0 and f == False:
                    start = i
                if goout == vehicle_width:
                    w_wyn = main_probe_end[start]
                    result.append(w_wyn)
                    # break
            else:
                goout = 1
                start = 0
                f = False
        print(result)

        # finding if is free room under vehicle
        ends = []
        beginnings = []

        for ccl in to_remove:
            ends.append(ccl[len(ccl)-1])
            beginnings.append(ccl[0])
        print('ends & beginnings')
        print(beginnings)
        print(ends)
        end_flag = True
        end_probe = 0
        try_flag = True
        revert_result = []

        for num, ray in enumerate(to_remove):
            end_flag = True
            try_flag = True
            start = ray[0]
            start_index = main_probe.index(start)
            end = ray[len(ray)-1]
            print(str(start) + ' ... ' + str(end))
            print(wheel_width_p+1)
            main_probe_cc = main_probe.copy()

            for num2 in range(len(beginnings)):
                if num2 != num:
                    print(beginnings[num2])
                    print(ends[num2])
                    main_probe_cc.remove(beginnings[num2])
                    main_probe_cc.remove(ends[num2])
            print(main_probe_cc)
            end_index = main_probe_cc.index(end)
            print('end index to : '+str(end_index))

            for check in range(wheel_width_p+1):
                print(start-(check+1))
                if (main_probe_cc[start_index-(check+1)] - main_probe_cc[start_index-(check+1)-1]) == 1:
                    print("it's ok to drive : " + str(main_probe_cc[start_index-(check+1)-1]))
                    if check == wheel_width_p:
                        print('last: ' + str(main_probe_cc[start_index - (check + 1) - 1]))
                        end_probe = main_probe_cc.index(main_probe_cc[start_index-(check+1)-1])
                else:
                    print("it's ok to drive")
                    end_flag = False
                    break

            if end_flag:
                for check3 in range(vehicle_width):
                    print(main_probe_cc[end_probe + check3])
                    if main_probe_cc[end_probe + check3 + 1] - main_probe_cc[end_probe + check3] == 1:
                        print('width ok')
                        if check3 == vehicle_width-1:
                            result.append(main_probe_cc[end_probe])
                    else:
                        print('width no ok')
                        break

            if end_flag and try_flag:
                for check2 in range(wheel_width_p+1):
                    if (main_probe_cc[end_index+(check2+1)] - main_probe_cc[end_index + check2]) == 1:
                        print("it's ok !")
                        print(main_probe_cc[end_index+(check2+1)])
                        if check2 == wheel_width_p:
                            print('last2: ' + str(main_probe_cc.index(main_probe_cc[end_index+(check2+1)])))
                            end_probe2 = main_probe_cc.index(main_probe_cc[end_index+(check2+1)])
                            print(main_probe_cc[end_probe2])
                    else:
                        end_flag = False
                        print('wrong')
                        break
            if end_flag and try_flag:
                for check4 in range(vehicle_width):
                    print(main_probe_cc[end_probe2 - check4])
                    print(main_probe_cc[end_probe2 - check4 - 1])
                    if main_probe_cc[end_probe2 - check4] - main_probe_cc[end_probe2 - check4 - 1] == 1:
                        # (main_probe_cc[start_index - (check + 1)] - main_probe_cc[start_index - (check + 1) - 1]) == 1:
                        print('width ok')
                        if check4 == vehicle_width-1:
                            revert_result.append(main_probe_cc[end_probe2])
                    else:
                        print('width not ok')
                        break
        print(result)
        print(revert_result)

        # optimization if there is no second space closer to the center
        if len(result) > 1:
            dist = len(tab)/2
            z_pom = result[0]
            wart_opt = []
            for dl in result:
                 wart_opt.append(abs(dist-dl))

            for val in wart_opt:
                if min(wart_opt) == val:
                    odp_indx = wart_opt.index(val)
                    break

            odp = result[odp_indx]
        elif len(result) == 1:
            odp = result[0]
        else:
            print('no result')
        if result:
            print("\n\n :it's okey to drive " + str(round((odp * dl_point), 2)) + 'cm from 0 point')
        else:
            print("\n\n\nit's not okey to drive")
