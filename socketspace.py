import pygame,player,socket,bullet
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ip="127.0.0.1"
port=5005
pygame.init()
pygame.font.init()
screen_x=700
screen_y=400
car_x=50
car_y=50
screen=pygame.display.set_mode((screen_x+100,screen_y))
backgroundimage=pygame.image.load("background.png")
backgroundimage=pygame.transform.scale(backgroundimage,(screen_x,screen_y))
car=pygame.image.load("hero.png")
car1=pygame.image.load("hero.png")#enemy.png
car=pygame.transform.scale(car,(car_x,car_y))
car.convert_alpha()
car.set_colorkey((255,255,255))
car1=pygame.transform.scale(car1,(car_x,car_y))
car1.convert_alpha()
car1.set_colorkey((255,255,255))
bulletimage=pygame.image.load("bullet1.png")
bulletimage=pygame.transform.scale(bulletimage,(20,10))
bulletimage.convert_alpha()
bulletimage.set_colorkey((17,17,17))
clock=pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textplay=myfont.render('START', False, (0, 0, 0))
textexit=myfont.render('EXIT', False, (0, 0, 0))
playingid=1
userid=1
userbullets=[]
enemybullets=[]
def update():
    screen.blit(backgroundimage, (0, 0))
    screen.blit(car,(user.x,user.y))
    s.sendto(b"%d %d %d"%(playingid,userid,(user.y*100)//screen_y),(ip,port))
    data,addr=s.recvfrom(1024)
    enemy_y=int(data.decode())
    screen.blit(car1,(screen_x-10-car_x,(enemy_y*screen_y)//100))
    for i in range(len(userbullets)):
        screen.blit(bulletimage, (userbullets[i].x, userbullets[i].y))
    pygame.display.update()
def start():
    global user
    user=player.player(10, screen_y // 2, userid)
    velocity=10
    ready=1
    s.sendto(b"1",(ip,port))
    #requests.post("http://127.0.0.1:5000/ready",data={"playingid":playingid,"ready":"1","user.id":str(user.id)}) telling its ready
    while(ready):
        # ready=int(requests.get("http://127.0.0.1:5000/ready",data={"playingid":str(playingid)}).text.strip(" "))
        # for i in pygame.event.get():
        #     if i.type==pygame.QUIT:
        #         requests.post("http://127.0.0.1:5000/ready", data={"playingid":str(playingid), "ready": "0","userid":str(user.id)})
        #         return(0)

    fire=0
    while(1):
        for i in pygame.event.get():
            if i.type==pygame.QUIT:
                return(0)
            if i.type==pygame.MOUSEBUTTONDOWN:
                if i.button==1:
                    fire=1
            if i.type==pygame.MOUSEBUTTONUP:
                if i.button==1:
                    fire=0
        mouse_x,mouse_y=pygame.mouse.get_pos()
        user.y+=(mouse_y-user.y)//velocity
        if fire==1:
            userbullets.append(bullet.bullet(user.x+car_x,user.y+car_y//2))
        i=0
        while (i<len(userbullets)):
            userbullets[i].x+=20
            if userbullets[i].x>=screen_x:
                userbullets.pop(i)
            i+=1
        update()
        clock.tick(30)

while(1):
    screen.blit(backgroundimage, (0, 0))
    screen.blit(textplay,((screen_x//2)-textplay.get_width()//2,screen_y//4))
    screen.blit(textexit,((screen_x//2)-textexit.get_width()//2, 3*screen_y//4))
    pygame.display.update()
    i =pygame.event.wait()
    if i.type==pygame.QUIT:
        pygame.quit()
        quit()
    if i.type==pygame.MOUSEBUTTONDOWN:
        if i.button==1:
            mouse_x, mouse_y=pygame.mouse.get_pos()
            if mouse_y<=screen_y//2:
                start()
            else:
                pygame.quit()
                quit()