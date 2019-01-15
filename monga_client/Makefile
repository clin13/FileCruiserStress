#!/usr/bin/make -f

NAME=monga-client

all: clean package

package:
	fpm -s python -t deb -a amd64 -d "python" -x '**/*.py' \
		--python-package-name-prefix filecruiser \
		setup.py

clean:
	rm -rf dist build filecruiser-$(NAME)*.deb *.egg-info
