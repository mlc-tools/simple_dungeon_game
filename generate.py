from mlc_tools import Generator


def generate():
    protocol = 'xml'
    generator = Generator(configs_directory='./configs', side='client', disable_logs='no', generate_tests='no')

    # Client:
    generator.generate('py', protocol, './client/mg')
    generator.generate_data('./configs/data_%s' % protocol, './client/assets')

    # Server Python
    generator.generate('py', protocol, './server_python/mg', side='server')
    generator.generate_data('./configs/data_%s' % protocol, './server_python')

    # Server PHP
    generator.generate('php', protocol, './server_php/mg', side='server')
    generator.generate_data('./configs/data_%s' % protocol, './server_php')

    # Server C++
    generator.generate('cpp', protocol, './server_cpp/mg', side='server', generate_intrusive='yes')
    generator.generate_data('./configs/data_%s' % protocol, './server_cpp')


if __name__ == '__main__':
    generate()
