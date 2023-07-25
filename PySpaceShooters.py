import pygame
pygame.font.init()
pygame.mixer.init()

height,width=500,500
window=pygame.display.set_mode((width,height))
pygame.display.set_caption="Hello World"
bg_color=(25,55,255)
black=(0,0,0)
spaceshiph,spaceshipw=100,75
bulleth,bulletw=50,25
dy,dx,bullet_dx=2,1,5
ship1_health=ship2_health=10

health_font=pygame.font.SysFont('comicsans',20)
winner_font=pygame.font.SysFont('comicsans',40)

bullet_hit_sound=pygame.mixer.Sound("Assets/hit.mp3")
bullet_fire_sound=pygame.mixer.Sound("Assets/fire.mp3")
win_sound=pygame.mixer.Sound("Assets/win.mp3")

ship1_hit=pygame.USEREVENT + 1
ship2_hit=pygame.USEREVENT + 2

def load_assets():
    global spaceship1,spaceship2
    spaceship1=pygame.transform.rotate(pygame.transform.scale(
        pygame.image.load('Assets/spaceship1-removebg-preview.png'),(spaceshiph,spaceshipw)),-90)
    spaceship2=pygame.transform.rotate(pygame.transform.scale(
        pygame.image.load('Assets/spaceship2-removebg-preview.png'),(spaceshiph,spaceshipw)),90)

def update():
    pygame.display.update()

def draw_game():
    global ship1_health,ship2_health
    window.fill(bg_color)
    pygame.draw.rect(window, black, pygame.Rect(width/2-5,0,10,height))
    for bullet in ship1_bullet:
        bulletship1=pygame.transform.rotate(pygame.transform.scale(
        pygame.image.load('Assets/bullet-removebg-preview.png'),(bulleth,bulletw)),-90)
        window.blit(bulletship1,(bullet.x,bullet.y))
    
    for bullet in ship2_bullet:
        bulletship2=pygame.transform.rotate(pygame.transform.scale(
        pygame.image.load('Assets/bullet-removebg-preview.png'),(bulleth,bulletw)),90)
        window.blit(bulletship2,(bullet.x,bullet.y))
        
    window.blit(spaceship1,(ship1.x,ship1.y))
    window.blit(spaceship2,(ship2.x,ship2.y))
    
    ship1text=health_font.render("Health: "+str(ship1_health),1,(255,255,255))
    ship2text=health_font.render("Health: "+str(ship2_health),1,(255,255,255))
    window.blit(ship1text,(10,10))
    window.blit(ship2text,(490-ship2text.get_width(),10))
    update()

def ship1_handle_movement(keyspress):
    if(keyspress[pygame.K_w]):
        if(ship1.y==0):
            pass
        else:
            ship1.y-=dy
    if(keyspress[pygame.K_s]):
        if(ship1.y==500-spaceshiph):
            pass
        else:
            ship1.y+=dy
    if(keyspress[pygame.K_a]):
        if(ship1.x==0):
            pass
        else:
            ship1.x-=dx
    if(keyspress[pygame.K_d]):
        if(ship1.x==250-spaceshipw):
            pass
        else:
            ship1.x+=dx

def ship2_handle_movement(keyspress):
    if(keyspress[pygame.K_UP]):
        if(ship2.y==0):
            pass
        else:
            ship2.y-=dy
    if(keyspress[pygame.K_DOWN]):
        if(ship2.y==500-spaceshiph):
            pass
        else:
            ship2.y+=dy
    if(keyspress[pygame.K_LEFT]):
        if(ship2.x==250):
            pass
        else:
            ship2.x-=dx
    if(keyspress[pygame.K_RIGHT]):
        if(ship2.x==500-spaceshipw):
            pass
        else:
            ship2.x+=dx

def bullet_handler():
    for bullet in ship1_bullet:
        bullet.x+=bullet_dx
        if ship2.colliderect(bullet):
            ship1_bullet.remove(bullet)
            bullet_hit_sound.play()
            pygame.event.post(pygame.event.Event(ship2_hit))
        elif bullet.x==500:
            ship1_bullet.remove(bullet)
            
    for bullet in ship2_bullet:
        bullet.x-=bullet_dx
        if ship1.colliderect(bullet):
            ship2_bullet.remove(bullet)
            bullet_hit_sound.play()
            pygame.event.post(pygame.event.Event(ship1_hit))
        elif bullet.x==0:
            ship2_bullet.remove(bullet)
            
def display_winner(winner_txt):
    print("hello")
    global height,width
    winner=winner_font.render(winner_txt,1,(255,255,255))
    window.blit(winner,(width//2-winner.get_width()//2,height//2-winner.get_height()//2))
    update()
    win_sound.play()
    pygame.time.delay(5000)
run=True

def main():
    global ship1_bullet,ship2_bullet,ship1,ship2,ship1_health,ship2_health,run
    ship1_bullet,ship2_bullet=[],[]
    ship1_health,ship2_health=10,10
    load_assets()
    ship1=pygame.Rect(50,100,spaceshiph,spaceshipw)
    ship2=pygame.Rect(400,100,spaceshiph,spaceshipw)
    
    clk=pygame.time.Clock()

    while run:
        clk.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(ship1_bullet)<3:
                    bullet=pygame.Rect(ship1.x + spaceshiph - 30,ship1.y+spaceshipw//2-9,bulleth,bulletw)
                    ship1_bullet.append(bullet)
                    bullet_fire_sound.play()
                if event.key==pygame.K_RCTRL and len(ship2_bullet)<3:
                    bullet=pygame.Rect(ship2.x,ship2.y+spaceshipw//2-9,bulleth,bulletw)
                    ship2_bullet.append(bullet)
                    bullet_fire_sound.play()
            if event.type==ship1_hit:
                ship1_health-=1
                
            if event.type==ship2_hit:
                ship2_health-=1   
                    
        if (run==False):
            break    
        if ship1_health<=0:
            winner="Ship2 wins!"
            display_winner(winner)
            break
        if ship2_health<=0:
            winner="Ship1 wins!"
            display_winner(winner)
            break
                
        keyspress=pygame.key.get_pressed()
        bullet_handler()
        ship1_handle_movement(keyspress)
        ship2_handle_movement(keyspress)
        draw_game()
    if run:
        main()

if __name__=="__main__":
    main()
