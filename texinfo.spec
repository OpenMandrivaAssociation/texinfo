%bcond_with bootstrap
%global optflags %{optflags} -rtlib=compiler-rt

Name:		texinfo
Version:	6.5
Release:	1
Summary:	Tools needed to create Texinfo format documentation files
License:	GPLv3+
Group:		Publishing
URL:		http://www.gnu.org/software/texinfo/
Source0:	ftp://ftp.gnu.org/pub/gnu/texinfo/%{name}-%{version}.tar.xz
Source2:	%{name}.rpmlintrc
Patch1:		texinfo-3.12h-fix.patch
Patch2:		texinfo-6.5-clang.patch
Patch107:	texinfo-4.13-vikeys-segfault-fix.patch
# (anssi 01/2008) for make check:
%if !%{with bootstrap}
Requires:	texlive-collection-texinfo
BuildRequires:	texlive-collection-texinfo
%endif
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	help2man
BuildRequires:	perl-devel

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
Requires:	coreutils
Requires:	grep
Requires:	less
Requires:	xz
%rename		info-install

%description -n	info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a valuable
source of information about the software on your system.

%prep
%autosetup -p1

%build
%configure
%make_build
%make -C util

%check
# all tests must pass
make check

%install
%make_install
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin
touch %{buildroot}%{_infodir}/dir

%find_lang %{name} --all-name

%transfiletriggerin -n info -- %{_infodir}/*.info* %{_infodir}/texinfo.*
if [ $1 -eq 1 -o $2 -eq 1 ]; then
    while [ -n "$3" ]; do
	if [ -f "$3" ]; then
	    LESSOPEN="|/usr/bin/lesspipe.sh %s" LESS_ADVANCED_PREPROCESSOR=1 less "$3" | grep -q -e INFO-DIR-SECTION && /sbin/install-info "$3" --dir=%{_infodir}/dir
	fi
	shift
    done
fi

%transfiletriggerun -n info -- %{_infodir}/*.info* %{_infodir}/texinfo.*
if [ $2 -eq 0 ]; then
    while [ -n "$3" ]; do
	if [ -f "$3" ]; then
	    LESSOPEN="|/usr/bin/lesspipe.sh %s" LESS_ADVANCED_PREPROCESSOR=1 less "$3" | grep -q -e INFO-DIR-SECTION && /sbin/install-info "$3" --dir=%{_infodir}/dir --remove
	fi
	shift
    done
fi

%files -f %{name}.lang
%doc AUTHORS NEWS README TODO
%{_bindir}/makeinfo
%{_bindir}/pdftexi2dvi
%{_bindir}/pod2texi
%{_bindir}/texindex
%{_bindir}/texi2any
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_infodir}/info-stnd.info*
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man1/pdftexi2dvi.1*
%{_mandir}/man1/pod2texi.1*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man1/texi2dvi.1*
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/texindex.1*
%{_mandir}/man5/texinfo.5*   
%{_datadir}/texinfo
%dir %{_libdir}/texinfo
%{_libdir}/texinfo/XSParagraph.so
%{_libdir}/texinfo/MiscXS.so

%files -n info
/sbin/install-info
%{_bindir}/info
%ghost %{_infodir}/dir
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
