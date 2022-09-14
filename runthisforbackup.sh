rsync -aR Pipfile Pipfile.lock _scrap/ apps/hiero/_scrap/ apps/maya/_scrap.py apps/maya/_scrap/ apps/nuke/_scrap/ completion/ pyrightconfig.json python/pp_tracker/trackers/shotgun/_scrap/ /homes/talhaa/Repos/sapper_excludes/
rsync -aR $(git ls-files -o -i --directory --exclude-standard | grep -v "pyc") ~/Repos/sapper_excludes/
rsync -aR $(git ls-files -o -i --directory --exclude-standard | grep -v "pyc") ~/Repos/sapper_excludes/
