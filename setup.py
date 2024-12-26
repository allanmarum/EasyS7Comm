from setuptools import setup, find_packages

setup(
    name="easys7comm",
    version="0.0.2",
    description="Um módulo para comunicação com PLCs usando S7.",
    author="Seu Nome",
    author_email="seuemail@exemplo.com",
    url="https://github.com/usuario/EasyS7Comm",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        # Dependências listadas no requirements.txt ou aqui
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows",
    ],
    python_requires=">=3.6",
)

