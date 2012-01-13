
PACKAGES=emball
RESOURCES="Images,doc,Levels"

SRC_FILES=emball/*.py

setup: $(SRC_FILES)
	env py2applet --make-setup --packages=$(PACKAGES) --resources=$(RESOURCES) EmBall.py

package: setup.py
	python setup.py py2app
	echo "Copying patched __init__ file for numpy"
	cp numpy_init  dist/EmBall.app/Contents/Resources/lib/python2.7/numpy/core/__init__.py

TAR_FILE=dist/EmBall.tar.gz
distribute: dist/EmBall.app
	tar -cvf $(TAR_FILE) dist/EmBall.app
	cp $(TAR_FILE) ~/Public/

test:
	python -m unittest discover --start-directory=./emball

clean:
	rm setup.py
	rm -rf build dist
