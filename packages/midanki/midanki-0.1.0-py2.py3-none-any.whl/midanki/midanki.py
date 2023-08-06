import pygame.midi
from pynput.keyboard import Key, Controller
#import notify2

def print_devices():
    for n in range(pygame.midi.get_count()):
        print (n,pygame.midi.get_device_info(n))

def number_to_note(number):
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number%12]

def note_to_number(key):
    keydict = {
        'c':Key.space,
        'd':'1',
        'e':'2',
        'f':'3',
        'g':'4',
        'a':'5',
        'c#':Key.down,
        'd#':Key.up,
        'f#':Key.page_down,
        'a#':Key.page_up,
    }
    # keydict = {
    #     'c':'j',
    #     'd':'k',
    #     'e':'l',
    #     'f':';',
    #     'a':'5',
    #     'b':'6'
    # }
    if key in keydict.keys():
        print("Pressed ", keydict[key])
        keyboard.press(keydict[key])
        keyboard.release(keydict[key])

def readInput(input_device):
    active = True
    while True:
        if input_device.poll():
            read = input_device.read(1)
            event = read[0]
            data = event[0]
            timestamp = event[1]
            note_number = data[1]
            input = data[0]
            velocity = data[2]
            if input == 176 and note_number == 66 and velocity > 0:
                active = not active 
                #if active:
                #    n = notify2.Notification("Anki Mode On")
                #else:
                #    n = notify2.Notification("Anki Mode Off")
                #n.show()
            if active and velocity > 0 and note_number > 59 and input == 144:
                print(read)
                print (number_to_note(note_number), velocity)
                note = number_to_note(note_number)
                note_to_number(note) 

def main(input: int):
    #notify2.init("midi anki")
    pygame.midi.init()
    keyboard = Controller()
    print_devices()
    my_input = pygame.midi.Input(input) #only in my case the id is 2
    readInput(my_input)

if __name__ == '__main__':
    main()