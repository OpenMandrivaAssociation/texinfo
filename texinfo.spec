%define name	texinfo
%define version	4.13
%define release	%mkrel 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Tools needed to create Texinfo format documentation files
License:	GPL
Group:		Publishing
URL:		http://www.texinfo.org/
Source0:	ftp://ftp.gnu.org/pub/gnu/texinfo/%{name}-%{version}.tar.lzma
Source1:	info-dir
Patch1:		texinfo-3.12h-fix.patch
Patch2:		texinfo-4.13-test.patch
Patch107:	texinfo-4.13-vikeys-segfault-fix.patch
Patch108:	texinfo-4.13-xz.patch
Requires:	texmf-data
# (anssi 01/2008) for make check:
BuildRequires:	tetex
BuildRequires:	tetex-latex
BuildRequires:	ncurses-devel
BuildRequires:	zlib-devel
Requires(pre):	info-install
Requires(preun):	info-install
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n info
Summary:	A stand-alone TTY-based reader for GNU texinfo documentation
Group:		System/Base
Requires(pre):	info-install
Requires(preun):	info-install

%description -n	info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a valuable
source of information about the software on your system.

%package -n info-install
Summary:	Program to update the GNU texinfo documentation main page
Group:		System/Base
Requires:	lzma
# explicit file provides
Provides:	/sbin/install-info

%description -n	info-install
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

%prep
%setup -q
%patch1 -p1
%patch2 -p1 -b .test~
#%%patch5 -p1 -b .test
%patch107 -p1
%patch108 -p1 -b .xz~

%build
%configure2_5x \
	--disable-rpath

%make 
rm -f util/install-info
%make -C util LIBS=%{_libdir}/libz.a

%check
# all tests must pass
make check

%install
rm -rf %{buildroot}

%makeinstall_std
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/info-dir
ln -s ../../..%{_sysconfdir}/info-dir %{buildroot}%{_infodir}/dir
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin/install-info
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmconfig

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%_install_info %{name}

%preun
%_remove_install_info %{name}

%post -n info
%_install_info info.info

%preun -n info
%_remove_install_info info.info

%files -f %{name}.lang
%defattr(-,root,root)
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
%defattr(-,root,root)
%{_bindir}/info
%{_infodir}/info.info*
%{_bindir}/infokey

%files -n info-install
%defattr(-,root,root)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/info-dir
%{_infodir}/dir
/sbin/install-info
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
