from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.display import Display

leds = Leds()
sound = Sound()
display = Display()
buttons = Button()

sound.set_volume(20)

def Color(color):
	leds.set_color('LEFT',color.upper())
	leds.set_color('RIGHT',color.upper())

def PlayTone(tone,time=0.2):
	sound.play_tone(tone,time,0,20,sound.PLAY_NO_WAIT_FOR_COMPLETE)