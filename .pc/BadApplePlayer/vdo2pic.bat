.\ffmpeg.exe -i ".\BadApple.flv" -r 8 -vf crop="iw:iw/2:0:(ih-(iw/2))/2",lutyuv="y=if(gte(val\,128)\,255\,0):u=128:v=128" -s 128x64 ".\BadApple-fps-8\BadApple%%04d.png"
.\ffmpeg.exe -i ".\BadApple.flv" -r 16 -vf crop="iw:iw/2:0:(ih-(iw/2))/2",lutyuv="y=if(gte(val\,128)\,255\,0):u=128:v=128" -s 128x64 ".\BadApple-fps-16\BadApple%%04d.png"
.\ffmpeg.exe -i ".\BadApple.flv" ".\BadApple.mp3"
pause