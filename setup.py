from setuptools import setup, find_packages

setup(
    name='clima',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
    ],
    description='Paquete para obtener datos climatológicos de AEMET',
    author='Tu Nombre',
    author_email='tu_email@example.com',
    url='https://github.com/tu_usuario/clima',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
