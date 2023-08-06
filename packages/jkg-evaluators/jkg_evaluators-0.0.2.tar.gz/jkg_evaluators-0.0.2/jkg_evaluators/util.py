import os


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def get_code_nb_cell(code="", metadata=None, outputs=None, execution_count=None):
    return {
        "cell_type": "code",
        "source": [code],
        "metadata": metadata or {},
        "outputs": outputs or [],
        "execution_count": execution_count,
    }
