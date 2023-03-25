DATE=$(date +"%Y-%m-%d_%H%M%S")

raspistill -hf -t 1800 -w 350 -h 350 -o /home/pi/camera/$DATE.jpg
