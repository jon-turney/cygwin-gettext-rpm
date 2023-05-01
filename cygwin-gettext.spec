%{?cygwin_package_header}

Name:      cygwin-gettext
Version:   0.19.8.1
Release:   2%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/gettext/
BuildArch: noarch

Source0:   http://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.xz
Patch0:    gettext-0.18.1.1-autopoint-V.patch
Patch1:    gettext-0.19.3-localename.patch
Patch2:    gettext-0.19.8.1-no-woe32dll.patch
Patch3:    gettext-0.19.8.1-cygwin-ftm.patch
Patch4:    gettext-0.19.8.1-have_wprintf.patch

BuildRequires: make
BuildRequires: autoconf automake cygwin-libtool-base
BuildRequires: cygwin32-filesystem >= 10
BuildRequires: cygwin32-gcc
BuildRequires: cygwin32-gcc-c++
BuildRequires: cygwin32-binutils
BuildRequires: cygwin32
BuildRequires: cygwin32-libiconv

BuildRequires: cygwin64-filesystem >= 10
BuildRequires: cygwin64-gcc
BuildRequires: cygwin64-gcc-c++
BuildRequires: cygwin64-binutils
BuildRequires: cygwin64
BuildRequires: cygwin64-libiconv

%description
Gettext libraries for Cygwin toolchains.

%package -n cygwin32-gettext
Summary:        Gettext libraries for Cygwin32 toolchain
Group:          Development/Libraries

%description -n cygwin32-gettext
Gettext library for the Cygwin i686 toolchain.

%package -n cygwin32-gettext-static
Summary:        Static version of the Cygwin32 Gettext library
Group:          Development/Libraries
Requires:       cygwin32-gettext = %{version}-%{release}
Requires:       cygwin32-libiconv-static

%description -n cygwin32-gettext-static
Static version of the Gettext library for the Cygwin i686 toolchain.

%package -n cygwin64-gettext
Summary:        Gettext libraries for Cygwin64 toolchain
Group:          Development/Libraries

%description -n cygwin64-gettext
Gettext library for the Cygwin x86_64 toolchain.

%package -n cygwin64-gettext-static
Summary:        Static version of the Cygwin64 Gettext library
Group:          Development/Libraries
Requires:       cygwin64-gettext = %{version}-%{release}
Requires:       cygwin64-libiconv-static

%description -n cygwin64-gettext-static
Static version of the Gettext library for the Cygwin x86_64 toolchain.

%{?cygwin_debug_package}


%prep
%setup -q -n gettext-%{version}
%patch0 -p2
%patch1 -p2
%patch2 -p2
%patch3 -p2
%patch4 -p2

rm -f m4/libtool.m4 gettext-tools/gnulib-m4/openmp.m4
touch m4/libtool.m4 gettext-tools/gnulib-m4/openmp.m4
cygwin-libtoolize --copy --force
GNULIB_TOOL=: ./autogen.sh --skip-gnulib


%build
# gnulib uses many AC_TRY_RUN/AC_RUN_IFELSE tests, but assumes functions
# are broken when cross-compiling and tries replacing them, eventually leading
# to compile errors in gettext-tools. The correct values below are based on
# comparison with a Cygwin-native build.
%cygwin_configure \
  --disable-java \
  --disable-native-java \
  --disable-csharp \
  --enable-static --enable-shared \
  --enable-threads=posix \
  --without-emacs \
  --with-included-glib \
  --with-included-libcroco \
  --with-included-libunistring \
  --with-included-libxml \
  --without-libiconv-prefix \
  ac_cv_func_lstat_dereferences_slashed_symlink=yes \
  am_cv_func_iconv_works=yes \
  gl_cv_cc_visibility=no \
  gl_cv_header_working_fcntl_h=yes \
  gl_cv_func_btowc_eof=yes \
  gl_cv_func_btowc_nul=yes \
  gl_cv_func_dup2_works=yes \
  gl_cv_func_fcntl_f_dupfd_works=yes \
  gl_cv_func_fnmatch_posix=yes \
  gl_cv_func_fopen_slash=yes \
  gl_cv_func_working_getdelim=yes \
  gl_cv_func_getopt_posix=yes \
  gl_cv_func_gettimeofday_clobber=no \
  gl_cv_func_mbrtowc_incomplete_state=yes \
  gl_cv_func_mbrtowc_null_arg=yes \
  gl_cv_func_mbrtowc_retval=yes \
  gl_cv_func_mbsrtowcs_works=yes \
  gl_cv_func_memchr_works=yes \
  gl_cv_func_open_slash=yes \
  gl_cv_func_readlink_works=yes \
  gl_cv_func_rmdir_works=yes \
  gt_cv_func_printf_posix=yes \
  gl_cv_func_setenv_works=yes \
  gl_cv_func_snprintf_retval_c99=yes \
  gl_cv_func_snprintf_size1=yes \
  gl_cv_func_stat_dir_slash=yes \
  gl_cv_func_stat_file_slash=yes \
  gl_cv_func_stpncpy=yes \
  gl_cv_func_strstr_linear=yes \
  gl_cv_func_svid_putenv=yes \
  gl_cv_func_symlink_works=yes \
  gl_cv_func_unsetenv_works=yes \
  gl_cv_func_wcrtomb_retval=yes \
  gl_cv_func_wctob_works=yes \
  gl_cv_func_wcwidth_works=yes \
  gl_cv_have_weak=no \
  gt_cv_int_divbyzero_sigfpe=yes

%cygwin_make %{?_smp_mflags}


%install
%cygwin_make install DESTDIR=$RPM_BUILD_ROOT

# Runtime data files
rm -f $RPM_BUILD_ROOT%{cygwin32_datadir}/locale/locale.alias
rm -f $RPM_BUILD_ROOT%{cygwin32_libdir}/charset.alias

