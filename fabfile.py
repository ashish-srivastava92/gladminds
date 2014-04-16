from fabric.api import task, run, local
import os
from subprocess import Popen

COVERAGE_ENABLED = False
PROJECT_PACKGE = 'gladminds'
NEVER_FAIL = False
CAPTURE = False

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
def create_android_build(ip_address):
    '''Runs Django Server on port 8000'''
    process = Popen('./afterbuy_script/phonegap_build.sh %s' % \
                                        (ip_address), shell=True)
    process.wait()


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
    '''Run Tests for the given package bin/fab test:<package>'''
    options = ['--with-progressive']
    options.append('--with-xunit')
    options.append('--xunit-file=out/xunit.xml')

    if COVERAGE_ENABLED:
        options.append('--with-coverage')
        options.append('--cover-html')
        options.append('--cover-xml')
        options.append('--cover-xml-file=out/coverage.xml')
        options.append('--cover-erase')
        options.append('--cover-html-dir=out/coverage')
        options.append('--cover-package=%s' % PROJECT_PACKGE)
        options.append('--cover-min-percentage=80')

    return _execute('bin/test test {0} {1}'.format(package, ' '.join(options)))


def _execute(cmd):
    if NEVER_FAIL:
        cmd = '%s; echo "Done"' % cmd

    return local(cmd, capture=CAPTURE)