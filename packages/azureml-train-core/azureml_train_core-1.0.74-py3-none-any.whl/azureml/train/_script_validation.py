# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import ast
import ruamel
import re
import time
import glob
import subprocess
from threading import Thread
import queue
from os.path import isfile
from collections import deque
from azureml.core.conda_dependencies import CondaDependencies

_AIDICT = {}
_JRDICT = {}
_SZDICT = {}
_CONDA_MAPPING = {}
FAILED = 'Failed'
TIMED_OUT = 'Timed Out'


def _validate(source_directory, run_config, telemetry_values):
    start = time.time()
    lint_queue = queue.Queue()
    lint_thread = Thread(target=_run_pyflakes, args=(source_directory,
                                                     run_config.script,
                                                     lint_queue))
    lint_thread.start()

    # Disable package validation when custom docker image is provided and for local runs
    validate = False
    azureml_images = _get_all_framework_images()
    validate_queue = queue.Queue()
    if run_config.environment.docker.base_image in azureml_images \
            and run_config.target != 'local':
        validate_thread = Thread(target=_validate_source_directory, args=(source_directory, run_config,
                                                                          validate_queue))
        validate_thread.start()
        validate = True

    # Checking lint results
    lint_thread.join(timeout=2)
    if lint_thread.is_alive():
        lint_results = TIMED_OUT
    else:
        try:
            lint_results = lint_queue.get(block=False)
            telemetry_values['validationLintTime'] = lint_queue.get(block=False)
        except queue.Empty:
            lint_results = FAILED
    # Normalize results for logging
    if lint_results not in [TIMED_OUT, []] and FAILED not in lint_results:
        normalized_pylint_results = [line.split(':')[-1] for line in lint_results]
        telemetry_values['validationLintErrors'] = normalized_pylint_results
    else:
        telemetry_values['validationLintErrors'] = lint_results if lint_results else False

    # Checking package check results
    package_results = set()
    if validate:
        validate_thread.join(timeout=2)
        if validate_thread.is_alive():
            package_results = TIMED_OUT
        else:
            try:
                package_results = validate_queue.get(block=False)
                telemetry_values['validationPackageTime'] = validate_queue.get(block=False)
                telemetry_values['validationFiles'] = validate_queue.get(block=False)
            except queue.Empty:
                package_results = FAILED

        if package_results != TIMED_OUT and FAILED not in package_results:
            telemetry_values['validationPackageErrors'] = True if package_results else False
        else:
            telemetry_values['validationPackageErrors'] = package_results
    else:
        telemetry_values['validationPackageErrors'] = 'No Validation'

    end = time.time()
    telemetry_values['validationTotalTime'] = end - start
    return lint_results, package_results


def _validate_source_directory(source_directory, run_config, validate_queue):
    try:
        start = time.time()
        # If framework image is used, get packages from scenario file
        base_image = run_config.environment.docker.base_image
        conda_dependencies = run_config.environment.python.conda_dependencies
        scenario_filename = base_image.replace(':', '-') + '.yml'
        scenario_file_path = os.path.join(os.path.dirname(__file__), "estimator", "scenarios", scenario_filename)
        if os.path.exists(scenario_file_path):
            conda_dependencies = _load_from_scenario_file(scenario_file_path)
        pattern = "[\[=|<|>|~|!]"
        user_pip_packages = [re.split(pattern, pip_pkg)[0] for pip_pkg in conda_dependencies.pip_packages]
        user_conda_packages = [re.split(pattern, conda_pkg)[0] for conda_pkg in conda_dependencies.conda_packages]
        user_pip_packages = _update_exceptions(user_pip_packages)

        local_candidates = _get_local_candidates_full_path(source_directory)
        all_imports, visited_files = _get_imports_used_files(source_directory=source_directory,
                                                             entry_script=run_config.script,
                                                             candidates=local_candidates)

        missing_packages = {}

        for name in [module for module in all_imports if module]:
            cleaned_name, _, _ = name.partition('.')
            if cleaned_name in ['azure', 'azureml']:
                modules = name.split('.')
                cleaned_name = '.'.join(modules[:2])

            pypi_packages = set(_get_pypi_package_name(name))
            conda_packages = set(_get_conda_package_name(name))
            if not (pypi_packages & set(user_pip_packages)) \
                    and not (conda_packages & set(user_conda_packages)):
                # An extra check for first level import only
                pypi_packages = set(_get_pypi_package_name(cleaned_name))
                conda_packages = set(_get_conda_package_name(cleaned_name))
                if not (pypi_packages & set(user_pip_packages)) \
                        and not (conda_packages & set(user_conda_packages)):
                    if name not in missing_packages.keys():
                        missing_packages[name] = pypi_packages if pypi_packages is not {cleaned_name} \
                            else conda_packages

        validate_queue.put(missing_packages)
        validate_queue.put(time.time() - start)
        validate_queue.put(len(visited_files))
    except Exception as e:
        validate_queue.put('Failed - {}'.format(str(e)))
        validate_queue.put(time.time() - start)
        validate_queue.put(0)


