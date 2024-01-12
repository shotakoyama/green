import setuptools

setuptools.setup(
        name = 'green',
        version = '0.1.0',
        packages = setuptools.find_packages(),
        entry_points = {
            'console_scripts':[
                'green = green.main:green',
                'sgreen = green.main:sgreen',
                'mgreen = green.main:mgreen']})

