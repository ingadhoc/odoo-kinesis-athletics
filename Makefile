all: addons

design/kinesis_athletics.xmi: design/kinesis_athletics.zargo
	-echo "REBUILD kinesis_athletics.xmi from kinesis_athletics.zargo. I cant do it"

addons: kinesis_athletics

kinesis_athletics: design/kinesis_athletics.uml
	xmi2oerp -r -i $< -t addons -v 2

clean:
	rm -rf addons/kinesis_athletics/*
	sleep 1
	touch design/kinesis_athletics.uml
