#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
#
Summary:	System V compatibility for upstart
Summary(pl.UTF-8):	Wsparcie dla System V w upstart
Name:		upstart-SysVinit
Version:	2.88
Release:	1
License:	GPL
Group:		Base
Source0:	http://download.savannah.gnu.org/releases/sysvinit/sysvinit-%{version}dsf.tar.bz2
# Source0-md5:	6eda8a97b86e0a6f59dabbf25202aa6f
Source1:	sysvinit.logrotate
Patch0:         sysvinit-paths.patch
Patch1:         sysvinit-bequiet.patch
Patch2:         sysvinit-wtmp.patch
Patch3:         sysvinit-man.patch
Patch4:         sysvinit-halt.patch
Patch5:         sysvinit-autofsck.patch
Patch6:         sysvinit-pidof.patch
Patch7:         sysvinit-killall5.patch
Patch8:         sysvinit-nopowerstates-single.patch
Patch9:         sysvinit-lastlog.patch
Patch10:        sysvinit-alt-fixes.patch
Patch11:        sysvinit-quiet.patch
Patch12:        sysvinit-rebootconfirmation.patch
%if %{with selinux}
BuildRequires:	libselinux-devel >= 1.28
BuildRequires:	libsepol-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	/bin/awk
Requires:	grep
%{?with_selinux:Requires:	libselinux >= 1.18}
Requires:	login
Requires:	mingetty
Requires:	sed
Requires:	upstart >= 0.6
Requires:	util-linux >= 2.20-5
Provides:	SysVinit = %{version}-%{release}
Provides:	group(utmp)
Obsoletes:	SysVinit
Obsoletes:	vserver-SysVinit
Conflicts:	rc-scripts < 0.4.5.1-6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		eventdir	/etc/init
%define		_sbindir	/sbin
# as in original flags
%define		specflags	-fomit-frame-pointer

%description
The SysVinit package contains a group of processes that control the
very basic functions of your system. SysVinit includes the init
program, the first program started by the Linux kernel when the system
boots. Init then controls the startup, running and shutdown of all
other programs.

%description -l de.UTF-8
SysVinit ist das erste Programm, das beim Systemstart vom Linux-Kernel
gestartet wird. Es steuert das Starten, Ausführen und Beenden aller
anderen Programme.

%description -l es.UTF-8
SysVinit es el primer programa ejecutado por el kernel Linux cuando se
inicia el sistema. Controla arranque, funcionamiento y cierre de todos
los otros programas.

%description -l fr.UTF-8
SysVinit est le premier programme exécuté par le noyau de Linux
lorsque le système démarre, il contrôle le lancement, l'exécution et
l'arrêt de tous les autres programmes.

%description -l pl.UTF-8
SysVinit jest pierwszym programem uruchamianym przez jądro podczas
startu systemu. Kontroluje start, pracę oraz zamykanie wszystkich
innych programów.

%description -l pt_BR.UTF-8
SysVinit é o primeiro programa executado pelo kernel Linux quando o
sistema é inicializado. Controla inicialização, funcionamento e
finalização de todos os outros programas.

%description -l ru.UTF-8
Пакет SysVinit содержит группу процессов, которые управляют самыми
базовыми функциями вашей системы. SysVinit включает программу init,
самую первую программу, которая запускается ядром Linux при загрузке
системы. После этого init управляет запуском, исполнением и остановом
всех остальных программ.

%description -l tr.UTF-8
SysVinit, sistem açılırken Linux çekirdeği tarafından çalıştırılan ilk
programdır. Diğer programların başlamalarını, çalışmalarını ve
sonlanmalarını sağlar/denetler.

%description -l uk.UTF-8
Пакет SysVinit містить групу процесів, котрі керують самими базовими
функціями вашої системи. SysVinit містить програму init, першу
програму, яку запускає ядро Linux під час загрузки системи. Після
цього init керує запуском, виконанням та зупинкою всіх інших програм.

%prep
%setup -q -n sysvinit-%{version}dsf
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p0

%build
%{__make} -C src \
	%{?with_selinux:WITH_SELINUX=yes} \
	CC="%{__cc}" \
	LCRYPT="-lcrypt" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT{%{_includedir},%{_sysconfdir},/etc/logrotate.d,/var/{log,run}} \
	$RPM_BUILD_ROOT%{eventdir}

%{__make} install -C src \
	ROOT=$RPM_BUILD_ROOT \
	BIN_OWNER=$(id -u) \
	BIN_GROUP=$(id -g)

cp -a %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/sysvinit

ln -sf ../var/run/initrunlvl $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf killall5 $RPM_BUILD_ROOT%{_sbindir}/pidof
ln -s utmpdump $RPM_BUILD_ROOT%{_bindir}/utmpx-dump

> $RPM_BUILD_ROOT/var/run/initrunlvl
> $RPM_BUILD_ROOT%{_sysconfdir}/ioctl.save
> $RPM_BUILD_ROOT/var/log/faillog
> $RPM_BUILD_ROOT/var/log/lastlog
> $RPM_BUILD_ROOT/var/log/wtmpx
> $RPM_BUILD_ROOT/var/log/btmpx

echo .so last.1 > $RPM_BUILD_ROOT%{_mandir}/man1/lastb.1
echo .so utmpdump.1 > $RPM_BUILD_ROOT%{_mandir}/man1/utmpx-dump.1
rm $RPM_BUILD_ROOT%{_includedir}/initreq.h

# remove binaries replaced by upstart
rm $RPM_BUILD_ROOT%{_sbindir}/{halt,init,poweroff,reboot,runlevel,shutdown,telinit}
rm $RPM_BUILD_ROOT%{_mandir}/*man8/{init,poweroff,reboot,runlevel,shutdown,telinit}.8*
rm $RPM_BUILD_ROOT%{_mandir}/*man5/inittab.5*
# in util-linux
rm $RPM_BUILD_ROOT{/bin/mountpoint,%{_mandir}/man1/mountpoint.1*}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 22 utmp

%post
touch %{_sysconfdir}/ioctl.save /var/log/{{fail,last}log,btmpx}
chmod 000 %{_sysconfdir}/ioctl.save /var/log/{fail,last}log
chown root:root %{_sysconfdir}/ioctl.save /var/log/faillog
chown root:utmp /var/log/lastlog
chmod 600 %{_sysconfdir}/ioctl.save
chmod 640 /var/log/faillog
chmod 660 /var/log/lastlog
chmod 640 /var/log/btmpx

%postun
if [ "$1" = "0" ]; then
	%groupremove utmp
fi

%files
%defattr(644,root,root,755)
%doc doc/{Propaganda,Changelog,*.lsm}
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/last
%attr(755,root,root) %{_bindir}/lastb
%attr(755,root,root) %{_bindir}/mesg
%attr(755,root,root) %{_bindir}/utmpdump
%attr(755,root,root) %{_bindir}/utmpx-dump
%attr(2755,root,tty) %{_bindir}/wall

%attr(640,root,root) /etc/logrotate.d/sysvinit
%ghost %{_sysconfdir}/initrunlvl
%ghost /var/run/initrunlvl
%attr(600,root,root) %ghost %{_sysconfdir}/ioctl.save
%attr(640,root,root) %ghost /var/log/faillog
%attr(660,root,utmp) %ghost /var/log/lastlog
%attr(664,root,utmp) %ghost /var/log/wtmpx
%attr(640,root,root) %ghost /var/log/btmpx

%{_mandir}/man[158]/*

# devel?
#%{_includedir}/initreq.h
