from mlc_tools import Mlc


def generate():
    protocol = 'xml'
    # protocol = 'json'
    
    generator = Mlc(configs_directory='./configs', side='client', disable_logs=False, generate_tests=False)

    # Client:
    generator.generate(language='py', formats=protocol, out_directory='./client/mg', side='client')
    generator.generate_data(data_directory='./configs/data_%s' % protocol, out_data_directory='./client/assets')

    # Server Python
    generator.generate(language='py', formats=protocol, out_directory='./server_python/mg', side='server')
    generator.generate_data(data_directory='./configs/data_%s' % protocol, out_data_directory='./server_python')

    # Server PHP
    generator.generate(language='php', formats=protocol, out_directory='./server_php/mg', side='server')
    generator.generate_data(data_directory='./configs/data_%s' % protocol, out_data_directory='./server_php')

    # Server C++
    generator.generate(language='cpp', formats=protocol, out_directory='./server_cpp/mg', side='server',
                       generate_intrusive=True, generate_factory=True)
    generator.generate_data(data_directory='./configs/data_%s' % protocol, out_data_directory='./server_cpp')


if __name__ == '__main__':
    generate()
