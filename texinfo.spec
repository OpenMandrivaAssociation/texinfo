%bcond_with	bootstrap

Name:		texinfo
Version:	4.13a
Release:	7
Summary:	Tools needed to create Texinfo format documentation files
License:	GPLv3+
Group:		Publishing
URL:		http://www.gnu.org/software/texinfo/
Source0:	ftp://ftp.gnu.org/pub/gnu/texinfo/%{name}-%{version}.tar.lzma
Source2:	%{name}.rpmlintrc
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
BuildRequires:	help2man

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
Requires:	xz
Requires(pre):	coreutils
# explicit file provides
Provides:	/sbin/install-info
%rename		info-install

%description -n	info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a valuable
source of information about the software on your system.

%prep
%setup -qn %{name}-4.13
%apply_patches

%build
%configure2_5x	--disable-rpath
%make 
%make -C util

%check
# all tests must pass
make check

%install
%makeinstall_std
touch %{buildroot}%{_infodir}/dir
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin/install-info

%find_lang %{name}

%pre -n info
if [ -f %{_sysconfdir}/info-dir -a -L %{_infodir}/dir ]; then
    mv %{_sysconfdir}/info-dir %{_infodir}/dir 
fi

%triggerin -n info -- %{_infodir}/*.info*, %{_infodir}/texinfo.*
if [ $1 -eq 0 -o $2 -eq 0 ]; then
    while [ -n "$3" ]; do
	if [ -f "$3" ]; then
	    %__install_info $3 --dir=%{_infodir}/dir
	fi
	shift
    done
fi

%triggerun -n info -- %{_infodir}/*.info*, %{_infodir}/texinfo.*
if [ $2 -eq 0 ]; then
    while [ -n "$3" ]; do
	if [ -f "$3" ]; then
	    %__install_info $3 --dir=%{_infodir}/dir --remove
	fi
	shift
    done
fi

%files -f %{name}.lang
%doc AUTHORS INTRODUCTION NEWS README TODO
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
%doc info/README
/sbin/install-info
%{_bindir}/info
%{_bindir}/infokey
%ghost %{_infodir}/dir
%{_infodir}/info.info*
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
