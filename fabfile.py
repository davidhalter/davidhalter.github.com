import time
import os
from fabric.api import local, settings

SUB_BLOGS = ['code', 'leben']


def push():
    local('git push')


def sync():
    # this is special because of github pages, pure html goes into master
    if not os.path.exists('_build'):
        raise ValueError('Build directory must exist.')
    last_commit = local('git log -n 1 --pretty=%B', capture=True)
    local('git checkout master')
    local('ls | grep -v _build | xargs -n 1 rm -r')
    local('cp -r _build/* .')
    local('mv _build .build')
    local('git add *')
    local('mv .build _build')
    com = last_commit.replace('"', r'\"')
    with settings(warn_only=True):
        local('git commit -a -m "new release: %s"' % com)
    local('git push')

    local('git checkout dev')


def build_sub_blogs():
    for sub_blog in SUB_BLOGS:
        os.chdir('_%s' % sub_blog)
        local('rm -rf _build/ && run-rstblog build')
        local('rm -rf ../_build/%s' % sub_blog)
        local('mv _build/%s ../_build/' % sub_blog)
        os.chdir('..')


def serve():
    local('rm -rf _build/ && mkdir _build')
    build_sub_blogs()
    local('run-rstblog serve')


def build():
    # Build HTML
    local('rm -rf _build/ && run-rstblog build')
    build_sub_blogs()

    # Generate sitemaps
    local('python gensitemap.py > _build/sitemap.xml')

    # Minify CSS
    local('cssmin < _build/static/style.css > _build/static/style.min.css')
    local('mv _build/static/style.min.css _build/static/style.css')
    local('cssmin < _build/static/_pygments.css > _build/static/_pygments.min.css')
    local('mv _build/static/_pygments.min.css _build/static/_pygments.css')

    # Add timestamp to css files
    local('find _build -type f -exec sed -i "s/\(link.*\)style.css/\\1style.css?1358541794?%s/g" {} \;' % int(time.time()))
    local('find _build -type f -exec sed -i "s/\(link.*\)_pygments.css/\\1_pygments.css?1358541795?%s/g" {} \;' % int(time.time()))


def publish():
    push()
    build()
    sync()
