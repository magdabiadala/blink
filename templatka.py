# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
import time, random
#from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = True
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################

#stary program liczący mrugnięcia
    '''win = visual.Window([400,400])
    message = visual.TextStim(win, text='init')
    message.autoDraw = True
    win.flip()
    core.wait(2.0)

    cnt_blinks = 0

    while True:
        if blink.value == 1:
            print('BLINK!')
            blink.value = 0
            cnt_blinks +=1
            message.setText(str(cnt_blinks))
            win.flip()
        if 'escape' in event.getKeys():
            print('quitting')
            quit_program.set()
        if quit_program.is_set():
            break'''

### ZMIENNE ###

    run = True
    sec1 = 0
    sec2 = 0
    cnt = 0
    X = 800
    Y = 400
    green = (0, 255, 0)
    black = (0, 0, 0)
    red = (255, 0, 0)
    #losuje liczbę
    rnd = random.randint(3, 10)
    #zamienia ją na stringa
    number = str(rnd)

### INICJALIZACJA GRY ###

    pg.init()
    #tworzenie okienka
    win = pg.display.set_mode((X, Y))
    #opis okienka
    pg.display.set_caption("Symulator stacji benzynowej")
    #wybór czcionki
    font = pg.font.Font('freesansbold.ttf', 32)

### EKRAN POCZĄTKOWY ###

    #instrukcja
    ins_txt1 = "Mrugnij, gdy licznik będzie równy"
    ins_txt2 = "czerwonej liczbie na górze okienka."
    #wygląd instrukcji
    instructions1 = font.render(ins_txt1, True, green, black)
    instructions2 = font.render(ins_txt2, True, green, black)
    #umieszcza instrukcję na prostokącie
    insRect1 = instructions1.get_rect()
    insRect2 = instructions2.get_rect()
    #umieszcza prostokąt z tekstem na środku okienka
    insRect1.center = (X // 2, Y // 3)
    insRect2.center = (X // 2, Y * (2/3))
    #nałożenie instrukcji na prostokąt (warstwy)
    win.blit(instructions1, insRect1)
    win.blit(instructions2, insRect2)
    #odświeżenie okienka
    pg.display.flip()
    #czeka 5 sekund - czas na przeczytanie
    pg.time.delay(5000)

    #wyświetla czarny ekran po instrukcji
    pg.draw.rect(win, black, (0, 0, 800, 400))
    pg.display.flip()
    pg.time.delay(1000)

    #wyświetla wylosowaną liczbę
    ran_num = font.render(number, True, red, black)
    textRect1 = ran_num.get_rect()
    textRect1.center = (X // 2, Y // 4)
    win.blit(ran_num, textRect1)
    pg.display.flip()
    pg.time.delay(1000)

### ODLICZANIE ###
    i = 1
    l = 3
    countdown = font.render("Odliczanie", True, green, black)
    cRect = countdown.get_rect()
    cRect.center = (X // 2, Y // 2)
    win.blit(countdown, cRect)
    pg.display.flip()
    pg.time.delay(1000)
    pg.draw.rect(win, black, (0, 150, 800, 250))
    pg.display.flip()
    while i<4:
        l = str(l)
        licznik = font.render(l, True, green, black)
        rect = licznik.get_rect()
        rect.center = (X // 2, Y // 2)
        win.blit(licznik, rect)
        pg.display.flip()
        pg.time.delay(1000)
        l = int(l)
        l -=1
        i +=1
    start = font.render("START", True, green, black)
    sRect = start.get_rect()
    sRect.center = (X // 2, Y // 2)
    win.blit(start, sRect)
    pg.display.flip()
    pg.time.delay(1000)
    pg.draw.rect(win, black, (0, 150, 800, 250))
    pg.display.flip()

### GRA ###

    text = font.render("", True, green, black)
    textRect2 = text.get_rect()
    textRect2.center = (X // 2, Y // 2)
    win.blit(text, textRect2)
    pg.display.flip()
    #TU!
    #get_ticks zwraca liczbę milisekund od wywołania pg.init()
    sec1 = int(pg.time.get_ticks()/1000)
#    print(pg.time.get_ticks())

    blink.value = 0
    print(blink.value)

    while run:
        #stara wersja wychodzenia z gry
        '''for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False'''

        # jeśli wcisniesz esc to kończysz grę i program
        if 'escape' in event.getKeys():
            print('quitting')
            quit_program.set()
        if quit_program.is_set():
            break

        keys = pg.key.get_pressed()

        ##########################
        # JEŚLI CHCESZ GRAĆ SPACJĄ
        # zakomentuj linijki 240 i 243
        ##########################

#        if keys[pg.K_SPACE]:

        ##########################
        #JEŚLI MRUGNIĘCIAMI
        #zakomentuj 233
        ##########################

        if blink.value == 1:

#            print('BLINK!')
            blink.value = 0
            pg.time.delay(1000)
            if (cnt-rnd<0):
                score = 10 - ((cnt-rnd)*(-1))
            else:
                score = 10 - (cnt-rnd)
#            print("score: ")
#            print(score)
            score = str(score)
            result = font.render("Twój wynik to:", True, green, black)
            scr = font.render(score, True, green, black)
            rRect = result.get_rect()
            sRect = scr.get_rect()
            rRect.center = (X // 2, Y * (3/4))
            sRect.center = (X // 2, Y * (7/8))
            win.blit(result, rRect)
            win.blit(scr, sRect)
            pg.display.flip()
            pg.time.delay(3000)

        sec2 = int(pg.time.get_ticks()/1000)
        #jeśli czas który upłynął między sec1 a sec2 to 1 sekunda:
        if sec2 - sec1 == 1:
            sec1 = sec2
            cnt += 1
            print(cnt)
            cnt = str(cnt)
            #aktualizacja zmiennej text
            text = font.render(cnt, True, green, black)
            textRect2 = text.get_rect()
            textRect2.center = (X // 2, Y // 2)
            win.blit(text, textRect2)
            pg.display.flip()
            #zamiana z string na int
            cnt = int(cnt)



    pg.quit()

# Zakończenie podprocesów
    proc_blink_det.join()
