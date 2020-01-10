@echo off


ffmpeg -i %1 -c:v libx264 -preset ultrafast -qp 0 -pix_fmt yuv420p -movflags +faststart temp_raw.mp4

for /L %%i in (0, 2, 16 - 1) do (
	ffmpeg -ss %%i -i temp_raw.mp4 -t 2 -c:v libx264 -c:a copy temp_%%i.mp4
	ffmpeg -i temp_%%i.mp4 -b:v 128K temp_%%i_128K.mp4
	del temp_%%i.mp4
)

del temp_raw.mp4