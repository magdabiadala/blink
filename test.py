import pygame as pg

pg.init()

win = pg.display.set_mode((400,400))

run = True
clock = pg.time.Clock()
sec1 = int(pg.time.get_ticks()/1000)
sec2 = 0
cnt = 0

print(pg.time.get_ticks()/1000)

while run:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
    sec2 = int(pg.time.get_ticks()/1000)
    if sec2 - sec1 == 1:
        sec1 = sec2
        cnt += 1
        print(cnt)
        str(cnt)
        czy = isinstance(cnt, int)
        print(str(czy))


pg.quit()
