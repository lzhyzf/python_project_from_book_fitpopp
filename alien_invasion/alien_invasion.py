import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    #初始化pygame,设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    
    #创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    #创建一艘飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    #创建一个用于外星人的编组
    aliens = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    #创建一个用于存储游戏统计信息的实例并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb)#检测鼠标键盘事件
        if stats.game_active == True:
            ship.update()#更新飞船位置
            gf.update_bullets(ai_settings, screen, stats, ship, aliens, bullets, sb)#更新子弹
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)#更新外星人
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb)#打印飞船,外星人,子弹
        
run_game()
