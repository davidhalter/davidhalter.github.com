import time
import os
from fabric.api import local, settings



def push():
    local('git push')


def sync():
    # this is special because of github pages, pure html goes into master
    if not os.path.exists('build'):
        raise ValueError('Build directory must exist.')
    last_commit = local('git log -n 1 --pretty=%B', capture=True)
    local('git checkout master')
    local('ls | grep -v build | xargs -n 1 rm -r')
    local('cp -r build/* .')
    local('mv build .build')
    local('ls | xargs git add')
    local('mv .build build')
    com = last_commit.replace('"', r'\"')
    with settings(warn_only=True):
        local('git commit -a -m "new release: %s"' % com)
    local('git push')

    local('git checkout dev')


def serve():
    local('run-rstblog serve')


def build():
    # Build HTML
    local('rm -rf _build/ && run-rstblog build')

    # Generate sitemaps
    local('python gensitemap.py > _build/sitemap.xml')

    # Minify CSS
    local('cssmin < _build/static/style.css > _build/static/style.min.css')
    local('mv _build/static/style.min.css _build/static/style.css')
    local('cssmin < _build/static/_pygments.css > _build/static/_pygments.min.css')
    local('mv _build/static/_pygments.min.css _build/static/_pygments.css')

    # Add timestamp to css files
    local('find _build -type f -exec sed -i "s/\(link.*\)style.css/\\1style.css?%s/g" {} \;' % int(time.time()))
    local('find _build -type f -exec sed -i "s/\(link.*\)_pygments.css/\\1_pygments.css?%s/g" {} \;' % int(time.time()))


def publish():
    push()
    build()
    sync()