def _run_pyflakes(source_directory, entry_script, lint_queue):
    try:
        start = time.time()
        local_candidates = _get_local_candidates_full_path(source_directory)
        all_imports, visited_files = _get_imports_used_files(source_directory=source_directory,
                                                             entry_script=entry_script,
                                                             candidates=local_candidates)

        cmd = 'python -m flake8 --select F821,E999,F823 ' + ' '.join(visited_files)
        process = subprocess.run(cmd, shell=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 timeout=2)
        pyflakes_output = process.stdout.decode("utf-8")
        error = process.stderr.decode("utf-8")
        # flake8 exits with return code 1 when successful but errors found
        # so need to differentiate between that and actual failure
        if process.returncode == 1:
            if pyflakes_output:
                pyflakes_results = [line for line in pyflakes_output[:-1].split('\n')]
                lint_queue.put(pyflakes_results)
            else:
                lint_queue.put('Flake8 Failed: {}'.format(error))
        elif process.returncode == 0:
            lint_queue.put([])
        else:
            lint_queue.put('Flake8 Failed: {}'.format(error))
        lint_queue.put(time.time() - start)
    except Exception as e:
        lint_queue.put('Failed - {}'.format(str(e)))
        lint_queue.put(time.time() - start)


def _get_local_candidates_full_path(source_directory):
    """
    This function navigates the source directory to identify all files that could be imported locally.
    :param source_directory:A  local directory containing experiment configuration files.
    :return: A dictionary of possible local imports and their full paths.
    """
    candidates = {}
    walk = os.walk(source_directory)
    ignore_dirs = [".hg", ".svn", ".git", ".tox", "__pycache__", "env", "venv"]

    for root, dirs, files in walk:
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        candidates[os.path.basename(root)] = [root]

        files = [os.path.splitext(fn)[0] for fn in files if os.path.splitext(fn)[1] == ".py"]
        for file in files:
            # map filename without extension (example: utils) to file's full path
            # It is a list to account for files with same name but different locations
            if file not in candidates.keys():
                candidates[file] = []
            candidates[file].append(os.path.join(root, file + '.py'))

    return candidates


def _get_imports_used_files(source_directory, entry_script, candidates):
    """
    Not all files in the source directory are used at runtime.
    This function finds files used at runtime using local imports starting from the entry script.
    :param source_directory:A  local directory containing experiment configuration files.
    :param entry_script: The relative path to the file containing the training script.
    :param candidates: A dictionary of possible local imports and their full paths.
    :return: A list of external imports and a list of runtime files
    """
    queue = deque()
    visited = set()
    queue.append(os.path.join(source_directory, entry_script))
    visited.add(os.path.join(source_directory, entry_script))
    all_raw_imports = []

    while len(queue) != 0:
        raw_imports = set()
        file_name = queue.popleft()

        with open(file_name, "r", encoding='utf-8') as file:
            contents = file.read()
        try:
            tree = ast.parse(contents)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for subnode in node.names:
                        raw_imports.add(subnode.name)
                elif isinstance(node, ast.ImportFrom):
                    raw_imports.add(node.module)
        except Exception as e:
            pass

        local_imports = []
        for module in [name for name in raw_imports if name]:
            clean_import = module.split('.')[0]  # add else statement
            for candidate in candidates.get(clean_import, []):
                local_imports.append(module)
                if candidate not in visited and isfile(candidate):
                    queue.append(candidate)
                    visited.add(candidate)

        # Removing the local imports that were found in this file
        raw_imports = raw_imports - set(local_imports)
        all_raw_imports.extend(raw_imports)

    all_raw_imports = set(all_raw_imports)

    # removing python packages
    with open(os.path.join(os.path.dirname(__file__), "metadata", "stdlib"), "r") as file:
        python_packages = {line.strip() for line in file}

    return list(all_raw_imports - python_packages), list(visited)


