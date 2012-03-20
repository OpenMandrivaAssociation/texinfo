%bcond_with	bootstrap

Name:		texinfo
Version:	4.13a
Release:	6
Summary:	Tools needed to create Texinfo format documentation files
License:	GPL
Group:		Publishing
URL:		http://www.gnu.org/software/texinfo/
Source0:	ftp://ftp.gnu.org/pub/gnu/texinfo/%{name}-%{version}.tar.lzma
Source1:	info-dir
Patch1:		texinfo-3.12h-fix.patch
Patch2:		texinfo-4.13-test.patch
Patch3:		texinfo-4.13-fix-crash-used-parallel.patch
Patch107:	texinfo-4.13-vikeys-segfault-fix.patch
Patch108:	texinfo-4.13-xz.patch
# backported from cvs
Patch109:	texinfo-4.13-use-size_t-for-len.patch
# Local fixes submitted upstream
Patch200:	texinfo-4.13-mb_modeline.patch
# (anssi 01/2008) for make check:
%if !%{with bootstrap}
Requires:	texlive-collection-texinfo
BuildRequires:	texlive-collection-texinfo
%endif
BuildRequires:	ncurses-devel
BuildRequires:	zlib-devel
BuildRequires:	help2man
Requires(pre):	info-install
Requires(preun):info-install

%description
Texinfo is a documentation system that can produce both online information
and printed output from a single source file.  Normally, you'd have to
write two separate documents: one for online help or other online
information and the other for a typeset manual or other printed work.
Using Texinfo, you only need to write one source document.  Then when the
work needs revision, you only have to revise one source document.  The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you are
going to write documentation for the GNU Project.

%package -n	info
Summary:	A stand-alone TTY-based reader for GNU texinfo documentation
Group:		System/Base
Requires(pre):	info-install
Requires(preun):info-install

%description -n	info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a valuable
source of information about the software on your system.

%package -n	info-install
Summary:	Program to update the GNU texinfo documentation main page
Group:		System/Base
Requires:	xz
# explicit file provides
Provides:	/sbin/install-info

%description -n	info-install
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

%prep
%setup -qn %{name}-4.13
%apply_patches

%build
%configure2_5x	--disable-rpath

%make 
rm -f util/install-info
%make -C util LIBS=%{_libdir}/libz.a

%check
# all tests must pass
make check

%install
%makeinstall_std
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/info-dir
rm -f %{buildroot}%{_infodir}/dir
ln -s ../../..%{_sysconfdir}/info-dir %{buildroot}%{_infodir}/dir
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin/install-info
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmconfig

%find_lang %{name}

%post
if [ -f %{_infodir}/texinfo.xz ]; then # --excludedocs?
%_install_info %{name} || :
fi

%preun
if [ $1 = 0 ]; then
	if [ -f %{_infodir}/texinfo.xz ]; then # --excludedocs?
%_remove_install_info %{name} || :
	fi
fi

%post -n info
if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
%_install_info info.info
fi
if [ -x /bin/sed ]; then
/bin/sed -i '/^This is.*produced by makeinfo.*from/d' %{_infodir}/dir || :
fi

%preun -n info
if [ $1 = 0 ]; then
	if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
%_remove_install_info info.info || :
	fi
fi

%files -f %{name}.lang
%doc AUTHORS INTRODUCTION NEWS README TODO
%doc --parents info/README
%{_bindir}/makeinfo
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/pdftexi2dvi
%{_infodir}/info-stnd.info*
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man1/pdftexi2dvi.1*
%{_mandir}/man1/texi2dvi.1*                         
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/texindex.1*
%{_mandir}/man5/texinfo.5*   
%{_datadir}/texinfo

%files -n info
%{_bindir}/info
%{_infodir}/info.info*
%{_bindir}/infokey

%files -n info-install
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/info-dir
%{_infodir}/dir
/sbin/install-info
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
