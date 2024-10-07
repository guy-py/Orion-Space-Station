import pygame
import math
import os
import random

#
if True:
    #set vars
    if True:
        class empty_class():
            def __init__(self):
                pass

        def empty_func(*args, **kwargs):
            pass
        pygame.init()
        vector=pygame.Vector2
        font = pygame.font.Font('freesansbold.ttf', 30)
        default_values={
            'pos':vector(0, 0),
            'rot':0,
            'size':(100, 100),
            'color':'white',
            'image':None,
            'update_func':empty_func,
            'after_physics':empty_func,
            'start_func':empty_func,
            'redraw':empty_func,
            'fol_cam':True,
            'show':True,
            'children':[]
        }
        
        purple=pygame.Surface((100, 100))
        purple.set_colorkey('purple')
        
        allimages={
            '':pygame.Surface((100, 100), pygame.SRCALPHA),
            'purple':purple
        }

    def assign(s, i, n):
        l=list(s)
        l[i]=str(n)
        return ''.join(l)

    def infdiv(x, y):
        if y=='inf':
            return 0
        if y==0:
            return 'inf'
        return x/y

    def infmul(x, y):
        if 'inf' in [x, y]:
            return 'inf'
        return x*y

    def infmin(x, y):
        if x=='inf':
            return y
        if y=='inf':
            return x
        return min(x, y)

    def infdistance(p1, p2=[0, 0]):
        if 'inf' in p1:
            return 'inf'
        return distance(p1, p2)

    def correct_collision(t1, t2, bias, r1=None, r2=None):
        if t1.fol_cam==t2.fol_cam:
            if r1==None: r1=t1.rect
            if r2==None: r2=t2.rect
            r1=r1.inflate(-1, -1)
            r2=r2.inflate(-1, -1)
            crect=r1.clip(r2)

            change=vector(0, 0)

            if crect.w>=crect.h:
                nega=-1
                if t1.pos[1]>t2.pos[1]:
                    nega=1
                change=vector(change.x, crect.h*nega)
                
            if crect.w<=crect.h:
                nega=-1
                if t1.pos[0]>t2.pos[0]:
                    nega=1
                change=vector(crect.w*nega, change.y)
            
            if ',' in bias:
                b1, b2=bias.split(',')
            else:
                b1, b2=bias, 1-float(bias)

            t1.pos+=change*float(b1)
            t2.pos-=change*float(b2)
            t1.update_rect()
            t2.update_rect()

        #if clipped:
        #    start, end = vector(clipped[0]), vector(clipped[1])
        #    t1.pos+=(end-start)

    def distance(p1, p2=[0, 0]):
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

    def normalize(vec):
        if vec==vector(0, 0):
            return vec
        return vec* (1/distance(vec))

    def multiply(v1, v2):
        try:
            return vector(v1[0]*v2[0], v1[1]*v2[1])
        except TypeError:
            return vector(v1[0]*v2, v1[1]*v2)
    
    def divide(v1, v2):
        try:
            return vector(v1[0]/v2[0], v1[1]/v2[1])
        except TypeError:
            return vector(v1[0]/v2, v1[1]/v2)
    
    def add(a, b):
        try:
            return vector(a[0]+b[0], a[1]+b[1])
        except TypeError:
            return vector(a[0]+b, a[1]+b)
    
    def minus(a, b):
        return add(a, multiply(b, -1))

    def angle(a, b):
            c=add(a, (0, 1))
            ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
            return ang + 360 if ang < 0 else ang

    def interpolate(a, b, n):
        if type(a)==int or type(a)==float:
            return a+(n*(b-1))
        return add(a, multiply(minus(b, a), n))

    def apply(v, f):
        return vector(f(v[0]), f(v[1]))

    def load_image(name, title=None, colorkey=None):
            image = pygame.image.load(name).convert_alpha()
            if colorkey is not None:
                image.set_colorkey(colorkey)
            allimages[[name.split('.')[0], title][bool(title)]] = image

