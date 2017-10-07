from pynq.overlays.base import BaseOverlay
from time import sleep
base = BaseOverlay("base.bit")
pAudio = base.audio

pAudio.load("sin1.pdm")
pAudio.play()


sleep(3)

pAudio.load("sin2.pdm")
pAudio.play()

