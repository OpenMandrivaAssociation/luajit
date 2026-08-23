%if %cross_compiling
%undefine _debugsource_packages
%ifarch %{riscv}
# clang's RISC-V target seems to be missing __clear_cache,
# use gcc for now
%define prefer_gcc 1
%endif
%endif

%define major 2
%define mmajor %(echo %{version} |cut -d. -f1-2)
%define api 5.1
%define oldlibname %mklibname %{name}-%{api} %{major}
%define libname %mklibname %{name}-%{api}
%define libcommon %mklibname %{name}-%{api}-common
%define devname %mklibname %{name}-%{api} -d

# Upstream has officially switched to "release never" and
# recommending git snapshots.
# The version tag is given in seconds since January 1, 1970 00:00
%define versiontag 1787165859
%define tarname LuaJIT

%global optflags %{optflags} -O3

Name:		luajit
Version:	2.1.%{versiontag}
Release:	1
Summary:	Just-In-Time Compiler for the Lua programming language
Group:		Development/Other
License:	MIT
Url:		https://luajit.org/luajit.html
Source0:	https://github.com/LuaJIT/LuaJIT/archive/refs/heads/v%{mmajor}.tar.gz
Patch0:		luajit-2.1.0-no-Lusrlib.patch
# RISC-V support from https://github.com/infiWang/LuaJIT-RV (v2.1-riscv64),
# rebased onto current upstream v2.1. README.md patch omitted.
Patch1000:	0001-riscv-support-add-RISC-V-64-arch-base-definition.patch
Patch1001:	0002-riscv-dynasm-add-RISC-V-support.patch
Patch1002:	0003-riscv-interp-add-register-definition.patch
Patch1003:	0004-riscv-interp-add-frame-definition.patch
Patch1004:	0005-riscv-interp-add-helper-macros-and-typedefs.patch
Patch1005:	0006-riscv-interp-add-base-assembly-interpreter-VM.patch
Patch1006:	0007-riscv-support-add-target-definition.patch
Patch1007:	0008-riscv-ffi-add-call-convention-and-support-framework.patch
Patch1008:	0009-riscv-support-add-extension-detection.patch
Patch1009:	0010-riscv-jit-add-mandatory-constants.patch
Patch1010:	0011-riscv-jit-add-insn-emitter.patch
Patch1011:	0012-riscv-jit-add-IR-assembler.patch
Patch1012:	0013-riscv-interp-add-VM-builder-support.patch
Patch1013:	0014-riscv-misc-add-bytecode-listing-support.patch
Patch1014:	0015-riscv-jit-add-hooks-in-interpreter.patch
Patch1015:	0016-riscv-interp-add-DWARF-info.patch
Patch1016:	0017-riscv-jit-add-GDBJIT-support.patch
Patch1017:	0018-riscv-support-linux-add-Linux-specfic-icache-sync-co.patch
Patch1018:	0019-riscv-support-linux-make-mremap-non-moving-due-to-VA.patch
Patch1019:	0020-riscv-misc-add-disassmbler-support.patch
Patch1020:	0021-riscv-misc-add-support-in-Makefile.patch
# LoongArch64 support from https://github.com/loongson/LuaJIT (v2.1-loongarch64),
# rebased onto current upstream v2.1 + RISC-V. LUAJIT_ARCH_LOONGARCH64 is 9
# (RISC-V already uses 8).
Patch2000:	0001-LoongArch64-Add-target-architecture-selection.patch
Patch2001:	0002-LoongArch64-Add-DynASM-support.patch
Patch2002:	0003-LoongArch64-Add-register-assignments-for-the-interpr.patch
Patch2003:	0004-LoongArch64-Add-stack-layout.patch
Patch2004:	0005-LoongArch64-Add-some-general-macro-type-definitions-.patch
Patch2005:	0006-LoongArch64-Add-pure-interpreter-backend.patch
Patch2006:	0007-LoongArch64-Add-definitions-for-target-CPU.patch
Patch2007:	0008-LoongArch64-Add-some-constant-definitions.patch
Patch2008:	0009-LoongArch64-Add-LoongArch-instruction-emitter.patch
Patch2009:	0010-LoongArch64-Add-IR-assembler-support.patch
Patch2010:	0011-LoongArch64-Add-JIT-support-in-the-interpreter.patch
Patch2011:	0012-LoongArch64-Add-CPU-feature-detection-when-init-JIT-.patch
Patch2012:	0013-LoongArch64-Add-LoongArch-lp64-calling-conventions-a.patch
Patch2013:	0014-LoongArch64-Add-FFI-C-callback-handling.patch
Patch2014:	0015-LoongArch64-Add-FFI-support-in-the-interpreter.patch
Patch2015:	0016-LoongArch64-Add-DWARF-and-ELF-header-definitions.patch
Patch2016:	0017-LoongArch64-Add-support-for-LuaJIT-VM-builder.patch
Patch2017:	0018-LoongArch64-Add-loongarch64-support-when-save-list-b.patch
Patch2018:	0019-LoongArch64-Add-LoongArch64-disassembler-module.patch
Patch2019:	0020-LoongArch64-Add-support-in-Makefile.patch
Patch2020:	0021-LoongArch64-Upgrade-the-base-code-to-v2.1.ROLLING.patch
Patch2021:	0022-LoongArch64-Sync-code-with-luajit2-s-6f2fa1d9.patch
Patch2022:	0023-LOONGARCH64-Optimize-function-that-moves-i32-constan.patch
Patch2023:	0024-LOONGARCH64-Optimize-emit_store-loadofs-and-emit_mov.patch
Patch2024:	0025-LOONGARCH64-Optimize-emit_djml-function-and-remove-e.patch
Patch2025:	0026-LOONGARCH64-Optimize-register-allocation-RID_R20-reg.patch
Patch2026:	0027-LOONGARCH64-Add-stack-check-to-pcall-xpcall.patch
Patch2027:	0028-LOONGARCH64-Fixed-the-register-allocation-bug-in-asm.patch
Patch2028:	0029-LOONGARCH64-Fix-the-setup-for-the-end-of-each-trace-.patch
Patch2029:	0030-LOONGARCH64-Standardize-coding-style-and-comments.patch
Patch2030:	0031-LOONGARCH64-Fix-the-.ffunc_1-tostring.patch
Patch2031:	0032-LOONGARCH64-Optimize-emit_-functions-to-eliminate-th.patch
Patch2032:	0033-LOONGARCH64-Optimize-LOONGF_I-to-LOONGF_I-to-elimina.patch
Patch2033:	0034-LOONGARCH64-Optimize-the-efficiency-of-getting-setti.patch
Patch2034:	0035-LOONGARCH64-Fix-the-error-of-checking-the-immediate-.patch
Patch2035:	0036-LOONGARCH64-Fix-emit_lsptr-and-emit_load-storeofs-fu.patch
Patch2036:	0037-LOONGARCH64-Fix-the-bug-introduced-by-emit_-function.patch
Patch2037:	0038-LOONGARCH64-Fix-the-way-to-load-UREF-op1-address-in-.patch
Patch2038:	0039-LOONGARCH64-Fix-the-branch-that-is-out-of-range-when.patch
Patch2039:	0040-LOONGARCH64-Optimized-the-bswap-function.patch
Patch2040:	0041-LOONGARCH64-Fixed-the-bug-in-math_minmax-function.patch
Patch2041:	0042-LOONGARCH64-Fixed-the-bug-in-pcall-and-xpcall-functi.patch
Patch2042:	0043-LOONGARCH64-Optimized-the-use-of-some-conditional-br.patch
Patch2043:	0044-LOONGARCH64-Fix-the-bug-in-Hard-float-round-to-integ.patch
Patch2044:	0045-LOONGARCH64-Fixed-the-bugs-of-movfcsr2gr_2-movgr2fcs.patch
Patch2045:	0046-LOONGARCH64-Optimizing-the-vm_next-function.patch
Patch2046:	0047-LOONGARCH64-Bump-copyright-date.patch
Patch2047:	0048-LOONGARCH64-Fix-pcall-error-case.patch
Patch2048:	0049-LOONGARCH64-Fix-FP-to-integer-conversions.patch
Patch2049:	0050-LOONGARCH64-Add-the-definition-and-usage-of-the-CFR.patch
Patch2050:	0051-LOONGARCH64-Fix-vm_next-register-dirty-read-bug.patch
Patch2051:	0052-LOONGARCH64-Fix-min-max-return-register-error.patch
Patch2052:	0053-LOONGARCH64-Optimize-unary-test-and-copy-ops.patch
Patch2053:	0054-LOONGARCH64-Fix-the-BC_UNM-int-error.patch
Patch2054:	0055-LOONGARCH64-Optimize-binary-arith-ops.patch
Patch2055:	0056-LOONGARCH64-Optimize-the-BC_KNUM.patch
Patch2056:	0057-LOONGARCH64-Optimize-the-table-upvalue-and-function-.patch
Patch2057:	0058-LOONGARCH64-Fix-BC_TSETS_Z-overwriting-the-mark-regi.patch
Patch2058:	0059-LOONGARCH64-Optimize-calls-and-vararg-handling.patch
Patch2059:	0060-LOONGARCH64-Optimize-target-jump-calculation-by-stre.patch
Patch2060:	0061-LOONGARCH64-Optimize-return-ops.patch
Patch2061:	0062-LOONGARCH64-Eliminate-unnecessary-register-moves-and.patch
Patch2062:	0063-LOONGARCH64-Simplify-function-headers-by-eliminating.patch
Patch2063:	0064-LOONGARCH64-Switch-from-DISPATCH-base-to-JGL-base-to.patch
Patch2064:	0065-LOONGARCH64-Replace-or-CARG1-L-r0-with-mv-CARG1-L-to.patch
Patch2065:	0066-LOONGARCH64-Replace-jirl-r0-ra-0-with-ret-to-improve.patch
Patch2066:	0067-LOONGARCH64-Replace-addi.d-rd-r0-si12-with-l12i-rd-s.patch
Patch2067:	0068-LOONGARCH64-Fix-the-bug-of-register-allocation-overl.patch
Patch2068:	0069-LOONGARCH64-Optimize-the-comparison-method-of-certai.patch
Patch2069:	0070-LOONGARCH64-Replace-addi.w-rd-r0-si12-with-l12i-rd-s.patch
Patch2070:	0071-LOONGARCH64-Adjust-assembly-instructions-to-improve-.patch
Patch2071:	0072-LOONGARCH64-Fix-li-traceno-range-check-and-instructi.patch
Patch2072:	0073-LOONGARCH64-Fix-the-bug-in-generating-machine-instru.patch
Patch2073:	0074-LOONGARCH64-Fix-offset-calculation-between-current-P.patch
Patch2074:	0075-LOONGARCH64-Optimize-the-implementation-mechanism-of.patch
Patch2075:	0076-LOONGARCH64-Fix-tmp-register-restored-after-guard-ex.patch
Patch2076:	0077-LOONGARCH64-Optimize-register-allocation-to-use-RID_.patch
Patch2077:	0078-LOONGARCH64-Fixed-ffi_callback-to-ensure-global_Stat.patch
Patch2078:	0079-LOONGARCH64-Fixed-the-old-PC-being-overwritten-by-th.patch
Patch2079:	0080-LOONGARCH64-Fixed-data-loss-in-number-type-caused-by.patch
Patch2080:	0081-LOONGARCH64-Use-LJ_NO_UNWIND-macro-to-control-genera.patch
Patch2081:	0082-LOONGARCH64-Fix-the-bug-where-the-value-of-FTMP0-is-.patch
Patch2082:	0083-LOONGARCH64-Fix-debug_frame-and-eh_frame-CFI-for-vm_.patch
Patch2083:	0084-LOONGARCH64-Adjust-.eh_frame-CIE-and-FDE-alignment-f.patch
Patch2084:	0085-LOONGARCH64-Use-__builtin___clear_cache-instead-of-_.patch
Patch2085:	0086-LOONGARCH64-Use-__loongarch_lp64-instead-of-_ABILP64.patch
Patch2086:	0087-LoongArch64-Allow-mcode-allocations-outside-of-the-j.patch
Patch2087:	0088-LoongArch64-Unify-Lua-number-to-FFI-integer-conversi.patch
Patch2088:	0089-LoongArch64-DUALNUM-Improve-fix-edge-cases-of-unary-.patch
Patch2089:	0090-LoongArch64-Avoid-unaligned-load-in-lj_vm_exit_inter.patch
Patch2090:	0091-LoongArch64-Bump-copyright-date.patch
# Interpreter was missing BC_BNOT/BAND/BOR/BXOR/BSHL/BSHR/BSAR; buildvm
# died with "undefined opcode BC_BNOT". JIT and bit.* ffuncs already exist.
Patch2091:	0092-LoongArch64-Add-missing-interpreter-bitops.patch

