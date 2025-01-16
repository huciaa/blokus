# Example file showing a circle moving on screen
import pygame
from field import Field, BlockType, Block
from board import Board


# pygame setup
pygame.init()

screen_width = 600  
screen_height = 700
cell_size = 30 
number_of_cells_in_line = 20
current_block_to_display = 0
rectangle_draging = False

last_block_x = 0
last_block_y = 0

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

board = Board()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block_to_display -= 1
                if current_block_to_display < 0:
                    current_block_to_display = len(blocks) - 1
                print(current_block_to_display)
                

            if event.key == pygame.K_RIGHT:
                current_block_to_display += 1
                if current_block_to_display >= len(blocks):
                    current_block_to_display = 0
                print(current_block_to_display)
    

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()


        mouse_pos = pygame.mouse.get_pos()
        for x in range(number_of_cells_in_line):
            for y in range(number_of_cells_in_line):
                field = Field(x * cell_size, y * cell_size, cell_size, cell_size)
                if field.border.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, "red", field.border)
                else:
                    pygame.draw.rect(screen, "black", field.border)
                pygame.draw.rect(screen, "white", field.inner)

        # draw two arrows (left and right) on the bottom of the screen

        blocks = [block for block in BlockType]


        block = Block(blocks[current_block_to_display], cell_size)
        block_rects = block.get_rect()

        for rect in block_rects:
            rect.x = 250 + rect.x
            rect.y = 650 + rect.y
            pygame.draw.rect(screen, "blue", rect)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(mouse_pos):
                    print("clicked")
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos

                    

                    offset_x = rect.x - mouse_x
                    offset_y = rect.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:


                board.add_block(block, last_block_x, last_block_y)
                
                for block_on_board in board.blocks:
                    block_rects = block_on_board.block.get_rect()
                    for rect in block_rects:
                        rect.x = block_on_board.x + rect.x
                        rect.y = block_on_board.y + rect.y
                        pygame.draw.rect(screen, "blue", rect)

                if event.button == 1:            
                    rectangle_draging = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    rect.x = mouse_x + offset_x
                    rect.y = mouse_y + offset_y

                    last_block_x = rect.x
                    last_block_y = rect.y

                    pygame.draw.rect(screen, "blue", rect)




        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()
