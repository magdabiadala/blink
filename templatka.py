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
    white = (255, 255, 255)
    yellow = (255, 255, 0)
#ustaw prędkość na 1 lub więcej (do 50 jest ok)
    speed = 50
    spd = 1000/speed
    start = 2 * speed
    stop = 9 * speed

### FUNKCJE ###

    ### FUNKCJA WYŚWIETLAJĄCA NAPIS ###
    #content - napis lub wartość do wyświetlenia
    #colour - kolor napisu
    #cX - środek napisu na osi x
    #cY - środek napisu na osi y

    def show(content, colour, cX, cY):
        if isinstance(content, str):
            text = font.render(content, True, colour, black)
            tRect = text.get_rect()
            tRect.center = (cX, cY)
            win.blit(text, tRect)
            pg.display.flip()
        elif isinstance(content, int):
            content = str(content)
            show(content, colour, cX, cY)

    ### FUNKCJA ZAKRYWAJĄCA NAPIS ###
    #sX - lewy, górny róg na osi x
    #sY - lewy, górny róg na osi y
    #wide - szerokość
    #height - wysokość

    def hide(sX, sY, wide, height):
        pg.draw.rect(win, black, (sX, sY, wide, height))
        pg.display.flip()

    ### ODLICZANIE ###

    def countdown():
        i = 1
        l = 3
        show("Odliczanie", white, X//2, Y//2)
        pg.time.delay(1000)
        hide(0, 150, 800, 250)
        while i<4:
            show(l, white, X//2, Y//2)
            pg.time.delay(1000)
            l -=1
            i +=1
        show("START", white, X//2, Y//2)
        pg.time.delay(1000)
        hide(0, 150, 800, 250)

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
    show(ins_txt1, green, X//2, Y//3)
    show(ins_txt2, green, X//2, Y *(2/3))
    #czeka 5 sekund - czas na przeczytanie
    pg.time.delay(3000)
    #wyświetla czarny ekran po instrukcji
    hide(0, 0, X, Y)
    pg.time.delay(1000)

### GRA ###

    while run:
        if 'escape' in event.getKeys():
            print('quitting')
            quit_program.set()
        if quit_program.is_set():
            break

        #losuje liczbę
        rnd = random.randint(start, stop)
        #wyświetla wylosowaną liczbę
        show(rnd, green, X//2, Y//4)
        pg.time.delay(1000)
        countdown()

        show("", white, X//2, Y//2)
        cnt = 0
        #get_ticks zwraca liczbę milisekund od wywołania pg.init()
        sec1 = int(pg.time.get_ticks()/spd)

        blink.value = 0
#        print(blink.value)

        while True:
            # jeśli wcisniesz esc to kończysz grę i program
            if 'escape' in event.getKeys():
                print('quitting')
                quit_program.set()
            if quit_program.is_set():
                run = 0
                break

        # JEŚLI CHCESZ GRAĆ SPACJĄ

            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:

        #JEŚLI MRUGNIĘCIAMI

#            if blink.value == 1:
#                blink.value = 0

        #######################

                pg.time.delay(1000)
                if (cnt - rnd != 0):
                    if (cnt - rnd < 0):
                        score = (cnt - rnd)*(-1)
                    else:
                        score = cnt - rnd
                    show("Pomyliłeś się o:", red, X//2, Y *(3/4))
                    show(score, red, X//2, Y *(7/8))
                else:
                    show("BRAWO!", yellow, X//2, Y *(3/4))
                pg.time.delay(3000)
                hide(0, 0, X, Y)
                break

            sec2 = int(pg.time.get_ticks()/spd)
            #jeśli czas który upłynął między sec1 a sec2 to 1 sekunda (dla speed = 1)
            if sec2 - sec1 == 1:
                sec1 = sec2
                cnt += 1
#                print(cnt)
                show(cnt, white, X//2, Y//2)

    pg.quit()

# Zakończenie podprocesów
    proc_blink_det.join()