def _load_md_files():
    try:
        import zipfile
        global _AIDICT
        global _JRDICT
        global _SZDICT
        global _CONDA_MAPPING
        md_directory = os.path.join(os.path.dirname(__file__), 'metadata')
        path = os.path.join(md_directory, 'a-i')

        if not os.path.exists(path):
            zip_path = os.path.join(md_directory, 'a-i.zip')
            with zipfile.ZipFile(zip_path, 'r') as unzip:
                unzip.extractall(md_directory)
        with open(path, "r") as file:
            _AIDICT = dict([line.strip().split(":")[0], line.strip().split(':')[1].split(',')] for line in file)

        path = os.path.join(md_directory, 'j-r')
        if not os.path.exists(path):
            zip_path = os.path.join(md_directory, 'j-r.zip')
            with zipfile.ZipFile(zip_path, 'r') as unzip:
                unzip.extractall(md_directory)
        with open(path, "r") as file:
            _JRDICT = dict([line.strip().split(":")[0], line.strip().split(':')[1].split(',')] for line in file)

        path = os.path.join(md_directory, 's-z')
        if not os.path.exists(path):
            zip_path = os.path.join(md_directory, 's-z.zip')
            with zipfile.ZipFile(zip_path, 'r') as unzip:
                unzip.extractall(md_directory)
        with open(path, "r") as file:
            _SZDICT = dict([line.strip().split(":")[0], line.strip().split(':')[1].split(',')] for line in file)

        path = os.path.join(md_directory, 'conda-mapping')
        if not os.path.exists(path):
            zip_path = os.path.join(md_directory, 'conda-mapping.zip')
            with zipfile.ZipFile(zip_path, 'r') as unzip:
                unzip.extractall(md_directory)
        with open(path, "r") as file:
            _CONDA_MAPPING = dict([line.strip().split(":")[0], line.strip().split(':')[1].split(',')] for line in file)
    except Exception:
        pass


def _get_pypi_package_name(package):

    start_char = package[0].lower()
    if start_char.isalpha():
        if 'a' <= start_char <= 'i':
            return _AIDICT.get(package, [package])
        elif 'j' <= start_char <= 'r':
            return _JRDICT.get(package, [package])

    return _SZDICT.get(package, [package])


def _get_conda_package_name(package):
    return _CONDA_MAPPING.get(package, [package])


def _load_from_scenario_file(scenario_path):
    if not os.path.isfile(scenario_path):
        return
    with open(scenario_path, "r") as input:
        scenario = ruamel.yaml.round_trip_load(input)
        dependencies = scenario.get('inlineCondaDependencies', None)
    return CondaDependencies(_underlying_structure=dependencies)


def _update_exceptions(user_pip_packages):
    if 'azureml-defaults' in user_pip_packages:
        user_pip_packages.extend(['azureml-core'])

    # TODO: Add all tensorflow packages tf-nightly etc...
    if 'tensorflow' in user_pip_packages or 'tensorflow-gpu' in user_pip_packages:
        user_pip_packages.extend(['absl-py', 'astor', 'backports.weakref',
                                  'enum34', 'gast', 'google-pasta', 'grpcio',
                                  'keras-applications', 'keras-preprocessing',
                                  'numpy', 'opt-einsum', 'protobuf', 'six', 'tensorboard',
                                  'tensorflow-estimator', 'termcolor', 'wheel', 'wrapt'])

    if 'scipy' in user_pip_packages:
        user_pip_packages.append('numpy')

    if 'cntk-gpu' in user_pip_packages:
        user_pip_packages.extend(['numpy', 'scipy'])

    return user_pip_packages


def _get_all_framework_images():
    files = glob.glob(os.path.join(os.path.dirname(__file__), 'estimator', 'scenarios', '**/*.yml'), recursive=True)
    filenames = [os.path.splitext(os.path.basename(file))[0] for file in files]
    azureml_images = [file.replace('-', ':', 1) for file in filenames]
    for file in files:
        with open(file, "r") as input:
            scenario = ruamel.yaml.round_trip_load(input)
            base_image = scenario.get('baseImage', None)
            azureml_images.append(base_image)

    return azureml_images