rm -f $RPM_BUILD_ROOT%{cygwin64_datadir}/locale/locale.alias
rm -f $RPM_BUILD_ROOT%{cygwin64_libdir}/charset.alias

# This documentation is available in base gettext-devel.
rm -rf $RPM_BUILD_ROOT%{cygwin32_docdir}
rm -rf $RPM_BUILD_ROOT%{cygwin32_infodir}
rm -rf $RPM_BUILD_ROOT%{cygwin32_mandir}

rm -rf $RPM_BUILD_ROOT%{cygwin64_docdir}
rm -rf $RPM_BUILD_ROOT%{cygwin64_infodir}
rm -rf $RPM_BUILD_ROOT%{cygwin64_mandir}

# Remove unnecessary Cygwin native binaries and their dependencies
rm -f $RPM_BUILD_ROOT%{cygwin32_bindir}/*.exe
rm -f $RPM_BUILD_ROOT%{cygwin32_bindir}/gettext.sh
rm -f $RPM_BUILD_ROOT%{cygwin32_bindir}/cyggettextlib-*.dll
rm -f $RPM_BUILD_ROOT%{cygwin32_bindir}/cyggettextsrc-*.dll
rm -f $RPM_BUILD_ROOT%{cygwin32_libdir}/libgettextlib.*
rm -f $RPM_BUILD_ROOT%{cygwin32_libdir}/libgettextsrc.*
rm -fr $RPM_BUILD_ROOT%{cygwin32_libdir}/gettext/
rm -fr $RPM_BUILD_ROOT%{cygwin32_datadir}/gettext-*/

rm -f $RPM_BUILD_ROOT%{cygwin64_bindir}/*.exe
rm -f $RPM_BUILD_ROOT%{cygwin64_bindir}/gettext.sh
rm -f $RPM_BUILD_ROOT%{cygwin64_bindir}/cyggettextlib-*.dll
rm -f $RPM_BUILD_ROOT%{cygwin64_bindir}/cyggettextsrc-*.dll
rm -f $RPM_BUILD_ROOT%{cygwin64_libdir}/libgettextlib.*
rm -f $RPM_BUILD_ROOT%{cygwin64_libdir}/libgettextsrc.*
rm -fr $RPM_BUILD_ROOT%{cygwin64_libdir}/gettext/
rm -fr $RPM_BUILD_ROOT%{cygwin64_datadir}/gettext-*/

# We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -name '*.la' -delete

%cygwin_find_lang gettext --all-name


%files -n cygwin32-gettext -f cygwin32-gettext.lang
%doc COPYING
%{cygwin32_bindir}/autopoint
%{cygwin32_bindir}/gettextize
%{cygwin32_bindir}/cygasprintf-0.dll
%{cygwin32_bindir}/cyggettextpo-0.dll
%{cygwin32_bindir}/cygintl-8.dll
%{cygwin32_includedir}/autosprintf.h
%{cygwin32_includedir}/gettext-po.h
%{cygwin32_includedir}/libintl.h
%{cygwin32_libdir}/libasprintf.dll.a
%{cygwin32_libdir}/libgettextpo.dll.a
%{cygwin32_libdir}/libintl.dll.a
%{cygwin32_datadir}/aclocal/*m4
%{cygwin32_datadir}/gettext/

%files -n cygwin32-gettext-static
%{cygwin32_libdir}/libasprintf.a
%{cygwin32_libdir}/libgettextpo.a
%{cygwin32_libdir}/libintl.a

%files -n cygwin64-gettext -f cygwin64-gettext.lang
%doc COPYING
%{cygwin64_bindir}/autopoint
%{cygwin64_bindir}/gettextize
%{cygwin64_bindir}/cygasprintf-0.dll
%{cygwin64_bindir}/cyggettextpo-0.dll
%{cygwin64_bindir}/cygintl-8.dll
%{cygwin64_includedir}/autosprintf.h
%{cygwin64_includedir}/gettext-po.h
%{cygwin64_includedir}/libintl.h
%{cygwin64_libdir}/libasprintf.dll.a
%{cygwin64_libdir}/libgettextpo.dll.a
%{cygwin64_libdir}/libintl.dll.a
%{cygwin64_datadir}/aclocal/*m4
%{cygwin64_datadir}/gettext/

%files -n cygwin64-gettext-static
%{cygwin64_libdir}/libasprintf.a
%{cygwin64_libdir}/libgettextpo.a
%{cygwin64_libdir}/libintl.a


%changelog
* Mon May 01 2023 Jon Turney <jon.turney@dronecode.org.uk> - 0.19.8.1-1
- add make to BuildRequires

* Tue Dec 05 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 0.19.8.1-1
- new version

* Mon Sep 12 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 0.19.7-1
- new version

* Sun Feb 21 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 0.19.5.1-1
- new version

* Tue Mar 10 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 0.19.4-1
- new version

* Mon Jun 16 2014 Yaakov Selkowitz <yselkowitz@cygwin.com> - 0.18.3.2-1
- Version bump.

* Sun Jun 30 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.18.1.1-3
- Rebuild for new Cygwin packaging scheme.
- Add cygwin64 support.

* Thu Jan 24 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.18.1.1-2
- Remove bogus printf symbols from libintl.
- Set correct config.cache values for more AC_TRY_RUNs.

* Mon Oct 31 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.18.1.1-1
- Version bump.
- Included relocation and locale patches from Cygwin gettext 0.18.1.1-2.

* Sun Aug 21 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.17-2
- Remove Cygwin EXEs and other files not needed for cross-compiling.

* Thu Feb 17 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.17-1
- Initial RPM release, largely based on mingw32-gettext.
