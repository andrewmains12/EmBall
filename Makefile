
PACKAGES=emball
RESOURCES="Images,doc,Levels"
setup:
	env py2applet --make-setup --packages=$(PACKAGES) --resources=$(RESOURCES) EmBall.py

package: setup.py
	python setup.py py2app
	echo
	echo "Copying patched __init__ file for numpy"
	cp numpy_init  dist/EmBall.app/Contents/Resources/lib/python2.7/numpy/core/__init__.py

clean:
	rm -rf build dist
