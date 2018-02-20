import os

os.system('python ./mlc/src/main.py -i ./configs -o ./client/mg -l py -f json -side client -data ./configs/data_json -data_out ./client/assets')
os.system('python ./mlc/src/main.py -i ./configs -o ./server_python/mg -l py -f json -side server -data ./configs/data_json -data_out ./server_python')
os.system('python ./mlc/src/main.py -i ./configs -o ./server_php/mg -l php -f json -side server -data ./configs/data_json -data_out ./server_php')
os.system('python ./mlc/src/main.py -i ./configs -o ./server_cpp/mg -l cpp -f json -side server -data ./configs/data_json -data_out ./server_cpp')
