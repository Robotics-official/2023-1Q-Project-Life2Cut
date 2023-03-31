DATE=$(date +"%Y-%m-%d_%H%M%S")

raspistill -hf -t 1800 -w 400 -h 390 -o ./images/temp/$DATE.jpg

ls -t
