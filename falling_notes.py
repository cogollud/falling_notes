import pygame
import sys
import midi_parser


# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Clock for managing the frame rate
clock = pygame.time.Clock()


class FallingNote:
    def __init__(self, x, note):
        self.width = 40
        self.x = SCREEN_WIDTH // 2
        self.y = 0  # Start at the top of the screen
        self.time = note.time  # Time in seconds when the note should be hit        
        self.midi_note = note.midi_note  # MIDI note that will play when the note reaches the bottom
        self.duration = note.duration  # Duration of the note in seconds
        self.color = RED if note.strong else BLUE
        
    def update(self, speed):
        self.y += speed

    def draw(self):        
        # Draw a rectangle to represent the duration
        rect_height = int(self.duration * 100)  # Scale the duration for visibility        
        pygame.draw.rect(screen, self.color, (self.x - self.width, self.y - rect_height, self.width, rect_height))


# Main game function
def main_game(midi_file, fallingNotes):
            
    already_playing = False
    play_is_over = False    
    pygame.mixer.music.load(midi_file)

    falling_speed = 5  # Speed of falling notes
    start_ticks = pygame.time.get_ticks()  # Track the start time

    finish_line_y = SCREEN_HEIGHT - 100  # Position of the finish line

    while not play_is_over:
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (0, finish_line_y), (SCREEN_WIDTH, finish_line_y), 5)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the current time in seconds
        current_time = (pygame.time.get_ticks() - start_ticks) / 1000.0

        # Update and draw notes
        for fallingNote in fallingNotes:
            # Check if the note should be falling based on current time
            if fallingNote.time <= current_time and (fallingNote.y - (fallingNote.duration * 100)) < finish_line_y:
                fallingNote.update(falling_speed)
                fallingNote.draw()
                

            if not already_playing:
                # Play sound when first note reaches the finish line
                if fallingNote.y >= finish_line_y - (fallingNote.duration * 100): # last number stands for some delay due to the play call
                    # Play the MIDI music only once when the first note hits the bottom                
                    pygame.mixer.music.play()
                    already_playing = True
                
        
        # Check if the music has finished playing
        if already_playing and not pygame.mixer.music.get_busy():
            play_is_over = True  # Exit the loop when music is finished

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(50)

    # Exit gracefully after the loop ends
    pygame.quit()
    sys.exit()

if __name__ == "__main__":    
    # Load the MIDI file into the Song object
    midi_file = "simple.mid"
    song = midi_parser.Song(midi_file)
    print(song) # Print the song information

    # build fallingNotes from the notes of the first track (ignoring the rest of the tracks)
    track = song.tracks[0] 
    fallingNotes = [FallingNote(SCREEN_WIDTH // 2, note) for note in track.notes]

    main_game(midi_file, fallingNotes)
