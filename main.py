from sys import stdout
import pygame
import time

# Initialize pygame for joystick support
pygame.display.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()

while True:

    # Get next pygame event
    pygame.event.pump()
    send_string = "!JOY,"
    stdout.write('%s | Axes: ' % controller.get_name())

    for k in range(controller.get_numaxes()):
        stdout.write('%d:%+2.2f ' % (k, controller.get_axis(k)))
        send_string += '%+2.2f,' % controller.get_axis(k)
    stdout.write(' | Buttons: ')
    for k in range(controller.get_numbuttons()):
        stdout.write('%d:%d ' % (k, controller.get_button(k)))
        send_string += '%d,' % controller.get_button(k)
    stdout.write(' | Hat: ')
    for k in range(controller.get_numhats()):
        stdout.write('%d:%s ' % (k, controller.get_hat(k)))
        send_string += str(controller.get_hat(k)) + ","

    send_string += "*"
    while len(send_string) != 100:
        send_string += "*"
    stdout.write('\n')
    print(send_string)
    time.sleep(0.05)
