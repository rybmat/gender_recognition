import os
import wave

files=[]
names=os.listdir('.')
for el in names:
	if el!='params.py':
		files.append(wave.open(el,'rb'))

	
for el in files:
	print el.getnframes()/el.getframerate()
	el.close()	
