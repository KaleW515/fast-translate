PREFIX=/opt
APP_PATH=/opt


check-dependency:
	pip3 install -r requirements.txt

clear:
	rm -rf ./build
	rm -rf ./disk
	rm -rf ./test*
	rm -rf ./tempCodeRunnerFile*
	rm -rf ./cache
	rm -rf *.spec

build: clear
	mkdir -p build/fast-translate/usr/bin
	mkdir -p build/fast-translate/usr/share/applications
	mkdir -p build/fast-translate/usr/share/icons
	mkdir -p build/fast-translate$(APP_PATH)/fast-translate

	cp pkg/aur/ftranslate build/fast-translate/usr/bin/

	cp src/data/icon/logo.svg.png build/fast-translate/usr/share/icons/fast-translate.png
	cp pkg/aur/fast-translate.desktop build/fast-translate/usr/share/applications/

	cp -r src/* build/fast-translate$(APP_PATH)/fast-translate/

uninstall:
	sudo rm -rf $(PREFIX)/fast-translate
	sudo rm -rf /usr/bin/ftranslate /usr/share/icons/fast-translate.png /usr/share/applications/fast-translate.desktop

install: uninstall
	sudo mkdir -p /usr/bin/
	sudo mkdir -p /usr/share/icons/
	sudo cp -r ./build/fast-translate$(PREFIX)/fast-translate $(PREFIX)/
	sudo cp build/fast-translate/usr/bin/* /usr/bin/
	sudo cp build/fast-translate/usr/share/icons/* /usr/share/icons/
	sudo cp build/fast-translate/usr/share/applications/* /usr/share/applications/
