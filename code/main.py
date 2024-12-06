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
        
        # Sound setup
        self.main_menu_music = pygame.mixer.Sound(MAIN_MENU_MUSIC)
        self.main_menu_music.set_volume(0.5)
        self.main_menu_music.play(loops=-1)
        self.in_game_music_played = False
        self.in_game_music = pygame.mixer.Sound(IN_GAME_MUSIC)
    
    def handle_quit_event(self, event):
        """Handle quit events."""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def handle_screen_events(self, buttons):
        """Handle events for the current screen."""
        for event in pygame.event.get():
            self.handle_quit_event(event)
            for button_name, button_action in buttons.items():
                button = getattr(self.ui, button_name)
                if button.handle_event(event):
                    button_action()

    def show_screen(self, screen_method, buttons):
        """Display a screen with specified UI elements."""
        screen_method()
        for button_name in buttons.keys():
            button = getattr(self.ui, button_name)
            button.draw(self.screen)
        pygame.display.update()
        self.handle_screen_events(buttons)

    def run_start_screen(self):
        """Display the start screen."""
        self.show_screen(
            self.ui.show_start_screen,
            {
                'start_button': lambda: self.set_screen('game'),
                'help_button': lambda: self.set_screen('instructions')
            }
        )

    def run_instructions_screen(self):
        """Display the instructions screen."""
        self.show_screen(
            self.ui.show_instructions_screen,
            {'back_button': lambda: self.set_screen('start_screen')}
        )

    def run_pause_screen(self):
        """Display the pause menu."""
        self.show_screen(
            self.ui.show_pause_menu,
            {'resume_button': lambda: self.set_screen('game')}
        )

    def run_death_screen(self):
        """Display the death screen."""
        self.show_screen(
            self.ui.show_death_screen,
            {'retry_button': self.reset_game}
        )

    def run_end_screen(self):
        """Display the end screen."""
        self.show_screen(
            self.ui.show_end_screen,
            {'retry_button': self.reset_game}
        )

    def run_game(self):
        """Run the main game loop."""
        if not self.in_game_music_played:
            self.main_menu_music.stop()  # Stop menu music
            self.in_game_music.play(loops=-1)  # Play main game music
            self.in_game_music_played = True
        
        for event in pygame.event.get():
            self.handle_quit_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.set_screen('paused')

        # Check game conditions
        if self.level.player.health <= 0:
            self.set_screen('death')
            self.level.player_death_sound.play()

        if self.level.door_open and self.level.player.check_exit():
            self.set_screen('end')

        # Render game
        self.screen.fill('black')
        self.level.run()
        pygame.display.update()
        self.clock.tick(FPS)

    def reset_game(self):
        """Reset the game level."""
        self.set_screen('game')
        self.level = Level()

    def set_screen(self, screen_name):
        """Set the current screen."""
        self.current_screen = screen_name

    def run(self):
        """Main game loop."""
        while True:
            if self.current_screen == 'start_screen':
                self.run_start_screen()
            elif self.current_screen == 'instructions':
                self.run_instructions_screen()
            elif self.current_screen == 'paused':
                self.run_pause_screen()
            elif self.current_screen == 'death':
                self.run_death_screen()
            elif self.current_screen == 'end':
                self.run_end_screen()
            elif self.current_screen == 'game':
                self.run_game()

if __name__ == '__main__':
    game = Game()
    game.run()
