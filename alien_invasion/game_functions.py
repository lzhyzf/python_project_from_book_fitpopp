import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import random

def check_keydown(event, ai_settings, screen, stats, ship, aliens, bullets, sb):
    '''发生按下键盘事件可能需要做的改变'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats, ship, aliens, bullets, sb)
        
def check_keyup(event, ship):
    '''发生松开键盘事件可能需要做的改变'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, stats, ship, aliens, bullets, sb)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb):
    '''在玩家单击Play按钮且游戏处于静止时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
       start_game(ai_settings, screen, stats, ship, aliens, bullets, sb)

def start_game(ai_settings, screen, stats, ship, aliens, bullets, sb):
    '''点击开始游戏或按p键可开始新游戏'''
    #重置游戏设置
    ai_settings.initialize_dynamic_settings()
    
    #隐藏光标
    pygame.mouse.set_visible(False)
        
    #重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    
    #重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
        
    #清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
        
    #创建一群新的外星人并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb):
    '''更新屏幕上的图像，并且换到新屏幕'''
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    #在外星人和飞船后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    
    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, ship, aliens, bullets, sb):
    '''更新所有子弹,并删除已经消失的子弹'''
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets, sb)

def check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets, sb):
    '''响应子弹和外星人的碰撞'''
    #如果碰撞，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        #删除现有子弹,加快游戏速度
        bullets.empty()
        ai_settings.increase_speed()
        
        #提高等级
        stats.level += 1
        sb.prep_level()
        
        #新建一批敌人
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    '''如果子弹还没达到上限，就发射一颗子弹'''
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    '''计算每行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / 3 / alien_width)
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算每列可容纳多少个外星人'''
    available_space_y = ai_settings.screen_height - 7 * alien_height - ship_height
    number_rows = int(available_space_y / 2 / alien_height)
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''创建一个外星人并将其放在当前行,列中'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 3 * alien_number * alien_width
    alien.y = alien_height + 2 * row_number * alien_height
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算一行,一列可容纳多少外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    #创建外星人群
    for alien_number in range(number_aliens_x):
        for number_row in range(number_rows):
            if random.randint(0,1):
                create_alien(ai_settings, screen, aliens, alien_number, number_row)

def change_fleet_direction(ai_settings, aliens):
    '''将整群外星人下移，并改变它们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def check_fleet_edges(ai_settings, aliens):
    '''有外星人到达边缘时采取相应措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        #将ships_left减1
        stats.ships_left -= 1
        #更新飞船生命
        sb.prep_ships()    
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        #暂停
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''检查是否有外星人位于屏幕边缘，并更新整群外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
        
    #检测是否有外星人达到屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)
        
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    '''检测是否有外星人到达了屏幕底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def check_high_score(stats, sb):
    '''检查是否诞生了新的最高得分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
