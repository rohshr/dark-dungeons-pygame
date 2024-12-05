import pygame, sys
import pygame.freetype
import pytmx
from settings import *
from sprite import *
from player import *
from level import *
from debug import debug
from ui import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dungeon Escape')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.ui = UI()
        self.current_screen = 'start_screen'
        self.start_time = pygame.time.get_ticks()
    
    def run(self):
        while True:
            if self.current_screen == 'start_screen':
                self.ui.show_start_screen()
                start_button = self.ui.start_button
                help_button = self.ui.help_button
                start_button.draw(self.screen)
                help_button.draw(self.screen)
                
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if start_button.handle_event(event):
                        self.current_screen = 'game'
                    if help_button.handle_event(event):
                        self.current_screen = 'instructions'                   
                        
            elif self.current_screen == 'instructions':
                self.ui.show_instructions_screen()
                back_button = self.ui.back_button
                back_button.draw(self.screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if back_button.handle_event(event):
                        self.current_screen = 'start_screen'
            
            elif self.current_screen == 'paused':
                self.ui.show_pause_menu()
                resume_button = self.ui.resume_button
                resume_button.draw(self.screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if resume_button.handle_event(event):
                        self.current_screen = 'game'
            
            elif self.current_screen == 'death':
                self.ui.show_death_screen()
                retry_button = self.ui.retry_button
                retry_button.draw(self.screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if retry_button.handle_event(event):
                        self.current_screen = 'game'
                        self.level = Level()
                        
            elif self.current_screen == 'end':
                self.ui.show_end_screen()
                restart_button = self.ui.retry_button
                restart_button.draw(self.screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if restart_button.handle_event(event):
                        self.current_screen = 'game'
                        self.level = Level()
                        
            elif self.current_screen == 'game':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current_screen = 'paused'
                    
                    if self.level.player.health <= 0:
                        print('death')
                        self.current_screen = 'death'
                    
                    if self.level.door_open and self.level.player.check_exit():
                        self.current_screen = 'end'
                
                self.screen.fill('black')
                self.level.run()
                # debug('Test')
                pygame.display.update()
                self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()