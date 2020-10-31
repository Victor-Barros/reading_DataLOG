# Victor's binary DataLOG file reader to CSV
import csv
import sys


if len(sys.argv) < 2:
	print("Provide input file...")
	sys.exit()

byte_array = []

with open(sys.argv[1],"rb") as file: #read every byte and save to a list
	byte = file.read(1)
	while byte:
		byte_array.append(byte)
		byte = file.read(1)


print("File Length: "+str(len(byte_array)))

#sector 2
print("Sector 2 (Channel Data): ")


values=[[0],[0],[0],[0],[0],[0],[0],[0]] #to store analog data


offset=512 #offset for sector 2 (512)
nread=1<<20 #limit of iterations 2^20

for i in range(0,2*9*nread,2): #for each 9 lines of  16 bits

	if i+offset+1 > len(byte_array): #check if it's EOF
		print("EOF")
		break

	#Construct word from two bytes
	word = (byte_array[offset+i][0] << 8) | byte_array[offset+1+i][0]
	
	#print(str(format(int(i/2),"03d"))+": "+str(format(word,"016b")))
	
	#digital data between readings
	if word != 0x3f:
		#read channel and data
		channel = word>>13
		data = word&0x1FFF
		#store readings
		values[channel].append(data)
		#print the high 3 (channel) and low 13 (data) values
		print("Channel: "+str(channel)+", Value: "+str(data))
	else:
		print("-------------------------")

with open(sys.argv[1]+".csv", "w") as out_file:
	data_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	#header row
	data_writer.writerow(["ch0","ch1","ch2","ch3","ch4","ch5","ch6","ch7"])
	
	#add an entry for each channel, ignoring the first (zeros) and last (usually incomplete) reading
	for i in range(1,len(values[0])-2):
		data_writer.writerow([values[0][i],values[1][i],values[2][i],values[3][i],values[4][i],values[5][i],values[6][i],values[7][i]])


#end
