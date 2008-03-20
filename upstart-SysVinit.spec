#
# Conditional build:
%bcond_with	preconfigured
%bcond_without	selinux		# build without SELinux support
#
Summary:	System V compatibility for upstart
Summary(pl.UTF-8):	Wsparcie dla System V w upstart
Name:		upstart-SysVinit
Version:	2.86
Release:	12
License:	GPL
Group:		Base
Source0:	ftp://ftp.cistron.nl/pub/people/miquels/software/sysvinit-%{version}.tar.gz
# Source0-md5:	7d5d61c026122ab791ac04c8a84db967
Source1:	sysvinit.logrotate
Source2:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/sysvinit-non-english-man-pages.tar.bz2
# Source2-md5:	9ae8a63a4685368fae19707f95475cca
Source3:	%{name}-control-alt-delete.event
Source4:	%{name}-rc-default.event
Source5:	%{name}-rc0.event
Source6:	%{name}-rc1.event
Source7:	%{name}-rc2.event
Source8:	%{name}-rc3.event
Source9:	%{name}-rc4.event
Source10:	%{name}-rc5.event
Source11:	%{name}-rc6.event
Source12:	%{name}-rcS.event
Source13:	%{name}-sulogin.event
Source14:	%{name}-tty1.event
Source15:	%{name}-tty2.event
Source16:	%{name}-tty3.event
Source17:	%{name}-tty4.event
Source18:	%{name}-tty5.event
Source19:	%{name}-tty6.event
Patch0:		sysvinit-paths.patch
Patch1:		sysvinit-bequiet.patch
Patch2:		sysvinit-md5-bigendian.patch
Patch3:		sysvinit-wtmp.patch
Patch4:		sysvinit-man.patch
Patch6:		sysvinit-blowfish.patch
Patch7:		sysvinit-autofsck.patch
Patch8:		sysvinit-pidof.patch
Patch9:		sysvinit-killall5.patch
Patch10:	sysvinit-selinux.patch
Patch11:	sysvinit-nopowerstates-single.patch
Patch12:	sysvinit-lastlog.patch
Patch13:	sysvinit-alt-fixes.patch
%if %{with selinux}
BuildRequires:	libselinux-devel >= 1.28
BuildRequires:	libsepol-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(post):	fileutils
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	/bin/awk
Requires:	login
%if %{with preconfigured}
Requires:	logrotate
%endif
%{?with_selinux:Requires:	libselinux >= 1.18}
Requires:	mingetty
Requires:	upstart
Provides:	SysVinit = %{version}-%{release}
Provides:	group(utmp)
Obsoletes:	SysVinit
Obsoletes:	vserver-SysVinit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_eventdir	/etc/upstart/event.d
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
%setup -q -n sysvinit-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%{?with_selinux:%patch10 -p1}
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
%{__make} -C src \
	CC="%{__cc}" \
	LCRYPT="-lcrypt" \
	OPTIMIZE="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT{%{_includedir},%{_sysconfdir},/etc/logrotate.d,/var/{log,run}} \
	$RPM_BUILD_ROOT%{_eventdir}

%{__make} install -C src \
	ROOT=$RPM_BUILD_ROOT \
	BIN_OWNER=$(id -u) \
	BIN_GROUP=$(id -g)

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/sysvinit

ln -sf ../var/run/initrunlvl $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf killall5 $RPM_BUILD_ROOT%{_sbindir}/pidof

> $RPM_BUILD_ROOT/var/run/initrunlvl
> $RPM_BUILD_ROOT%{_sysconfdir}/ioctl.save
> $RPM_BUILD_ROOT/var/log/faillog
> $RPM_BUILD_ROOT/var/log/lastlog
> $RPM_BUILD_ROOT/var/log/wtmpx
> $RPM_BUILD_ROOT/var/log/btmpx

echo .so last.1 > $RPM_BUILD_ROOT%{_mandir}/man1/lastb.1
bzip2 -dc %{SOURCE2} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
rm -f $RPM_BUILD_ROOT%{_includedir}/initreq.h
rm -f $RPM_BUILD_ROOT%{_mandir}/README.sysvinit-non-english-man-pages

cp -a man/intl/* $RPM_BUILD_ROOT%{_mandir}

# remove binaries replaced by upstart
rm -f $RPM_BUILD_ROOT%{_sbindir}/{halt,init,poweroff,reboot,runlevel,shutdown,telinit}
rm -f $RPM_BUILD_ROOT%{_mandir}/*man8/{init,poweroff,runlevel,shutdown}.8*

# provide default copatibility events
install %{SOURCE3} $RPM_BUILD_ROOT%{_eventdir}/control-alt-delete
install %{SOURCE4} $RPM_BUILD_ROOT%{_eventdir}/rc-default
install %{SOURCE5} $RPM_BUILD_ROOT%{_eventdir}/rc0
install %{SOURCE6} $RPM_BUILD_ROOT%{_eventdir}/rc1
install %{SOURCE7} $RPM_BUILD_ROOT%{_eventdir}/rc2
install %{SOURCE8} $RPM_BUILD_ROOT%{_eventdir}/rc3
install %{SOURCE9} $RPM_BUILD_ROOT%{_eventdir}/rc4
install %{SOURCE10} $RPM_BUILD_ROOT%{_eventdir}/rc5
install %{SOURCE11} $RPM_BUILD_ROOT%{_eventdir}/rc6
install %{SOURCE12} $RPM_BUILD_ROOT%{_eventdir}/rcS
install %{SOURCE13} $RPM_BUILD_ROOT%{_eventdir}/sulogin
install %{SOURCE14} $RPM_BUILD_ROOT%{_eventdir}/tty1
install %{SOURCE15} $RPM_BUILD_ROOT%{_eventdir}/tty2
install %{SOURCE16} $RPM_BUILD_ROOT%{_eventdir}/tty3
install %{SOURCE17} $RPM_BUILD_ROOT%{_eventdir}/tty4
install %{SOURCE18} $RPM_BUILD_ROOT%{_eventdir}/tty5
install %{SOURCE19} $RPM_BUILD_ROOT%{_eventdir}/tty6

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

%{_eventdir}/*

%attr(755,root,root) /bin/mountpoint
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/last
%attr(755,root,root) %{_bindir}/lastb
%attr(755,root,root) %{_bindir}/mesg
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
%lang(cs) %{_mandir}/cs/man[158]/*
%lang(de) %{_mandir}/de/man[158]/*
%lang(es) %{_mandir}/es/man[158]/*
%lang(fi) %{_mandir}/fi/man[158]/*
%lang(fr) %{_mandir}/fr/man[158]/*
%lang(hu) %{_mandir}/hu/man[158]/*
%lang(id) %{_mandir}/id/man[158]/*
%lang(it) %{_mandir}/it/man[158]/*
%lang(ja) %{_mandir}/ja/man[158]/*
%lang(ko) %{_mandir}/ko/man[158]/*
%lang(pl) %{_mandir}/pl/man[158]/*
%lang(ru) %{_mandir}/ru/man[158]/*
%lang(sv) %{_mandir}/sv/man[158]/*

# devel?
#%{_includedir}/initreq.h
