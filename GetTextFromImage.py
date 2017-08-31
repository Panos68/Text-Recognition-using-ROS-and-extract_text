import os
import sys

if len(sys.argv) != 3:
    print "%s input_file output_file" % (sys.argv[0])
    sys.exit()
else:
    input_file = sys.argv[1]
    output_file = sys.argv[2]

if not os.path.isfile(input_file):
    print "No such file '%s'" % input_file
    sys.exit()

os.system("tesseract "+input_file+" before_"+output_file)
os.system("python extract_text.py "+input_file+" "+"extract.png")
os.system("tesseract "+"extract1.png"+" after_"+output_file)


filenames = ["before_"+output_file+".txt", "after_"+output_file+".txt"]
with open('/home/name/yourfolder/finaltext.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
