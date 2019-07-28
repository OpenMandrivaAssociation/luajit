%define major 2
%define api 5.1
%define libname %mklibname %{name}-%{api} %{major}
%define libcommon %mklibname %{name}-%{api}-common
%define devname %mklibname %{name}-%{api} -d
%define beta beta3

%define tarname LuaJIT

Name:		luajit
Version:	2.1.0
Release:	0.%{beta}.1
Summary:	Just-In-Time Compiler for the Lua programming language
Group:		Development/Other
License:	MIT
Url:		http://luajit.org/luajit.html
# http://luajit.org/download/LuaJIT-2.0.0-beta10.tar.gz
Source0:	https://github.com/LuaJIT/LuaJIT/archive/v%{version}-%{beta}.tar.gz
Patch0:		luajit-2.1.0-no-Lusrlib.patch
Requires:	%{libcommon} = %{version}-%{release}

%description
LuaJIT has been successfully used as a scripting middle-ware in games,
3D modelers, numerical simulations, trading platforms and many other
specialty applications.
It combines high flexibility with high performance and an unmatched low
memory footprint: less than 125K for the VM plus less than 85K for the
JIT compiler (on x86).
LuaJIT has been in continuous development since 2005. It is widely considered
to be one of the fastest dynamic language implementations.

%package -n %{libcommon}
Summary:	Just-In-Time Compiler for the Lua programming language
Group:		System/Libraries

%description -n %{libcommon}
LuaJIT has been successfully used as a scripting middle-ware in games,
3D modelers, numerical simulations, trading platforms and many other
specialty applications.
It combines high flexibility with high performance and an unmatched low
memory footprint: less than 125K for the VM plus less than 85K for the
JIT compiler (on x86).
LuaJIT has been in continuous development since 2005. It is widely considered
to be one of the fastest dynamic language implementations.

%package -n %{libname}
Summary:	Just-In-Time Compiler for the Lua programming language
Group:		System/Libraries
Requires:	%{libcommon} = %{version}-%{release}

%description -n %{libname}
LuaJIT has been successfully used as a scripting middle-ware in games,
3D modelers, numerical simulations, trading platforms and many other
specialty applications.
It combines high flexibility with high performance and an unmatched low
memory footprint: less than 125K for the VM plus less than 85K for the
JIT compiler (on x86).
LuaJIT has been in continuous development since 2005. It is widely considered
to be one of the fastest dynamic language implementations.

%package -n %{devname}
Summary:	Just-In-Time Compiler for the Lua programming language
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{tarname}-devel = %{version}-%{release}

%description -n %{devname}
This package contains header files needed by developers.

%prep
%autosetup -p1 -n %{tarname}-%{version}-beta3
%if "%{_lib}" != "lib"
sed -i -e 's,^multilib=lib,multilib=%{_lib},' etc/luajit.pc
%endif

%build
%make_build amalg PREFIX=%{_usr} \
	Q='' \
	DEFAULT_CC=%{__cc} \
	CCDEBUG="%{optflags}" \
	TARGET_LDFLAGS="%{ldflags}" \
%ifarch %{x86_64} %{aarch64}
	TARGET_CFLAGS="%{optflags} -DMULTIARCH_PATH='\"%{_libdir}/\"'" INSTALL_LIB="%{buildroot}%{_libdir}"
%else
	TARGET_CFLAGS="%{optflags}" INSTALL_LIB="%{buildroot}%{_libdir}"
%endif

%install
%make_install PREFIX=%{_usr} INSTALL_LIB=%{buildroot}%{_libdir}

ln -sf %{_bindir}/%{name}-%{version}-%{beta} %{buildroot}%{_bindir}/%{name}
ln -sf %{_libdir}/libluajit-%{api}.so.%{version} %{buildroot}%{_libdir}/libluajit-%{api}.so

%files
%doc COPYRIGHT README
%{_bindir}/%{name}-%{version}-%{beta}
%{_bindir}/%{name}
%{_mandir}/man1/luajit.1.xz

%files -n %{libcommon}
%{_datadir}/%{name}-%{version}-%{beta}/jit/*.lua

%files -n %{libname}
%{_libdir}/lib%{name}*.so.%{major}
%{_libdir}/lib%{name}*.so.%{version}

%files -n %{devname}
%{_includedir}/luajit*/*.h*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/libluajit*.a
%{_libdir}/libluajit-%{api}.so
