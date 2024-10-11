TREX_VERSION := 3.05
IMAGE_TAG := local/trex-server:latest

.PHONY: image
image: ./trex-bin
	docker build -t $(IMAGE_TAG) .

./trex-bin: ./trex-release/v$(TREX_VERSION).tar.gz
	mkdir ./trex-bin
	tar -xv --strip-components 1 -f ./trex-release/v$(TREX_VERSION).tar.gz -C ./trex-bin

./trex-release/v$(TREX_VERSION).tar.gz:
	mkdir ./trex-release
	wget --no-check-certificate --no-cache -O ./trex-release/v$(TREX_VERSION).tar.gz https://trex-tgn.cisco.com/trex/release/v$(TREX_VERSION).tar.gz
