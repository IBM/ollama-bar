.PHONY: clean
clean:
	rm -rf build dist *.egg-info

.PHONY: test
test:
	./scripts/run_tests.sh

.PHONY: build-app
build-app: clean
	./scripts/build_app.sh

.PHONY: install-app
install-app: build-app
	./scripts/install_app.sh