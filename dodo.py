def task_setup_tool():
    return {
        'actions': [
            'python3 -m pip install -e .'
        ]
    }


def task_lint():
    return {
        'actions': [
            'flake8 --ignore=F401,E501'
        ]
    }


def task_unit_tests():
    return {
        'actions': [
            'pytest -v'
        ]
    }
