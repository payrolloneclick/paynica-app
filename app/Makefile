.PHONY: clean
clean:
	rm -rf node_modules
	rm -rf coverage

.PHONY: start
start:
	yarn run start

.PHONY: lint
lint:
	yarn run lint
	yarn run pretty-quick --staged  --check

.PHONY: test
test:
	yarn run test --coverage --watchAll=false --passWithNoTests

.PHONY: remove_cache
remove_cache:
	rm -rf node_modules/.cache

.PHONY: build
build:
	NODE_ENV=production GENERATE_SOURCEMAP=false yarn run build

.PHONY: fix
fix:
	yarn run lint --fix
	yarn run pretty-quick
