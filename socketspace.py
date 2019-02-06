import pygame, player, socket, bullet ,Name
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "127.0.0.1"#input("enete number:")#ip address
name=Name.name("Enter Your Name:")[16:]#input("Enter Your Name:")
name=name+" "*(8-len(name))
port = 5005
pygame.init()
pygame.font.init()
screen_x = 800
screen_y = 400
car_x = 50
car_y = 50
fire = 0
enemy_y = 50
playingi1=0
healthbar_x=100
healthbar_y=10
screen = pygame.display.set_mode((screen_x , screen_y))
backgroundimage = pygame.image.load("background.png")
backgroundimage = pygame.transform.scale(backgroundimage, (screen_x, screen_y))
car = pygame.image.load("hero.png")
car1 = pygame.image.load("enemy.png")
car = pygame.transform.scale(car, (car_x, car_y))
car.convert_alpha()
car.set_colorkey((255, 255, 255))
car1 = pygame.transform.scale(car1, (car_x, car_y))
car1.convert_alpha()
car1.set_colorkey((255, 255, 255))
bulletimage = pygame.image.load("bullet1.png")
bulletimage = pygame.transform.scale(bulletimage, (20, 10))
bulletimage.convert_alpha()
bulletimage.set_colorkey((17, 17, 17))
bulletimage1 = pygame.image.load("bullet2.png")
bulletimage1 = pygame.transform.scale(bulletimage1, (20, 10))
bulletimage1.convert_alpha()
bulletimage1.set_colorkey((17, 17, 17))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textplay = myfont.render('START', False, (0, 0, 0))
textexit = myfont.render('EXIT', False, (0, 0, 0))
textplayagain=myfont.render("Play again",False,(0,0,0))
textname=myfont.render(name, False, (0, 0, 0))
textmatching=myfont.render("Matching please wait", False, (0, 0, 0))
textname=pygame.transform.scale(textname,(healthbar_x,30))
textenemy_name=""
userbullets = []
enemybullets = []
pygame.mixer.music.load("3.wav")
enemy_name=""
def end(text):
    screen.blit(backgroundimage, (0, 0))
    te = myfont.render(text, False, (0, 0, 0))
    screen.blit(te, (screen_x // 2 - te.get_width() // 2, screen_y // 4))
    screen.blit(textplayagain, (screen_x // 2 - textplayagain.get_width() // 2, 3*screen_y // 4))
    pygame.display.update()
    while(1):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            if i.type==pygame.MOUSEBUTTONDOWN and i.button==1:
                mx,my=pygame.mouse.get_pos()
                if my>=screen_y//2:
                    main()

def healthbar(h,ii):
    if ii==1:
        xx=10
        color = (0, 255, 0)
        ttname=textname
    else:
        xx=screen_x-healthbar_x-10
        color = (255, 0, 0)
        ttname=textenemy_name
    screen.blit(ttname, (xx, 20))
    pygame.draw.rect(screen, (0,0,0), (xx, 10, healthbar_x, healthbar_y), 2)#box
    pygame.draw.rect(screen, color, (xx, 10, healthbar_x * (h / 100), healthbar_y))#fill health
def update():
    screen.blit(backgroundimage, (0, 0))
    screen.blit(car, (user.x, user.y))
    s.sendto(b"%d %d %d %d 0" % (playingid, (user.y * 100) // screen_y, fire, user.health), (ip, port))
    data, addr = s.recvfrom(1024)
    global enemy_y
    enemy_y, enemy_fire, enemy_health = list(map(int, data.decode().split()))
    if enemy_health <= 0:
        end("you won")
    if user.health <= 0:
        end("you lost")
    if enemy_fire == 1:
        enemybullets.append(bullet.bullet(screen_x - 10 - car_x, (enemy_y * screen_y) // 100 + car_y // 2))
    screen.blit(car1, (screen_x - 10 - car_x, (enemy_y * screen_y) // 100))
    for i in range(len(userbullets)):
        screen.blit(bulletimage, (userbullets[i].x, userbullets[i].y))
    for j in range(len(enemybullets)):
        screen.blit(bulletimage1, (enemybullets[j].x, enemybullets[j].y))
    healthbar(user.health,1)
    healthbar(enemy_health,2)
    pygame.display.update()
def start():
    global user,playingid ,fire,textenemy_name
    screen.blit(backgroundimage, (0, 0))
    screen.blit(textmatching, ((screen_x // 2) - textmatching.get_width() // 2, screen_y // 2))
    pygame.display.update()
    user = player.player(10, screen_y // 2)
    velocity = 10
    ready = 1
    s.sendto(b"-1 0 0 0 %s"%(name.encode()), (ip, port))
    data, addr = s.recvfrom(1024)
    playingid = int(data)
    s.sendto(b"%d %d 0 0 0"%(playingid,ready), (ip, port))
    s.settimeout(0.2)
    while(1):
        try:
            data,addr=s.recvfrom(1024)  # to start the game at the same time
            break
        except:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    s.sendto(b"%d 0 0 0 0" % (playingid), (ip, port))
                    return (0)
    s.settimeout(None)
    enemy_name=data.decode().split()[1]
    enemy_name = enemy_name + " " * (8 - len(enemy_name))
    textenemy_name =myfont.render(enemy_name, False, (0, 0, 0))
    textenemy_name=pygame.transform.scale(textenemy_name, (healthbar_x, 30))
    while (1):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return (0)
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    fire = 1
            if i.type == pygame.MOUSEBUTTONUP:
                if i.button == 1:
                    fire = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        user.y += (mouse_y - user.y) // velocity
        if fire == 1:
            pygame.mixer.music.stop()
            userbullets.append(bullet.bullet(user.x + car_x, user.y + car_y // 2))
            pygame.mixer.music.play(0)
        i = 0
        while (i < len(userbullets)):
            userbullets[i].x += 20
            if screen_x - car_x <= userbullets[i].x <= screen_x and (enemy_y * screen_y) // 100 <= userbullets[i].y <= (
                    enemy_y * screen_y) // 100 + car_y:
                userbullets.pop(i)
                continue
            if userbullets[i].x >= screen_x:
                userbullets.pop(i)
            i += 1
        i = 0
        while (i < len(enemybullets)):
            enemybullets[i].x -= 20
            if user.x <= enemybullets[i].x <= user.x + car_x and user.y <= enemybullets[i].y <= user.y + car_y:
                user.health -= 10
                enemybullets.pop(i)
                continue
            if enemybullets[i].x <= 0:
                enemybullets.pop(i)
                continue
            i += 1
        update()
        clock.tick(30)
def main():
    while (1):
        screen.blit(backgroundimage, (0, 0))
        screen.blit(textplay, ((screen_x // 2) - textplay.get_width() // 2, screen_y // 4))
        screen.blit(textexit, ((screen_x // 2) - textexit.get_width() // 2, 3 * screen_y // 4))
        pygame.display.update()
        i = pygame.event.wait()
        if i.type == pygame.QUIT:
            pygame.quit()
            quit()
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_y <= screen_y // 2:
                    start()
                else:
                    pygame.quit()
                    quit()
main()