#

    class thing(pygame.sprite.Sprite):
        def __init__(self, pos=None, rot=None, size=None, color=None, image=None, update_func=None, after_physics=None, start_func=None, redraw=None, fol_cam=None, show=None, children=None, tag='', custom={}):
            pygame.sprite.Sprite.__init__(self)

            self.pos=pos
            self.rot=rot
            self.size=size
            self.color=color
            self.image=image
            self.update_func=update_func=update_func
            self.after_physics=after_physics
            self.start_func=start_func
            self.redraw=redraw
            self.fol_cam=fol_cam
            self.show=show
            self.tag=tag
            self.children=children
            self.custom=custom

        def change_image(self, change):
            if change:
                self.image = pygame.transform.scale(allimages[change], (self.size)).convert_alpha()
            else:
                self.image=pygame.Surface(self.size, pygame.SRCALPHA)

        def initialize(self, game):

            for attr, name in [(self.pos, 'pos'), (self.rot, 'rot'), (self.size, 'size'), (self.color, 'color'), (self.image, 'image'), (self.update_func, 'update_func'), (self.after_physics, 'after_physics'), (self.start_func, 'start_func'), (self.redraw, 'redraw'), (self.fol_cam, 'fol_cam'), (self.show, 'show'),(self.children, 'children')]:
                if attr==None:
                    if name in game.tag_settings.get(self.tag, {}):
                        setattr(self, name, game.tag_settings[self.tag][name])
                    elif name in game.tag_settings.get('everything', {}):
                        setattr(self, name, game.tag_settings['everything'][name])
                    else:
                        setattr(self, name, default_values[name])
                    
            self.vel=vector(0, 0)
            self.alpha=255
            self.ticks=0

            children=self.children
            self.children=[]
            self.add_children(game, children)
            self.parent=None
            
            self.change_image(self.image)
            self.rect = self.image.get_rect()
            self.rect.center=self.pos

        def get_parent_pos(self):
            if self.parent:
                parent_pos=self.parent.pos
            else:
                parent_pos=vector(0, 0)
            return parent_pos

        def update_rect(self):
            try:
                self.rect = self.image.get_rect()
                self.rect.update([self.pos, game.world_to_screen(self.pos)][self.fol_cam] + self.get_parent_pos(), (self.size))
            except TypeError:
                raise TypeError

        def update(self, game, inputs, dt):

            self.update_func(game, self, inputs, dt)
            
            #collision
            self.check_collision(game, game.collision_tiers.get(self.tag, []))
            self.after_physics(game, self, inputs, dt)

            #update rect position
            self.update_rect()
            
            self.ticks+=1

        def check_collision(self, game, group, r1=None, r2=None):
            #check thing's collision from a list of tag|bias
            ret=[]

            for scared in group:
                affectedby, bias=scared.split('|')

                colls=pygame.sprite.spritecollide(self, game.tags[affectedby], False)
                self.rect.inflate_ip(10, 10)
                colls2=pygame.sprite.spritecollide(self, game.tags[affectedby], False)
                self.rect.inflate_ip(-10, -10)

                if colls:
                    for i, coll in enumerate(colls):
                        if not coll==self:
                            correct_collision(self, coll, bias, r1=r1, r2=r2)
                            ret.append(colls2[i])

                
            
            return ret
        
        def draw(self, game, screen, dontcare=False, offset=[0, 0], th=0, onset=None):
            if self.redraw==empty_func or dontcare:
                position=[self.pos, game.world_to_screen(self.pos)][self.fol_cam]
                screen.blit(pygame.transform.rotate(self.image, self.rot), add(add(position, offset), self.get_parent_pos()))
            else:
                self.redraw(self, game, screen)

        def render(self, image=None, rot=None, offset=[0, 0], alpha=255):
            if image==None:
                image=self.image
            if rot==None:
                rot=self.rot

            position=[self.pos, game.world_to_screen(self.pos)][self.fol_cam]
            texture=pygame.transform.scale(pygame.transform.rotate(image, rot), self.size)
            texture.set_alpha(alpha)
            game.screen.blit(texture, add(position, offset))

        def start(self, game):
            self.initialize(game)

            for i in self.custom:
                setattr(self, i, self.custom[i])

            self.start_func(game, self)
        
        def add_child(self, game, thing):
            self.children.append(thing)
            game.things.append(thing)

            if thing.tag in game.tags:
                game.tags[thing.tag].add(thing)
            else:
                game.tags[thing.tag] = pygame.sprite.Group(thing)
            game.tags['everything'].add(thing)

            thing.start(game)
            thing.fol_cam=self.fol_cam
            thing.parent=self

        def add_children(self, game, things):
            for thing in things:
                self.add_child(game, thing)

        def set_alpha(self, alpha):
            self.alpha=alpha
            self.image.set_alpha(alpha)
            for child in self.children:
                child.image.set_alpha(alpha)

        def mouse_in(self, inputs):
            return self.rect.collidepoint(pygame.mouse.get_pos())

        def clicked(self, inputs):
            return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed(3)[0]
        
        def delete(self, game):
            del game.things[game.things.index(self)]
            for child in self.children:
                child.kill()
            self.kill()

