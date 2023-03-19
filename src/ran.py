import pygame
import threading
from net_thread import Network
import time

pygame.init()
screen = pygame.display.set_mode((640, 480))

# Define a global variable to store the user count
user_count = 0
net = Network()

# Define a function that will run in a separate thread to get the user count from the server
def update_user_count():
    global user_count
    while True:
        # Send a request to the server to get the user count
        net.get_connection()
        data = net.receive_data()
        # Extract the user count from the response JSON
        if data:
            user_count = data
        print(f"Running... user count: {user_count}")
        # Wait for 1 second before sending the next request
        time.sleep(2)

# Start the thread to update the user count
user_count_thread = threading.Thread(target=update_user_count)
user_count_thread.daemon = True  # Set the thread as a daemon so that it will stop when the program exits
user_count_thread.start()

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Render the user count
    font = pygame.font.Font(None, 36)
    user_count_text = font.render(f"Connected users: {user_count}", True, (255, 255, 255))
    screen.blit(user_count_text, (10, 10))

    # Update the display
    pygame.display.update()