Requires:	%{libcommon} = %{version}-%{release}

BuildRequires:	make
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
%rename %{oldlibname}

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
%autosetup -p1 -n %{tarname}-%{mmajor}
%if "%{_lib}" != "lib"
sed -i -e 's,^multilib=lib,multilib=%{_lib},' etc/luajit.pc
%endif

%build
%make_build amalg PREFIX=%{_usr} \
	Q='' \
	DEFAULT_CC="%{__cc}" \
%if %cross_compiling
%ifarch %{riscv}
	HOST_CC="clang -D__riscv_compressed -D__riscv_float_abi_double" \
%else
	HOST_CC="clang" \
%endif
%else
	CCDEBUG="%{optflags}" \
%endif
	TARGET_LDFLAGS="%{ldflags}" \
	XCFLAGS="-DLUAJIT_ENABLE_LUA52COMPAT" \
	MULTILIB="%{_lib}" \
%if "%{_lib}" != "lib"
	TARGET_CFLAGS="%{optflags} -DMULTIARCH_PATH='\"%{_libdir}/\"'" INSTALL_LIB="%{buildroot}%{_libdir}"
%else
	TARGET_CFLAGS="%{optflags}" INSTALL_LIB="%{buildroot}%{_libdir}"
%endif

%install
%make_install PREFIX=%{_usr} MULTILIB="%{_lib}" INSTALL_LIB=%{buildroot}%{_libdir}

ln -sf %{_bindir}/%{name}-%{version} %{buildroot}%{_bindir}/%{name}
ln -sf %{_libdir}/libluajit-%{api}.so.%{version} %{buildroot}%{_libdir}/libluajit-%{api}.so

%files
%doc COPYRIGHT README
%{_bindir}/%{name}-%{version}
%{_bindir}/%{name}
%{_mandir}/man1/luajit.1.*

%files -n %{libcommon}
%{_datadir}/%{name}-%{mmajor}/jit/*.lua

%files -n %{libname}
%{_libdir}/lib%{name}*.so.%{major}
%{_libdir}/lib%{name}*.so.%{version}

%files -n %{devname}
%{_includedir}/luajit*/*.h*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/libluajit*.a
%{_libdir}/libluajit-%{api}.so