#

    class Game:

        def __init__(self, size, start=empty_func, update_func=empty_func):
            self.screen = pygame.display.set_mode(size, flags=pygame.SCALED)
            self.clock = pygame.time.Clock()
            self.ticks=0
            self.running = False
            self.cam_pos=vector(0, 0)
            self.cam_sup_pos=vector(0, 0)
            self.cam_rot=0
            self.things=[]
            self.tags={'everything':pygame.sprite.Group()}
            self.vars=empty_class()
            self.update_func=update_func

            start(self)
        
        def world_to_screen(self, pos):
            npos=pos-self.cam_pos
            return npos
        
        def screen_to_world(self, pos):
            npos=self.cam_pos+pos
            return npos
        
        def add_thing(self, thing):
            self.things.append(thing)
            if thing.tag in self.tags:
                self.tags[thing.tag].add(thing)
            else:
                self.tags[thing.tag] = pygame.sprite.Group(thing)
            self.tags['everything'].add(thing)

            if self.running:
                thing.start(self)
        
        def update(self, inputs, dt):

            self.update_func(self, inputs, dt)
            for thing in self.things:
                thing.update(self, inputs, dt)

        def draw(self, screen):
            screen.fill("black")

            for thing in self.things:
                if thing.show:
                    thing.draw(game, screen)

            pygame.display.flip()
        
        def run(self):
            for thing in self.things:
                thing.start(self)

            self.running=True
            while self.running:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                inputs=[pygame.mouse.get_pos(), pygame.key.get_pressed()]

                #cam smoothie

                self.cam_pos=interpolate(self.cam_pos, self.cam_sup_pos, 0.05)

                self.clock.tick()
                self.ticks+=1
                dt=self.ticks

                self.update(inputs, dt)
                self.draw(self.screen)

#

