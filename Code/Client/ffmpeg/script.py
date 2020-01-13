import os
import sys

"""
인수 3개인지 확인
"""
if len(sys.argv) != 4:
	print("error occurs: input 3 parameters (file, rate, length)")
	print("example: temp.y4m, 50K, 2")
	sys.exit()

"""
파일이 맞는 지 확인
"""
input_file = sys.argv[1]
if (not ("." in input_file)) or (not os.path.exists(input_file)):
	print("error occurs: check your input (file)")
	sys.exit()

"""
인코딩 레이트 맞는 지 확인
"""
input_rate = sys.argv[2].upper()
if (not ("M" in input_rate or "K" in input_rate)) or ("M" in input_rate and "K" in input_rate) or ((input_rate.count("M") > 1) or (input_rate.count("K") > 1)):
	print("error occurs: check your input (rate)")
	sys.exit()

try:
	int(input_rate[:-1])
except:
	print("error occurs: check your input (rate)")
	sys.exit()

"""
영상 재생 시간 구하기
"""
sum_length = 0
try:
	os.system("ffmpeg -i " + input_file + " > temp_length 2>&1")
except:
	print("error occurs: ffmpeg")
	sys.exit()

try:	
	file = open("temp_length", "r")
	for line in file.readlines():
		if "Duration" in line:
			str_length = line.strip().split(" ")[1]
			str_length = str_length[0 : str_length.find(".")]

			for i, num in enumerate(str_length.split(":")):
				sum_length += pow(60, 2 - i) * int(num)
				
	file.close()
	os.remove("temp_length")
except:
	print("error occurs: can not get length information")
	sys.exit()

"""
입력 단위 시간 맞는 지 확인
"""
try:
	input_length = int(sys.argv[3])
except:
	print("error occurs: check your input (length)")
	sys.exit()

if input_length > sum_length:
	print("error occurs: check your input (length)")
	sys.exit()

"""
mp4파일 만들기
"""
name = input_file.split(".")[0]
if not os.path.exists(name + ".mp4"):
	os.system("ffmpeg -i " + input_file + " -c:v libx264 -preset ultrafast -qp 0 -pix_fmt yuv420p -movflags +faststart " + name + ".mp4")

index = 0
while input_length * index < sum_length:
	os.system("ffmpeg -ss " + str(input_length * index) + " -i " + name + ".mp4 -t 2 -c:v libx264 -c:a copy temp_" + str(index) + ".mp4")
	os.system("ffmpeg -i temp_" + str(index) + ".mp4 -b:v " + input_rate + " " + name + "_" + str(index) + "_" + input_rate + ".mp4")
	os.remove("temp_" + str(index) + ".mp4")
	index += 1
