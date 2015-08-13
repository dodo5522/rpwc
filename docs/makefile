PLANTUML := plantuml.jar
CONFIG := plantuml_config.txt
DEPEND_FILES := makefile $(PLANTUML) $(CONFIG)

define SHOW_IMAGE
$(shell \
	if [ -z "$(BUILD_ENV)" ]; then \
		OS=`uname`; \
		if [ "$${OS}" = 'Darwin' ]; then \
			open $1; \
		elif [ "$${OS}" = 'Linux' ]; then \
			gnome-open $1; \
		fi; \
	fi)
endef

.PHONY:all

all:sequence.png
	$(call SHOW_IMAGE,$<)

%.png:%.uml $(DEPEND_FILES)
	java -jar $(PLANTUML) -config $(CONFIG) $<

.PHONY:clean

clean:
	rm -f *.png
