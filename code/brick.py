from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.button import Button

leds = Leds()
sound = Sound()
buttons = Button()

sound.set_volume(20)

def Color(color):
	leds.set_color('LEFT',color.upper())
	leds.set_color('RIGHT',color.upper())

def PlayTone(tone):
	sound.play_tone(tone,0.2,0,20,sound.PLAY_NO_WAIT_FOR_COMPLETE)