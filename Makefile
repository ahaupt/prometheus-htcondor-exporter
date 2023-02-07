NAME	    = prometheus-htcondor-exporter
VERSION	    = $(shell cat VERSION)

DESTDIR	   ?= /
SBINDIR    ?= /usr/sbin
SYSTEMDDIR ?= /usr/lib/systemd/system

install:
	mkdir -p $(DESTDIR)$(SBINDIR)
	sed -e 's@__sbindir__@$(SBINDIR)@' src/htcondor-exporter-daemon > $(DESTDIR)$(SBINDIR)/htcondor-exporter-daemon
	sed -e 's@__sbindir__@$(SBINDIR)@' src/htcondor-exporter > $(DESTDIR)$(SBINDIR)/htcondor-exporter
	chmod +x $(DESTDIR)$(SBINDIR)/{htcondor-exporter,htcondor-exporter-daemon}

	mkdir -p $(DESTDIR)$(SYSTEMDDIR)
	sed -e 's@__sbindir__@$(SBINDIR)@' src/htcondor-exporter.service > $(DESTDIR)$(SYSTEMDDIR)/htcondor-exporter.service
	chmod +r $(DESTDIR)$(SYSTEMDDIR)/htcondor-exporter.service

rpm: dist
	rpmbuild -D '_sourcedir .' -ta $(NAME)-$(VERSION).tar.gz

dist:
	$(eval TMPSPECFILE = $(shell mktemp))
	sed -e 's@__NAME__@$(NAME)@' -e 's@__VERSION__@$(VERSION)@' -e 's@__SBINDIR__@$(SBINDIR)@' -e 's@__SYSTEMDDIR__@$(SYSTEMDDIR)@' rpm/$(NAME).spec > $(TMPSPECFILE)
	chmod +r $(TMPSPECFILE)
	tar -cz --transform 's@^\(.\)@$(NAME)-$(VERSION)/\1@' --transform 's@$(TMPSPECFILE)@/$(NAME).spec@' --exclude-backups --exclude-from=.gitignore -f $(NAME)-$(VERSION).tar.gz src/* Makefile $(TMPSPECFILE)
	rm -f $(TMPSPECFILE)

