import checkBox
import pygame as pg

def main():
    WIDTH = 800
    HEIGHT = 600
    display = pg.display.set_mode((WIDTH, HEIGHT))

    chkbox = checkBox.Checkbox(display, 400, 400)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()
            chkbox.update_checkbox(event)

        display.fill((200, 200, 200))
        chkbox.render_checkbox()
        pg.display.flip()

if __name__ == '__main__': main()