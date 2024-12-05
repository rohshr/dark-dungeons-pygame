import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (20, 20, 20)  # Dark background
BUTTON_COLOR = (50, 50, 50)  # Dark gray
HOVER_COLOR = (100, 100, 100)  # Light gray for hover effect
BORDER_COLOR = (150, 75, 0)  # Brownish for a dungeon feel
TEXT_COLOR = (200, 200, 200)  # Light gray text

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Crawler Button Example")

# Pixel Art Font (Optional, replace `None` if you have a pixel-art font file)
font = pygame.font.Font(None, 36)  # Use `pygame.font.Font('pixel_font.ttf', size)` for custom fonts

class DungeonButton:
    def __init__(self, x, y, width, height, text, font, color, hover_color, border_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.text_color = text_color
        self.is_hovered = False

        # Render the text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        # Change color if hovered
        button_color = self.hover_color if self.is_hovered else self.color

        # Draw button border
        pygame.draw.rect(screen, self.border_color, self.rect)

        # Draw inner button
        inner_rect = self.rect.inflate(-4, -4)  # Create a smaller inner rectangle for the button face
        pygame.draw.rect(screen, button_color, inner_rect)

        # Draw text
        screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        """Handle events like mouse hover and clicks."""
        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is over the button
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:  # Left mouse button
                return True  # Button clicked
        return False

# Create a button
button = DungeonButton(
    x=WIDTH // 2 - 100,
    y=HEIGHT // 2 - 25,
    width=200,
    height=50,
    text="START GAME",
    font=font,
    color=BUTTON_COLOR,
    hover_color=HOVER_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR
)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if button.handle_event(event):
            print("Button Clicked!")

    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw the button
    button.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