if __name__ == "__main__":


    #wall
    if True:
        def start_wall(game, wall):
            pass

        def wall(game, wall, inputs, dt):
            
            def sub_func(tile, game, trux, truy, stamp_pos):
                collide = game.tile_map[truy][trux] in ['#']
                    
                if collide:
                    offset=game.screen_to_world(stamp_pos)
                    #check and collide with things
                    #move to position

                    wall.pos+=offset
                    wall.update_rect()

                    wall.check_collision(game, group=['everything|0'])

                    wall.pos-=offset
                    wall.update_rect()
                
            gridding_system(wall, game, sub_func)

    #astronaut
    if True:      
        def start_astronaut(game, astro):
            astro.max_speed=5
            astro.acc=0.5
            astro.in_prox=False

        def astronaut(game, astro, inputs, dt):
            can_move=not len(game.tags.get('task', []))>0

            #movement
            if can_move:

                controls=vector((int(inputs[1][pygame.K_d]) - int(inputs[1][pygame.K_a])), (int(inputs[1][pygame.K_s]) - int(inputs[1][pygame.K_w])))

                astro.vel+=normalize(multiply(vector(astro.acc, astro.acc), normalize(controls)))

                #limit/control movement

                astro.vel*=0.9

                if controls==vector(0, 0):

                    if abs(astro.vel.x)<1:
                        astro.vel.x=0
                    if abs(astro.vel.y)<1:
                        astro.vel.y=0
                
                if not -astro.max_speed<astro.vel.x<astro.max_speed:
                    astro.vel.x=astro.max_speed * (astro.vel.x/abs(astro.vel.x))

                if not -astro.max_speed<astro.vel.y<astro.max_speed:
                    astro.vel.y=astro.max_speed * (astro.vel.y/abs(astro.vel.y))

                astro.pos+=astro.vel
                prev=astro.pos-astro.vel

                game.cam_sup_pos=add(minus(astro.pos, multiply(game.screen.get_size(), 0.5)), multiply(astro.rect.size, 0.5))

            #prox
            #if (not astro.in_prox==False) and inputs[1][pygame.K_e] and can_move:
            #    start_task(game, astro.in_prox)
            #    astro.in_prox=False

        def after_astronaut(game, astro, inputs, dt):
            pass

    #tile
    if True:

        def tile_draw(tile, game, screen):
            def sub_func(tile, game, trux, truy, stamp_pos):
                stamp=game.tile_map[truy][trux]
                image_name = tile.tile_types.get(stamp, '')

                if image_name=='top':
                    ns=[[truy-1, trux], [truy, trux+1], [truy+1, trux], [truy, trux-1]]
                    nbs=''
                    for i, e in enumerate(ns):
                        try:
                            addition=str(int(game.tile_map[e[0]][e[1]]=='#'))
                        except IndexError:
                            addition='0'
                        
                        nbs+=addition
                
                    if nbs=='1100':
                        image_name='top_ur'
                    elif nbs=='1010':
                        image_name='top_ud'
                    elif nbs=='1001':
                        image_name='top_ul'
                    elif nbs=='0110':
                        image_name='top_dr'
                    elif nbs=='0101':
                        image_name='top_lr'
                    elif nbs=='0011':
                        image_name='top_dl'
                    else:
                        image_name='top_lr'
                    
                    

                tile_image = pygame.transform.scale((allimages[image_name]), (tile.rect.size))

                screen.blit(pygame.transform.rotate(tile_image, tile.rot), stamp_pos)

            gridding_system(tile, game, sub_func)
            
            #draw the stars
            '''def sub_func2(tile, game, trux, truy, stamp_pos):
                texture=allimages[f'_stars{random.randint(1, 2)}']
                tile.render(image=texture, offset=stamp_pos)
            
            gridding_system_nofol(tile, game, sub_func2)'''

        def tile(game, tile, inputs, dt):
            tile.pos=apply(game.cam_pos/tile.size[0], math.floor)*tile.size[0]

        def start_tile(game, tile):
            tile.tile_types=game.tile_set

            #place the nessecary things on grid

            def sub_func(tile, game, trux, truy, stamp_pos):
                stamp=game.tile_map[truy][trux]
                

                def add_tile(tag, custom={}):
                    game.add_thing(thing(game.screen_to_world(stamp_pos), 0, image='', tag=tag, custom=custom))
                
                if stamp in '#':
                    add_tile('wall')
                elif stamp=='S':
                    add_tile('salon', custom={'display_text':'E to cut hair', 'ui_open':'hair cutting'})
                elif stamp=='B':
                    add_tile('salon', custom={'display_text':'E to sleep', 'ui_open':'bed'})
                elif stamp=='F':
                    add_tile('salon', custom={'display_text':'E to tend', 'ui_open':'farm'})

            gridding_system_nocam(tile, game, sub_func)


    #salon
    if True:
        def salon_draw(salon, game, screen):
            can_move=not len(game.tags.get('task', []))>0
            salon.draw(game, screen, dontcare=True)

            target_player=game.tags['player'].sprites()[0]
            dis_player=distance(target_player.pos, salon.pos)
            text_surface=font.render(salon.display_text, False, 'black')
            text_surface.set_alpha(255 * (1-(dis_player/salon.appear_radius))+50)

            if dis_player<salon.appear_radius:
                salon.appear_time+=0.1

                elevation=(1/salon.appear_time) * salon.anim_inten
                screen.blit(text_surface, game.world_to_screen(salon.pos + vector(0, elevation - salon.anim_limit)))

                if pygame.key.get_pressed()[pygame.K_e] and can_move:
                    start_task(game, salon.ui_open)
            else:
                salon.appear_time=salon.anim_inten/salon.anim_limit
                
            if salon.ui_open=='farm' and game.tomato_on:
                salon.set_alpha(100)
            else:
                salon.set_alpha(0)

        def salon(game, salon, inputs, dt):
            pass

        def start_salon(game, salon):
            salon.appear_radius=150
            salon.appear_time=0
            salon.anim_inten=10
            salon.anim_limit=30
            salon.change_image('purple')
            salon.image.set_colorkey('purple')


    #ball
    if True:
        def ball_start(game, ball):
            ball.vel=vector(0, 0)
            ball.prev_pos=ball.pos

        def ball(game, ball, inputs, dt):
            
            collisions = ball.check_collision(game, group=['everything|0,0'])
            
            ball.pos+=ball.vel
            ball.vel*=0.9999

            if collisions:

                collided=collisions[0]
                if collided.tag=='player':
                    ball.vel+=normalize(ball.pos-collided.pos) + collided.vel
                else:
                    if collided.pos[0]>ball.pos[0]:
                        ball.vel[0]=-abs(ball.vel[0])
                    if collided.pos[0]<ball.pos[0]:
                        ball.vel[0]=abs(ball.vel[0])

                    if collided.pos[1]>ball.pos[1]:
                        ball.vel[1]=-abs(ball.vel[1])
                    if collided.pos[1]<ball.pos[1]:
                        ball.vel[1]=abs(ball.vel[1])

                    ball.vel=vector(0, 0)

    #task
    if True:

        def start_task(game, task_type):
            task_thing=thing((0, game.screen.get_size()[1]/2), 0, game.screen.get_size(), image='_astro', tag='task', custom={'type':task_type})
            game.add_thing(task_thing)

        def task(game, task, inputs, dt):

            #if-loops
            if task.close_timer==0:
                if task.type== 'hair cutting':
                    task.time_left-=1
                    
                    head=task.children[0]
                    if head.level<1:
                        close_task(game, message='')
                        game.stats_hp+=task.hairs
                        game.stats_sh-=50-task.hairs-task.dmg_done
                    elif task.time_left<1:
                        close_task(game, message='')
                        game.stats_hp-=task.hairs
                        game.stats_sh-=50-task.hairs-task.dmg_done

                elif task.type=='number pad':
                    if pygame.mouse.get_pressed(3)[0]:
                        position=apply(divide(minus(inputs[0], task.pos), 100), math.floor)
                
                elif task.type=='bed':
                    if task.ticks==300:
                        close_task(game)
                        game.stats_hp+=10
                        game.stats_re-=10
                
                elif task.type=='farm':
                    if game.tomato_progress==20000:
                        game.tomato_progress=1
                    
                    

            #animation
            task.pos=interpolate(task.pos, task.pos_anim, 0.1)
            task.set_alpha(255 - 255/(game.screen.get_size()[1]/2)*task.pos[1])

            #closing
            if task.close_timer==1:
                task.pos_anim=vector(0, game.screen.get_size()[1]*0.75)
            if task.close_timer>0:
                task.close_timer-=1
            if task.pos[1]>game.screen.get_size()[1]/2+5:
                task.delete(game)
            


        def task_start(game, task):
            task.show=True
            task.fol_cam=False
            task.change_image('side_wall1')
            task.pos_anim=vector(0, 0)
            task.close_timer=0
            task.final_message=''

            #spawning children
            x_button=thing((10, 10), 0, (50, 50), image='_xbutt', update_func=task_x_button, tag='task_x_button', children=[])

            if task.type=='hair cutting':
                head=thing((0, 0), 0, (600, 600), image='_head1', update_func=task_head, start_func=task_head_start, tag='task_head', children=[])
                vacuum=thing((0, -300), 0, (600, 600), image='_vacuum', update_func=task_vacuum, start_func=task_vacuum_start, tag='task_vacuum', children=[])
                task.add_children(game, [head, vacuum])
                
                task.time_left=1000
                task.hairs=0
                task.dmg_done=0

            elif task.type=='number pad':
                pass
            
            elif task.type=='bed':
                #task.change_image('_bed')
                pass
            
            elif task.type=='farm':
                pass

            task.add_child(game, x_button)
        
        def task_draw(task, game, screen):
            task.draw(game, screen, dontcare=True)
            
            if task.type == 'hair cutting':
                text_surfaces=[
                    font.render(f'Time Left: {task.time_left}', False, 'black'),
                    font.render(f'Hair Strands: {task.hairs}', False, 'black'),
                    font.render(f'Damage Done: {task.dmg_done}', False, 'black'),
                    font.render(f'Cutting Left: {task.children[0].level}', False, 'black')
                ]
                
                for i, text_surface in enumerate(text_surfaces):
                    screen.blit(text_surface, (10, i*60 + 85))
            
            elif task.type == 'bed':
                task.render(image=allimages['_stars'], alpha=(task.ticks-20)*2)
                
            elif task.type =='farm':
                
                task.render(image=allimages[f'_tomato{math.ceil(4*game.tomato_progress/20000)}'])
                if game.tomato_on:
                    task.render(image=allimages['purple'], alpha=100)
            
            display=allimages[task.final_message]
            display.set_alpha(task.image.get_alpha() * (1- (task.close_timer-25)/50))
            screen.blit(display, vector(0, 400)+task.pos)
            
        
        def task_strand_start(game, strand):
            strand.pos+=vector(-50, 100)
            strand.ori_pos=strand.pos
            strand.vel=normalize(vector(random.randint(-100, 100), random.randint(-100, -50)))*random.randint(2, 4)
        
        def task_strand(game, strand, inputs, dt):
            #strand.rot+=1
            
            strand.pos+=strand.vel
            vacuums=game.tags['task_vacuum'].sprites()
            if vacuums:
                vac=vacuums[0]
                #strand.pos=vac.head
                if distance(vac.head, strand.pos)<100:
                    strand.vel+=normalize(vac.head-strand.pos)
                    
                if distance(vac.head, strand.pos)<50:
                    strand.delete(game)
                    strand.parent.hairs+=1
                
                if strand.pos[1]<-150 or strand.pos[0]<-150 or strand.pos[0]>700:
                    strand.delete(game)
                    strand.parent.dmg_done+=1
                    game.stats_sh-=1
                    print('dmg!!', game.stats_sh)
            
        def task_head_start(game, head):
            head.anim=True
            head.level=30
            head.max_level=30

        def task_head(game, head, inputs, dt):

            vacuums=game.tags['task_vacuum'].sprites()
            if vacuums:
                if (pygame.mouse.get_pos()[1]>300 and pygame.mouse.get_pressed(3)[0]) and (not vacuums[0].selected) and vacuums[0].can_press:
                    if head.anim:
                        strand=thing(multiply(game.screen.get_size(), (0.5, 0.75)), 0, (100, 100), image=f'_strand{random.randint(1, 2)}', update_func=task_strand, start_func=task_strand_start, tag='task_strand', children=[])
                        head.parent.add_child(game, strand)

                        head.anim=False
                        head.level-=1

                        head.change_image(['_head3', '_head2', '_head1'][int(head.level/head.max_level * 3)])
            
            if not pygame.mouse.get_pressed(3)[0]:
                head.anim=True

        def task_vacuum(game, vac, inputs, dt):
            screen_size=game.screen.get_size()

            vac.head=vac.pos+multiply(screen_size, (0.5, 1))-vector(0, 50)

            if vac.selected:
                vac.pos_anim=add(add(multiply(screen_size, (-0.5, -1)), pygame.mouse.get_pos()), vector(0, -10))
                if not vac.mouse_in(inputs) and pygame.mouse.get_pressed(3)[0] and vac.can_press:
                    vac.selected=False
                    vac.can_press=False

                vac.rot=angle(vac.head, multiply(screen_size, (0.5, -0.3)))*100

            else:
                vac.pos_anim=vector(multiply(screen_size, (0, -0.75)))
                if vac.clicked(inputs) and vac.can_press:
                    vac.selected=True
                    vac.can_press=False

                vac.rot=0
            
            if not pygame.mouse.get_pressed(3)[0]:
                vac.can_press=True
            
            vac.pos=interpolate(vac.pos, vac.pos_anim, 0.4)
        
        def task_vacuum_start(game, vac):
            vac.selected=False
            vac.can_press=True
            vac.rot=0
            vac.pos_anim=vector(0, 0)
            vac.head=vector(0, 0)
                
        def task_x_button(game, button, inputs, dt):
            if button.clicked(inputs):
                close_task(game, timer_set=1)

    #functions
    if True:
        def close_task(game, message='', timer_set=50):
            if game.tags.get('task', []):
                task=game.tags.get('task', []).sprites()[0]
                task.close_timer=timer_set #how long to display win
                task.final_message=message
                
                for child in task.children:
                    child.update_func=empty_func

        def gridding_system(thing, game, inter):
            length=thing.rect.size[0]
            maximum=game.screen.get_size()[0]
            position=math.floor(game.cam_pos.x/length)

            
            start=0
            end=math.ceil(maximum/length)+1

            for x in range(end):
                for y in range(end):

                    #render?

                    trux=x+math.floor(game.cam_pos.x/length)
                    truy=y+math.floor(game.cam_pos.y/length)

                    if (trux>=0 and truy>=0) and truy < len(game.tile_map)-1:
                        if trux<len(game.tile_map[truy]):
                            game.tile_map[truy][trux]
                            inter(thing, game, trux, truy, game.world_to_screen(vector(trux, truy)*length))

        def gridding_system_nocam(thing, game, inter):
            length=thing.rect.size[0]
            maximum=600
            positionx=math.floor(game.cam_pos.x/length)
            positiony=math.floor(game.cam_pos.y/length)

            
            startx=-positionx
            starty=-positiony
            end=math.ceil(maximum/length)+1+len(game.tile_map[0])

            for x in range(len(max(game.tile_map, key=len))):
                for y in range(len(game.tile_map)):

                    #render?

                    trux=x
                    truy=y

                    if (trux>=0 and truy>=0) and truy < len(game.tile_map)-1:
                        if trux<len(game.tile_map[truy]):
                            game.tile_map[truy][trux]
                            inter(thing, game, trux, truy, game.world_to_screen(vector(trux, truy)*length))
                            
        def gridding_system_nofol(thing, game, inter):
            length=thing.rect.size[0]
            maximum=600
            positionx=0
            positiony=0

            
            startx=-positionx
            starty=-positiony
            end=math.ceil(maximum/length)+1+len(game.tile_map[0])

            for x in range(len(max(game.tile_map, key=len))):
                for y in range(len(game.tile_map)):

                    #render?

                    trux=x
                    truy=y

                    if (trux>=0 and truy>=0) and truy < len(game.tile_map)-1:
                        if trux<len(game.tile_map[truy]):
                            game.tile_map[truy][trux]
                            inter(thing, game, trux, truy, game.world_to_screen(vector(trux, truy)*length))
        
    #stats
    if True:                    
        def start_stats(stats, game):
            pass
        
        def stats(stats, game, inputs, dt):
            pass
        
        def draw_stats(stats, game, screen):
            
            stats.render(image=allimages['top_ud'])
            
            scale=stats.rect.w/32
            
            for x in range(0, int(game.stats_hp*(30/100))):
                stats.render(image=allimages['stats_pink'], offset=[int(x*scale), 0])
                
            for x in range(0, int(game.stats_re*(30/100))):
                stats.render(image=allimages['stats_blue'], offset=[int(x*scale), 0])
                
            for x in range(0, int(game.stats_sh*(30/100))):
                stats.render(image=allimages['stats_grey'], offset=[int(x*scale), 0])
                
            stats.draw(game, screen, dontcare=True)
    
    #game
    def start_game(game):

        game.tag_settings={
            'everything':{'size':[50, 50]},
            'salon':{'update_func':salon, 'start_func':start_salon, 'redraw':salon_draw},
            'task':{'update_func':task, 'start_func':task_start, 'redraw':task_draw},
            'ball':{'update_func':ball, 'start_func':ball_start},
            'wall':{'update_func':empty_func, 'start_func':start_wall},
            'stats':{'update_func':stats, 'start_func':start_stats, 'redraw':draw_stats, 'fol_cam':False}
        }

        game.collision_tiers={
            'wall':['player|0']
        }
        
        if True:
            game.stats_hp=75
            game.stats_re=10
            game.stats_sh=100
            game.tomato_progress=1
            game.tomato_on=True

        #tiles
        if True:
            with open('/'.join(__file__.split('/')[:-1]) + '/iss_map.txt') as file:
                map_read = [line.rstrip() for line in file]

            tile_size=100
            
            load_image('pixelz/x_button.jpg', title='_xbutt')
            load_image('pixelz/astronaut.jpg', title='_astro')
            load_image('pixelz/hair1.png', title='_head1')
            load_image('pixelz/hair2.png', title='_head2')
            load_image('pixelz/hair3.png', title='_head3')
            load_image('pixelz/stars.png', title='_stars')
            load_image('pixelz/vacuum.png', title='_vacuum')
            load_image('pixelz/updown.png', title='top_ud')
            load_image('pixelz/leftright.png', title='top_lr')
            load_image('pixelz/downleft.png', title='top_dl')
            load_image('pixelz/downright.png', title='top_dr')
            load_image('pixelz/upleft.png', title='top_ul')
            load_image('pixelz/upright.png', title='top_ur')
            load_image('pixelz/floor.jpg', title='_floor')
            load_image('pixelz/salon.jpg', title='_salon')
            load_image('pixelz/wall1.jpg', title='side_wall1')
            load_image('pixelz/wall2.jpg', title='side_wall2')
            load_image('pixelz/wall3.jpg', title='side_wall3')
            load_image('pixelz/wall4.jpg', title='side_wall4')
            load_image('pixelz/wall5.jpg', title='side_wall5')
            load_image('pixelz/strand1.png', title='_strand1')
            load_image('pixelz/strand2.png', title='_strand2')
            load_image('pixelz/strand3.png', title='_strand3')
            load_image('pixelz/stats_glass.png', title='stats_glass')
            load_image('pixelz/stats_pink.png', title='stats_pink')
            load_image('pixelz/stats_blue.png', title='stats_blue')
            load_image('pixelz/stats_grey.png', title='stats_grey')
            load_image('pixelz/farm1.jpg', title='_farm1')
            load_image('pixelz/farm2.jpg', title='_farm2')
            load_image('pixelz/tomato1.jpg', title='_tomato1')
            load_image('pixelz/tomato2.jpg', title='_tomato2')
            load_image('pixelz/tomato3.jpg', title='_tomato3')
            load_image('pixelz/tomato4.jpg', title='_tomato4')

            
            game.tile_set={}
            for x in map_read[:map_read.index('')]:
                rep, act=x.split(' ')
                game.tile_set[rep]=act

            game.tile_map=map_read[map_read.index('')+1:]

        game.add_thing(thing((0, 0), 0, image=None, update_func=tile, start_func=start_tile, redraw=tile_draw, tag='tile'))
        game.add_thing(thing((1600, 200), 0, image='_astro', update_func=astronaut, after_physics=after_astronaut, start_func=start_astronaut, tag='player'))
        game.add_thing(thing((10, 10), 0, (125, 125), image='stats_glass', update_func=stats, start_func=start_stats, redraw=draw_stats, tag='stats'))
        #game.add_thing(thing((0, 0), 0, image='', start_func=start_wall, tag='wall'))
        #game.add_thing(thing((0, 0), 0, image='_qrc', tag='salon'))
        #game.add_thing(thing((50, 50), 0, image='_ryan', tag='ball'))

    def update_game(game, inputs, dt):
        pygame.display.set_caption(f'{dt}   {len(game.things)}')
        if game.tomato_on:
            game.tomato_progress+=1

    game=Game((600, 600), start=start_game, update_func=update_game)
    game.run()
    pygame.quit()
