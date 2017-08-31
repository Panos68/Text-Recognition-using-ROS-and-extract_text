import os
import sys
import difflib

looking_word=""
if len(sys.argv) < 2:
	print "%s looking_word" % (sys.argv[0])
	sys.exit()
else:
	for x in range (1,len(sys.argv)):
		looking_word = looking_word+sys.argv[x]
	
#on another terminal pointing on the same folder write “rosrun image_view image_view
#image:=/camera/rgb/image_raw _save_all_image:=false _filename_format:=camerapic.jpg
#__name:=image_saver

os.system("rosservice call /image_saver/save")
os.system("tesseract web-cam-shot.jpg before_extract")
os.system("python extract_text.py web-cam-shot.jpg"+" extract1.png")
os.system("tesseract "+"extract1.png"+" after_extract")

filenames = ["before_extract.txt", "after_extract.txt"]
with open('/home/name/your_folder/finaltext.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())


with open('finaltext.txt', 'r') as myfile:
    data=myfile.readlines()

for x in range(0, len(data)):
	seq=difflib.SequenceMatcher(None, looking_word,data[x])
	d=seq.ratio()*100
	if (d>60):
		print (d)
		print (data[x])

