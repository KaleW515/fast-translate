PREFIX=/opt
APP_PATH=/opt
APP_NAME=fast-translate


check-dependency:
	pip3 install -r requirements.txt

clear:
	rm -rf ./build
	rm -rf ./disk
	rm -rf ./test*
	rm -rf ./tempCodeRunnerFile*
	rm -rf ./cache
	rm -rf *.spec

build: clear check-dependency
	mkdir -p build/$(APP_NAME)/usr/bin
	mkdir -p build/$(APP_NAME)/usr/share/applications
	mkdir -p build/$(APP_NAME)/usr/share/icons
	
	mkdir -p build/$(APP_NAME)$(APP_PATH)/$(APP_NAME)

	cp pkg/aur/ftranslate build/$(APP_NAME)/usr/bin/
	cp src/data/icon/logo.svg.png build/$(APP_NAME)/usr/share/icons/fast-translate.png
	cp pkg/aur/fast-translate.desktop build/$(APP_NAME)/usr/share/applications/

	cp -r src/* build/$(APP_NAME)$(APP_PATH)/$(APP_NAME)/

uninstall:
	sudo rm -rf $(PREFIX)/$(APP_NAME)
	sudo rm -rf /usr/bin/ftranslate /usr/share/icons/fast-translate.png /usr/share/applications/fast-translate.desktop

install: uninstall
	sudo mkdir -p /usr/bin/
	sudo mkdir -p /usr/share/icons/
	sudo cp -r ./build/$(APP_NAME)$(PREFIX)/$(APP_NAME) $(PREFIX)/
	sudo cp build/$(APP_NAME)/usr/bin/* /usr/bin/
	sudo cp build/$(APP_NAME)/usr/share/icons/* /usr/share/icons/
	sudo cp build/$(APP_NAME)/usr/share/applications/* /usr/share/applications/
