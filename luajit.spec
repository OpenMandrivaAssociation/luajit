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
# The version tag is given in seconds since January 1, 1970
%define versiontag 1693350652

%define tarname LuaJIT

%global optflags %{optflags} -O3

Name:		luajit
Version:	2.1.%{versiontag}
Release:	1
Summary:	Just-In-Time Compiler for the Lua programming language
Group:		Development/Other
License:	MIT
Url:		http://luajit.org/luajit.html
Source0:	https://github.com/LuaJIT/LuaJIT/archive/refs/heads/v%{mmajor}.tar.gz
Patch0:		luajit-2.1.0-no-Lusrlib.patch
# RISC-V support patches based on the git repository at
# https://github.com/infiWang/LuaJIT-RV
Patch1000:	0001-dynasm-stash-riscv-progress.patch
# MODIFIED: removed chunk affecting src/lj_vm.h (floor/ceil) that is
# undone in 0018 [and doesn't apply on current 2.1]
Patch1001:	0002-lj-wip-init-rv64-interpreter-lib-progress.patch
Patch1002:	0003-lj-wip-init-rv64-interpreter-bcvm-progress.patch
Patch1003:	0004-lj-wip-refine-rv64-interpreter-bcvm-and-rx-0.patch
Patch1004:	0005-lj-wip-refine-rv64-interpreter-bc-decode-and-registe.patch
Patch1005:	0006-lj-wip-riscv-base-defs.patch
Patch1006:	0007-dynasm-riscv-fix-reg-parse_disp-shftw-fmv-dx.patch
Patch1007:	0008-lj-wip-vm_riscv64-minor-fix.patch
Patch1008:	0009-riscv64-interp-fix-branch-global-label-overflow.patch
Patch1009:	0010-riscv64-interp-misc-fix.patch
Patch1010:	0011-riscv64-interp-fix-bit.bswap.patch
Patch1011:	0012-riscv64-interp-fix-BC_IS-LT-LE-GT-GE.patch
Patch1012:	0013-dynasm-riscv-fix-negw.patch
Patch1013:	0014-dynasm-riscv-fix-RISC-V-ISA-ISE-iterate-order.patch
Patch1014:	0015-dasm-riscv-fix-shamt.patch
Patch1015:	0016-dynasm-riscv-allow-orderedPair-work-with-minilua.patch
Patch1016:	0017-dynasm-riscv-refactor-orderedPairs.patch
# 0018-riscv-interp-remove-stale-math-helper-condition.patch dropped (we fix 0002 instead)
Patch1018:	0019-riscv-enable-vm_modi-helper-on-riscv64-platform.patch
Patch1019:	0020-riscv-interp-add-a-pseudo-GOT-for-riscv64-platform.patch
Patch1020:	0021-riscv-interp-comment-cleanup.patch
# MODIFIED: rebased
Patch1021:	0022-riscv-target-prepare-for-RISC-V-64-backend.patch
Patch1022:	0023-riscv-emit-init.patch
Patch1023:	0024-riscv64-asm-init.patch
Patch1024:	0025-jit-add-RISC-V-flags.patch
Patch1025:	0026-asm-include-RISC-V-64-header.patch
Patch1026:	0027-riscv-interp-migrate-from-JGL-to-GL.patch
Patch1027:	0028-riscv-interp-optimize-branch.patch
Patch1028:	0029-riscv-interp-prepare-for-JIT.patch
Patch1029:	0030-riscv-interp-refine-helper-macros.patch
Patch1030:	0031-riscv-emit-polish-rot-lsptr-opk-lso-branch-jmp.patch
Patch1031:	0032-riscv-interp-fix-LJ_KEYINDEX-load.patch
Patch1032:	0033-emit-include-riscv-target-header.patch
Patch1033:	0034-riscv-emit-misc-fix.patch
Patch1034:	0035-riscv-target-drop-fixed-x5.patch
Patch1035:	0036-target-correct-RISC-V-header.patch
Patch1036:	0037-riscv-target-fix-reg.patch
Patch1037:	0038-riscv-emit-misc-fix.patch
Patch1038:	0039-riscv-target-add-missing-pseudo-instr.patch
Patch1039:	0040-riscv-emit-fix-movrr.patch
Patch1040:	0041-riscv-interp-misc-fix.patch
Patch1041:	0042-riscv-emit-misc-fix.patch
Patch1042:	0043-riscv-emit-modify-emit_opk.patch
Patch1043:	0044-riscv-asm-misc-fix.patch
Patch1044:	0045-riscv-jit-exit-handler-context-dispatch-fix.patch
Patch1045:	0046-riscv-emit-fix-delta.patch
Patch1046:	0047-riscv64-asm-misc-fixup.patch
Patch1047:	0048-riscv-target-fix-IMMB-encode-macro.patch
Patch1048:	0049-riscv-emit-misc-fix.patch
Patch1049:	0050-riscv-emit-optimize-emit_loadk32-special-case-handli.patch
Patch1050:	0051-riscv-emit-fix-emit_-call-jmp.patch
Patch1051:	0052-jit-fix-riscv-cpu-flag-detection.patch
Patch1052:	0053-arch-tune-RISC-V-64-JUMPRANGE.patch
Patch1053:	0054-riscv-asm-misc-fix.patch
Patch1054:	0055-riscv-asm-fix-misc-loadop-src-dst.patch
Patch1055:	0056-riscv-asm-drop-unused-irl-in-bnot.patch
Patch1056:	0057-riscv-asm-drop-unused-variable.patch
Patch1057:	0058-riscv-target-remove-ra-from-scratch-register-list.patch
Patch1058:	0059-riscv-emit-fix-emit_jmp-scratch-register-alloc.patch
Patch1059:	0060-riscv-interp-Fix-BC_ISNEN-PC-calculation.patch
Patch1060:	0061-riscv-interp-optimize-more-branch.patch
Patch1061:	0062-riscv-asm-fix-asm_tointg-guard.patch
Patch1062:	0063-riscv-asm-fix-asm_href-num-branch.patch
Patch1063:	0064-riscv-asm-refine-asm_href-bit-select-semantic.patch
# MODIFIED: rebased
Patch1064:	0065-riscv-ffi-FFI-init.patch
Patch1065:	0066-dynasm-riscv-fix-RVF-RVD-rounding-mode.patch
Patch1066:	0067-dynasm-riscv-silent-compiler-warning.patch
Patch1067:	0068-riscv-interp-rearange-FFI-handler-layout.patch
Patch1068:	0069-riscv-ffi-fix-callback-mcode-init-macro-and-ub.patch
Patch1069:	0070-riscv-comply-lp64d-ABI-sp-alignment.patch
Patch1070:	0071-riscv-jit-fix-lj_vmeta_for-dispatch.patch
Patch1071:	0072-riscv-ffi-fix-BC_IS-EQ-NE-V-vmeta-cdata-comparision-.patch
Patch1072:	0073-riscv-interp-clean-unnecessary-liw-helper.patch
Patch1073:	0074-riscv-misc-revert-early-development-workarounds-in-M.patch
# MODIFIED: rebased
Patch1074:	0075-riscv-vm-stop-generate-RVC-and-relax-in-lj_vm.patch
Patch1075:	0076-riscv-misc-FFI-related-bug-workaround.patch
Patch1076:	0077-riscv-misc-cleanup-nonsense-comment.patch
Patch1077:	0078-riscv-interp-reallocate-TMP-registers-to-comply-with.patch
Patch1078:	0079-Revert-riscv-misc-FFI-related-bug-workaround.patch
Patch1079:	0080-riscv-jit-follow-global-FMA-flag.patch
Patch1080:	0081-riscv-jit-fix-asm_fpunary-with-pseudo-instruction.patch
Patch1081:	0082-riscv-jit-fix-asm_mulov.patch
Patch1082:	0083-riscv-jit-optimize-asm_mulov.patch
Patch1083:	0084-riscv-jit-fix-trace-number-handling-on-JIT-exit.patch
Patch1084:	0085-riscv-jit-tune-trace-number-handling.patch
Patch1085:	0086-riscv-jit-fix-asm_fpcomp.patch
Patch1086:	0087-riscv-jit-fix-asm_min_max-with-integer.patch
Patch1087:	0088-riscv-jit-correct-scratch-register-list.patch
Patch1088:	0089-riscv-misc-correct-FUNCT3-FUNCT7-instruction-field-h.patch
Patch1089:	0090-riscv-jit-fix-asm_href-generic-type-hashing.patch
Patch1090:	0091-riscv-jit-fix-asm_loop_fixup-on-non-inverted-loop-ca.patch
Patch1091:	0092-riscv-jit-fix-asm_tobit.patch
Patch1092:	0093-riscv-jit-more-trace-number-handler-tuning.patch
Patch1093:	0094-riscv-jit-fix-asm_prof.patch
Patch1094:	0095-riscv-jit-fix-asm_tail_fixup.patch
Patch1095:	0096-riscv-emit-fix-emit_jmp.patch
Patch1096:	0097-riscv-emit-fix-emit_call.patch
Patch1097:	0098-riscv-asm-fix-emit_rot-i.patch
Patch1098:	0099-riscv-asm-fix-asm_bswap.patch
Patch1099:	0100-riscv-jit-initial-exitno-handling-overhaul.patch
Patch1100:	0101-riscv-asm-asm_guard-cleanup.patch
Patch1101:	0102-riscv-interp-random-immediate-optimizations.patch
Patch1102:	0103-riscv-emit-fix-emit_rot.patch
Patch1103:	0104-riscv-interp-conditional-select-optimizations.patch
Patch1104:	0105-riscv-emit-fix-emit_roti.patch
Patch1105:	0106-riscv-asm-tune-asm_comp.patch
Patch1106:	0107-riscv-asm-fix-asm_sparejump_use-argument-type.patch
Patch1107:	0108-riscv-emit-fix-emit_loadk32.patch
Patch1108:	0109-riscv-emit-drop-emit_loadk20.patch
Patch1109:	0110-riscv-emit-optimize-emit_loadu64.patch
Patch1110:	0111-riscv-asm-fix-emit_loadu64.patch
Patch1111:	0112-riscv-emit-further-optimize-emit_loadu64.patch
Patch1112:	0113-riscv-emit-cleanup-emit_loadu64.patch
Patch1113:	0114-riscv-emit-emit_loadu64-regression-workaround.patch
Patch1114:	0115-riscv-asm-cleanup-asm_gc_check.patch
Patch1115:	0116-riscv-asm-fix-asm_patchexit-on-end-of-loop-exit.patch
Patch1116:	0117-riscv-asm-fix-asm_tointg.patch
Patch1117:	0118-riscv-ffi-callback-initial-fix.patch
Patch1118:	0119-riscv-ffi-fix-last-commit.patch
Patch1119:	0120-riscv-emit-fix-emit_opk-constant-argument-type.patch
Patch1120:	0121-riscv-ffi-fix-lj_vm_ffi_callback.patch
Patch1121:	0122-riscv-arch-set-free-JIT-FFI.patch
Patch1122:	0123-riscv-dispatch-fix-FFIGOTDEF.patch
Patch1123:	0124-riscv-makefile-add-fwrapv-as-workaround.patch
Patch1124:	0125-riscv-jit-add-disassembler-and-bcsave-definition.patch
Patch1125:	0126-riscv-emit-sanitize-ub.patch
Patch1126:	0127-Revert-riscv-makefile-add-fwrapv-as-workaround.patch
Patch1127:	0128-riscv-emit-more-sanitization.patch
Patch1128:	0129-riscv-asm-fix-float-to-int-type-conversion-rounding.patch
Patch1129:	0130-riscv-asm-asm_setup_call_slots-workaround.patch
Patch1130:	0131-riscv-jit-fix-bcsave-ELF-e_flags.patch
Patch1131:	0132-riscv-interp-refine-TOBIT-init.patch
Patch1132:	0133-riscv-interp-refine-BC_MULxx.patch
Patch1133:	0134-riscv-interp-refine-last-commit.patch
Patch1134:	0135-riscv-jit-probe-and-emit-zba-zbb-extension.patch
Patch1135:	0136-riscv-asm-fix-asm_href-branch-guard-patching.patch
Patch1136:	0137-riscv-asm-refine-last-commit.patch
Patch1137:	0138-riscv-jit-probe-for-compressed-extension.patch
Patch1138:	0139-riscv-jit-format-riscv-functions.patch
Patch1139:	0140-riscv-asm-fix-sparejump-return-chaining.patch
Patch1140:	0141-riscv-asm-revert-last-commit.patch
Patch1141:	0142-riscv-interp-fix-minmax-fast-function.patch
Patch1142:	0143-riscv-jit-attempt-to-fuse-andn-orn-xnor.patch
Patch1143:	0144-riscv-asm-copy-RID_TMP-magic-from-MIPS.patch
Patch1144:	0145-riscv-asm-fix-asm_gencall-with-variable-argument-fun.patch
Patch1145:	0146-riscv-asm-fix-asm_setup_call_slots-with-variable-arg.patch
Patch1146:	0147-riscv-asm-fix-asm_hrefk-bigofs-check.patch
Patch1147:	0148-riscv-asm-introduce-XThead-ext-more-bitmanip-optimiz.patch
Patch1148:	0149-riscv-jit-correct-stack-pointer-alignment.patch
Patch1149:	0150-riscv-asm-fix-base-register-coalescing-in-side-trace.patch
# 0151-misc-add-a-proper-README.patch disabled, clashes with master (and is README only)
# 0152-misc-update-README.patch disabled, clashes with master (and is README only)
Patch1152:	0153-riscv64-interp-Ensure-forward-progress-on-trace-exit.patch
Patch1153:	0154-riscv64-Fix-bad-FP-FLOAD-assertion.patch
Patch1154:	0155-DynASM-riscv64-Fix-warnings.patch
Patch1155:	0156-riscv64-asm-fix-asm_bswap-scratch-register-list.patch
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
