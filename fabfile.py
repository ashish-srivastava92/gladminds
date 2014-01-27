from fabric.api import task, run, local
import os

COVERAGE_ENABLED = False
PROJECT_PACKGE = 'gladminds'

def _ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

@task()
def docs_gen():
    '''Generates Documents. Picks sources from docs folder.'''
    local("bin/sphinxbuilder")


@task()
def uml_gen():
    '''Generates Package Dependency Diagrams. Assumes Graphviz.'''
    local('bin/pyreverse -p deps %s' % PROJECT_PACKGE)
    local('mv *.dot out/')
    _ensure_dir('out/docs')
    local('dot -Tpng out/packages_deps.dot -o out/docs/packages_deps.png')


@task()
def runserver():
    '''Runs Django Server on port 8000'''
    local("bin/django runserver 0.0.0.0:8000")

@task()
def lint_py():
    '''Reports Pylint Errors & Warnings for Python files'''
    local('bin/pylint --rcfile=etc/lint.rc %s' % PROJECT_PACKGE)


@task()
def lint_js():
    '''Reports Pylint Errors & Warnings for Python files'''
    local('bin/jshint --config=etc/jshint.json src/static/js')


@task()
def coverage():
    '''Enables Coverage. Used for test targets'''
    global COVERAGE_ENABLED
    COVERAGE_ENABLED = True


@task()
def test_all():
    '''Runs All Tests in src and tests folders'''
    test()


@task()
def test_integration():
    '''Runs All Tests in tests/integration package'''
    test('integration')


@task()
def test_unit():
    '''Runs All Tests in tests/unit package'''
    test('unit')


def test(package=''):
    '''Run Tests for the given package'''
    options = ['--with-progressive']

    if COVERAGE_ENABLED:
        options.append('--with-coverage')
        options.append('--cover-package=%s' % PROJECT_PACKGE)
        options.append('--cover-min-percentage=80')

    local('bin/test test {0} {1}'.format(package, ' '.join(options)))
