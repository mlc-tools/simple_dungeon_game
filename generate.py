import os

os.system('python ./mlc/src/main.py -i ./configs -o ./client/mg -l py -f xml -side client -data ./configs/data -data_out ./client/assets')
os.system('python ./mlc/src/main.py -i ./configs -o ./server_python/mg -l py -f xml -side server -data ./configs/data -data_out ./server_python')
os.system('python ./mlc/src/main.py -i ./configs -o ./server_php/mg -l php -f xml -side server -data ./configs/data -data_out ./server_php')
os.system('python ./mlc/src/main.py -i ./configs -o ./server_cpp/mg -l cpp -f xml -side server -data ./configs/data -data_out ./server_cpp')
