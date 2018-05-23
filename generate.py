from mlc_tools import Generator


def generate():
    generator = Generator(configs_directory='./configs', side='client', disable_logs='no', generate_tests='no')

    # Client:
    generator.generate('py', 'json', './client/mg')
    generator.generate_data('./configs/data_json', './client/assets')

    # Server Python
    generator.generate('py', 'json', './server_python/mg', side='server')
    generator.generate_data('./configs/data_json', './server_python')

    # Server PHP
    generator.generate('php', 'json', './server_php/mg', side='server')
    generator.generate_data('./configs/data_json', './server_php')

    # Server C++
    generator.generate('cpp', 'json', './server_cpp/mg', side='server', generate_intrusive='yes')
    generator.generate_data('./configs/data_json', './server_cpp')

if __name__ == '__main__':
    generate()

# os.system('python ./mlc/src/main.py -i ./configs -o ./client/mg -l py -f json -side client -data ./configs/data_json -data_out ./client/assets')
# os.system('python ./mlc/src/main.py -i ./configs -o ./server_python/mg -l py -f json -side server -data ./configs/data_json -data_out ./server_python')
# os.system('python ./mlc/src/main.py -i ./configs -o ./server_php/mg -l php -f json -side server -data ./configs/data_json -data_out ./server_php')
# os.system('python ./mlc/src/main.py -i ./configs -o ./server_cpp/mg -l cpp -f json -side server -data ./configs/data_json -data_out ./server_cpp')
