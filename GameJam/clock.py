import pygame

pygame.font.init()


class Clock:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 1
        self.font = pygame.font.SysFont("Pixeltype", 50)  # Font size can be adjusted
        self.message_color = pygame.Color("red")

    # Start the timer
    def start_timer(self):
        self.start_time = 1200  # 20 seconds

    # Update the timer
    def update_timer(self):
        if self.start_time is not None and self.start_time > 0:
            self.start_time -= self.elapsed_time

        # Stop the timer when it reaches zero
        if self.start_time == 0:
            self.stop_timer()

    # Display the timer in minutes:seconds format
    def display_timer(self):
        if self.start_time is not None:
            minutes = int(self.start_time // 60)
            seconds = int(self.start_time % 60)
            # Format the output as "mm:ss"
            my_time = self.font.render(f"{minutes:02}:{seconds:02}", True, self.message_color)
            return my_time
        else:
            # Display "00:00" when the timer is stopped
            my_time = self.font.render("00:00", True, self.message_color)
            return my_time

    # Stop the timer
    def stop_timer(self):
        self.start_time = None
