TEST_FILES=test/*

default:
	./run.sh
docs:
	mkdir -p documentation
	rm -f documentation/*.html
	pydoc -w ./ > documentation/log.txt
	mv *.html documentation
	rm -f OpenRPG/*.pyc
test:
	./runTests.sh
	rm -rf tmp
