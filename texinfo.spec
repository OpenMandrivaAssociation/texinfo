%bcond_without bootstrap
%ifnarch riscv64
%global optflags %{optflags} -rtlib=compiler-rt
%endif

Name:		texinfo
Version:	7.2
Release:	1
Summary:	Tools needed to create Texinfo format documentation files
License:	GPLv3+
Group:		Publishing
URL:		https://www.gnu.org/software/texinfo/
Source0:	https://ftp.gnu.org/gnu/texinfo/%{name}-%{version}.tar.xz
Source2:	%{name}.rpmlintrc
Patch0:		texinfo-3.12h-fix.patch
Patch2:		texinfo-4.13-vikeys-segfault-fix.patch
Patch4:		texinfo-6.7-zstd-compression.patch
# (anssi 01/2008) for make check:
%if !%{with bootstrap}
Requires:	texlive-collection-texinfo
BuildRequires:	texlive-collection-texinfo
%endif
# So configure sees iconv() works
BuildRequires:	locales-extra-charsets
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	help2man
BuildRequires:	perl-devel
BuildRequires:	perl-Storable
Requires:	texlive-tex.bin
Requires:	texlive-dehyph
Requires:	texlive-texinfo
Requires:	texlive-epsf
# Not detected by the dependency generator because these perl modules
# go to %{_datadir}/texinfo rather than a default perl directory
# (tpg) why not use: global __provides_exclude ^perl\\(.*Texinfo.*\\)$ global __requires_exclude ^perl\\(.*Texinfo.*\\)$ ?
Provides:	perl(Texinfo::Common)
Provides:	perl(Texinfo::Convert)
Provides:	perl(Texinfo::Convert::Converter)
Provides:	perl(Texinfo::Convert::DocBook)
Provides:	perl(Texinfo::Convert::HTML)
Provides:	perl(Texinfo::Convert::Info)
Provides:	perl(Texinfo::Convert::IXIN)
Provides:	perl(Texinfo::Convert::IXINSXML)
Provides:	perl(Texinfo::Convert::Line)
Provides:	perl(Texinfo::Convert::NodeNameNormalization)
Provides:	perl(Texinfo::Convert::ParagraphNonXS)
Provides:	perl(Texinfo::Convert::Paragraph)
Provides:	perl(Texinfo::Convert::PlainTexinfo)
Provides:	perl(Texinfo::Convert::Plaintext)
Provides:	perl(Texinfo::Convert::Texinfo)
Provides:	perl(Texinfo::Convert::TexinfoSXML)
Provides:	perl(Texinfo::Convert::TexinfoXML)
Provides:	perl(Texinfo::Convert::TextContent)
Provides:	perl(Texinfo::Convert::Text)
Provides:	perl(Texinfo::Convert::UnFilled)
Provides:	perl(Texinfo::Convert::Unicode)
Provides:	perl(Texinfo::Convert::XSParagraph)
Provides:	perl(Texinfo::Convert::XSParagraph::TestXS)
Provides:	perl(Texinfo::Documentlanguages)
Provides:	perl(Texinfo::Encoding)
Provides:	perl(Texinfo::MiscXS)
Provides:	perl(Texinfo::ModulePath)
Provides:	perl(Texinfo::Parser)
Provides:	perl(Texinfo::ParserNonXS)
Provides:	perl(Texinfo::Report)
Provides:	perl(Texinfo::Structuring)
Provides:	perl(Texinfo::Transformations)
Provides:	perl(Texinfo::XSLoader)

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

%description -n info
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
touch %{buildroot}%{_infodir}/dir

%find_lang %{name} --all-name

%transfiletriggerin -n info -- %{_infodir}/*.info* %{_infodir}/texinfo.*
if [ $1 -eq 1 -o $2 -eq 1 ]; then
    while [ -n "$3" ]; do
	if [ -f "$3" ]; then
	    LESSOPEN="|/usr/bin/lesspipe.sh %s" LESS_ADVANCED_PREPROCESSOR=1 less "$3" | grep -q -e INFO-DIR-SECTION && %{_bindir}/install-info "$3" --dir=%{_infodir}/dir
	fi
	shift
    done
fi

%transfiletriggerun -n info -- %{_infodir}/*.info* %{_infodir}/texinfo.*
if [ $2 -eq 0 ]; then
    while [ -n "$3" ]; do
	if [ -f "$3" ]; then
	    LESSOPEN="|/usr/bin/lesspipe.sh %s" LESS_ADVANCED_PREPROCESSOR=1 less "$3" | grep -q -e INFO-DIR-SECTION && %{_bindir}/install-info "$3" --dir=%{_infodir}/dir --remove
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
%{_infodir}/texi2any*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man1/pdftexi2dvi.1*
%{_mandir}/man1/pod2texi.1*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man1/texi2dvi.1*
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/texindex.1*
%{_mandir}/man5/texinfo.5*
%{_datadir}/texinfo
%dir %{_libdir}/texi2any
%{_libdir}/texi2any/ConvertXS.so
%{_libdir}/texi2any/DocumentXS.so
%{_libdir}/texi2any/IndicesXS.so
%{_libdir}/texi2any/MiscXS.so
%{_libdir}/texi2any/Parsetexi.so
%{_libdir}/texi2any/StructuringTransfoXS.so
%{_libdir}/texi2any/XSParagraph.so
%{_libdir}/texi2any/libtexinfo-convert.so*
%{_libdir}/texi2any/libtexinfo-convertxs.so*
%{_libdir}/texi2any/libtexinfo.so*
%{_libdir}/texi2any/libtexinfoxs.so*
%{_datadir}/texi2any

%files -n info
%{_bindir}/install-info
%{_bindir}/info
%ghost %{_infodir}/dir
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
