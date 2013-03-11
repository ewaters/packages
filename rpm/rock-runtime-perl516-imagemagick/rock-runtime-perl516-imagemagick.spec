%filter_from_provides /.*/d
%filter_from_requires /^perl.*/d
%filter_setup

Name:           rock-runtime-perl516-imagemagick
Version:        6.8.3
Release:        1%{?dist}

Summary:        Use ImageMagick to convert, edit, or compose bitmap images in a variety of formats.  In addition resize, rotate, shear, distort and transform images.
Group:          Applications/Multimedia
License:        http://www.imagemagick.org/script/license.php
Url:            http://www.imagemagick.org/
Source0:        http://www.imagemagick.org/download/ImageMagick-6.8.3-9.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  rock-runtime-perl516-core-rpmbuild >= 5.12.2-2
BuildRequires:  bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires:  libtiff-devel, giflib-devel, zlib-devel
BuildRequires:  ghostscript-devel, djvulibre-devel
BuildRequires:  libwmf-devel, jasper-devel, libtool-ltdl-devel
BuildRequires:  libX11-devel, libXext-devel, libXt-devel
BuildRequires:  lcms-devel, libxml2-devel, librsvg2-devel, OpenEXR-devel
Requires:       rock-runtime-perl516-core >= 5.12.2-2

%description
ImageMagick is a software suite to create, edit, and compose bitmap images. It
can read, convert and write images in a variety of formats (about 100)
including DPX, GIF, JPEG, JPEG-2000, PDF, PhotoCD, PNG, Postscript, SVG,
and TIFF. Use ImageMagick to translate, flip, mirror, rotate, scale, shear
and transform images, adjust image colors, apply various special effects,
or draw text, lines, polygons, ellipses and Bézier curves.

The functionality of ImageMagick is typically utilized from the command line
or you can use the features from programs written in your favorite programming
language. Choose from these interfaces: G2F (Ada), MagickCore (C), MagickWand
(C), ChMagick (Ch), Magick++ (C++), JMagick (Java), L-Magick (Lisp), nMagick
(Neko/haXe), PascalMagick (Pascal), PerlMagick (Perl), MagickWand for PHP
(PHP), PythonMagick (Python), RMagick (Ruby), or TclMagick (Tcl/TK). With a
language interface, use ImageMagick to modify or create images automagically
and dynamically.

ImageMagick is free software delivered as a ready-to-run binary distribution
or as source code that you may freely use, copy, modify, and distribute in
both open and proprietary applications. It is distributed under an Apache
2.0-style license, approved by the OSI.

The ImageMagick development process ensures a stable API and ABI. Before
each ImageMagick release, we perform a comprehensive security assessment that
includes memory and thread error detection to help prevent exploits.ImageMagick
is free software delivered as a ready-to-run binary distribution or as source
code that you may freely use, copy, modify, and distribute in both open and
proprietary applications. It is distributed under an Apache 2.0-style license,
approved by the OSI.

%prep

%build

%configure --enable-shared \
	--prefix %{perl516_rootdir}%{_prefix} \
	--with-perl \
	--with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'"

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} INSTALL="install -p"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%defattr(-,root,root,-)
%doc QuickStart.txt ChangeLog Platforms.txt
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt
%{_libdir}/libMagickCore*so*
%{_libdir}/libMagickWand*so*
%{_bindir}/[a-z]*
%{_libdir}/%{name}-%{VERSION}
%{_datadir}/%{name}-%{MAJOR_VERSION}
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*
%exclude %{_libdir}/%{name}-%{VERSION}/modules-*/coders/djvu.*
%{_sysconfdir}/%{name}-%{MAJOR_VERSION}

%changelog
* Mon Mar 11 2013 Eric Waters <ewaters@gmail.com> - 6.8.3-1
- Initial build
