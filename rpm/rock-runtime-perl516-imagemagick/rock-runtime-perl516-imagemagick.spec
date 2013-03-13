%global VER 6.7.8
%global Patchlevel 10
%global upstreamname ImageMagick

%define _prefix %{perl516_rootdir}/usr
%define perl_vendorarch %{_prefix}/lib/perl5/vendor_perl
%define _mandir %{_prefix}/man

Name:	        rock-runtime-perl516-imagemagick
Version:		%{VER}.%{Patchlevel}
Release:		1%{?dist}
Summary:		An X application for displaying and manipulating images
Group:		    Applications/Multimedia
License:		ImageMagick
Url:			http://www.imagemagick.org/
Source0:		ftp://ftp.imagemagick.org/pub/%{upstreamname}/legacy/%{upstreamname}-%{VER}-%{Patchlevel}.tar.xz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  rock-runtime-perl516-core-rpmbuild >= 5.16.2-2
BuildRequires:	bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires:	libtiff-devel, giflib-devel, zlib-devel, perl-devel >= 5.8.1
BuildRequires:	ghostscript-devel, djvulibre-devel
BuildRequires:	libwmf-devel, jasper-devel, libtool-ltdl-devel
BuildRequires:	libX11-devel, libXext-devel, libXt-devel
BuildRequires:	lcms-devel, libxml2-devel, librsvg2-devel, OpenEXR-devel
BuildRequires:  patchelf
Requires:       rock-runtime-perl516-core >= 5.16.2-2

%description
ImageMagick is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and display images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.

With perl bindings to ImageMagick.

%prep
%setup -q -n %{upstreamname}-%{VER}-%{Patchlevel}
sed -i 's/libltdl.la/libltdl.so/g' configure
iconv -f ISO-8859-1 -t UTF-8 README.txt > README.txt.tmp
touch -r README.txt README.txt.tmp
mv README.txt.tmp README.txt
# for %doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples


%build
%configure --enable-shared \
           --disable-static \
           --with-modules \
           --with-perl="%{_prefix}/bin/perl" \
           --with-x \
           --with-threads \
           --with-magick_plus_plus \
           --with-gslib \
           --with-wmf \
           --with-lcms \
           --with-rsvg \
           --with-xml \
           --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
           --without-dps \
           --without-included-ltdl --with-ltdl-include=/usr/include \
           --with-ltdl-lib=/usr/lib64
# Disable rpath
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
make


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} INSTALL="install -p"

patchelf --set-rpath %{_libdir} %{buildroot}%{perl_vendorarch}/auto/Image/Magick/Magick.so

cp -a www/source %{buildroot}%{_datadir}/doc/%{upstreamname}-%{VER}
# Delete *ONLY* _libdir/*.la files! .la files used internally to handle plugins - BUG#185237!!!
rm %{buildroot}%{_libdir}/*.la

# fix weird perl Magick.so permissions
chmod 755 %{buildroot}%{perl_vendorarch}/auto/Image/Magick/Magick.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find %{buildroot} -name "*.bs" |xargs rm -f
find %{buildroot} -name ".packlist" |xargs rm -f
find %{buildroot} -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root,-)" > perl-pkg-files
find %{buildroot}%{_prefix}/lib/perl* -type f -print \
        | sed "s@^%{buildroot}@@g" > perl-pkg-files 
find %{buildroot}%{perl_vendorarch} -type d -print \
        | sed "s@^%{buildroot}@%dir @g" \
        | grep -v '^%dir %{perl_vendorarch}$' \
        | grep -v '/auto$' >> perl-pkg-files 
if [ -z perl-pkg-files ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

# fix multilib issues
%ifarch x86_64 s390x ia64 ppc64 alpha sparc64
%define wordsize 64
%else
%define wordsize 32
%endif

mv %{buildroot}%{_includedir}/%{upstreamname}/magick/magick-config.h \
   %{buildroot}%{_includedir}/%{upstreamname}/magick/magick-config-%{wordsize}.h

cat >%{buildroot}%{_includedir}/%{upstreamname}/magick/magick-config.h <<EOF
#ifndef IMAGEMAGICK_MULTILIB
#define IMAGEMAGICK_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "magick-config-32.h"
#elif __WORDSIZE == 64
# include "magick-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

# Fonts must be packaged separately. It does nothave matter and demos work without it.
rm PerlMagick/demo/Generic.ttf

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f perl-pkg-files
%defattr(-,root,root,-)
#%doc QuickStart.txt ChangeLog Platforms.txt
#%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt
#%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt
%{_libdir}/libMagickCore.so.5*
%{_libdir}/libMagickWand.so.5*
%{_bindir}/[a-z]*
%{_libdir}/%{upstreamname}-%{VER}
%{_datadir}/%{upstreamname}-%{VER}
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{upstreamname}.*
%{_mandir}/man3/*

%exclude %{_libdir}/%{upstreamname}-%{VER}/modules-Q16/coders/djvu.*
%exclude %{_sysconfdir}/%{upstreamname}
%exclude %{_bindir}/MagickCore-config
%exclude %{_bindir}/Magick-config
%exclude %{_bindir}/MagickWand-config
%exclude %{_bindir}/Wand-config
%exclude %{_libdir}/libMagickCore.so
%exclude %{_libdir}/libMagickWand.so
%exclude %{_libdir}/pkgconfig/MagickCore.pc
%exclude %{_libdir}/pkgconfig/ImageMagick.pc
%exclude %{_libdir}/pkgconfig/MagickWand.pc
%exclude %{_libdir}/pkgconfig/Wand.pc
%exclude %{_includedir}/%{upstreamname}
%exclude %{_mandir}/man1/Magick-config.*
%exclude %{_mandir}/man1/MagickCore-config.*
%exclude %{_mandir}/man1/Wand-config.*
%exclude %{_mandir}/man1/MagickWand-config.*
%exclude %{_datadir}/doc/%{upstreamname}-%{VER}
%exclude %{_libdir}/libMagick++.so.5*
%exclude %{_bindir}/Magick++-config
%exclude %{_includedir}/%{upstreamname}/Magick++
%exclude %{_includedir}/%{upstreamname}/Magick++.h
%exclude %{_libdir}/libMagick++.so
%exclude %{_libdir}/pkgconfig/Magick++.pc
%exclude %{_libdir}/pkgconfig/ImageMagick++.pc
%exclude %{_mandir}/man1/Magick++-config.*

%changelog
* Tue Mar 12 2013 Eric Waters <ewaters@shutterstock.com> - 6.7.8.9-6
- Stuff
