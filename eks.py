'''

Biblioteka do zapisu danych z lidara to eksela


'''

import openpyxl as xl
from openpyxl.chart import LineChart , Reference



def fnc2(table, m_nazwa_p ):
    '''
    Funkcja wpisuje dane z talbicy do pliku txt


    :param table: tablica
    :param m_nazwa_p: nazwa pliku txt (nazwa musi zawierac rozszerzenie .txt)
    :return:
    '''
    try :
        with open(m_nazwa_p, "r+") as f:
            text = f.readlines()
            licznik = (len(text)) + 1
            f.write("Dane nr ... : " + str(licznik) +"  "+ str(table) + "\n")

    except FileNotFoundError:
        testscik = open(m_nazwa_p,"w")
        testscik.close()
        print("plik o nawie " + m_nazwa_p + "zostal utworzony")



class Excel():
    '''
    Klasa z funkcjami do wpisywania danych do escela


    '''


    def stworz(self,name):
        '''
        Stworz plik z roszerzeniem xlsx
        :param name: nazwa z roszerzeniem xlsx
        :return:
        '''

        try:
            wb = xl.load_workbook(name)
            wb.save(name)
            print('PLIK NIE ZOSTAL UTWORZONY PONIEWAZ JUZ ISTNIEJE')

        except:

            wb = xl.Workbook()
            ws = wb.active
            ws.title = 'Data_1'
            wb.save(name)
            print('PLIK ZOSTAL UTWORZONY POMYSLNIE')

    def save_data_row(self, name, tabe_1, u_row, u_col, case = True):
        '''
        Zapis danych do akrusza

        :param name: nazwa pliku z rozszerzeniem
        :param tabe_1: dane z tablicy
        :param u_row: poczatkowy rzad
        :param u_col: poczatkowa kolumna
        :param case: True - zapisz w dol , False - zapisz poziomo
        :return:
        '''


        wb = xl.load_workbook(name)
        ws = wb.active


        if case == True:
            if u_row == 0:
                t = 1
            else:
                t = u_row
            for row in range(len(tabe_1)):
                ws.cell(row + t, u_col, tabe_1[row])
        if case== False:
            if u_col == 0:
                t = 1
            else:
                t = u_col
            for col in range(len(tabe_1)):
                ws.cell(u_row, col+t, tabe_1[col])

        wb.save(name)

    def zapisz_dane_apend(self,name,tabe_1 ):
        '''
        Dodaj apend
        :param name:  nazwa pliku z rozszerzeniem
        :param tabe_1:  dane z tablicy
        :return:
        '''
        wb = xl.load_workbook(name)
        ws = wb.active
        ws.append(tabe_1)

        wb.save(name)

    def stworz_wykres(self,name):
        '''
        Funkcja nie dopracowana
        :param name:
        :return:
        '''
        wb = xl.load_workbook(name)
        ws = wb.active


        values = Reference(ws, min_col=1, min_row=1, max_col=1, max_row=19)
        chart = LineChart()
        chart.title = 'Dane nr 1'
        chart.style = 1
        # chart.x_axis.title='nr probki'
        # chart.y_axis.title='odleglosc cm '
        chart.add_data(values)
        ws.add_chart(chart, "E15")

        wb.save(name)
