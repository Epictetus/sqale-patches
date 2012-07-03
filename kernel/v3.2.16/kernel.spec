Name: kernel
Summary: The Linux Kernel
Version: 3.2.16_grsec
Release: 3
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: http://www.kernel.org
Source0: kernel-3.2.16_grsec.tar.gz
Source1: config-3.2.16-grsec
BuildRoot: %{_tmppath}/%{name}-%{PACKAGE_VERSION}-root
Provides:  kernel-3.2.16-grsec
Patch0: increase_prot_sock.patch
Patch1: change_prot_sock_in_case_of_udp.patch
Patch2: cgroup_fork.patch
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%description
The Linux Kernel, the operating system core itself

%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: kernel-headers
Provides: kernel-headers = %{version}
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
cp %{_sourcedir}/config-3.2.16-grsec ./.config

%build
make clean && make %{?_smp_mflags}

%install
%ifarch ia64
mkdir -p $RPM_BUILD_ROOT/boot/efi $RPM_BUILD_ROOT/lib/modules
mkdir -p $RPM_BUILD_ROOT/lib/firmware
%else
mkdir -p $RPM_BUILD_ROOT/boot $RPM_BUILD_ROOT/lib/modules
mkdir -p $RPM_BUILD_ROOT/lib/firmware
%endif
INSTALL_MOD_PATH=$RPM_BUILD_ROOT make %{?_smp_mflags} KBUILD_SRC= modules_install
%ifarch ia64
cp $KBUILD_IMAGE $RPM_BUILD_ROOT/boot/efi/vmlinuz-3.2.16-grsec
ln -s efi/vmlinuz-3.2.16-grsec $RPM_BUILD_ROOT/boot/
%else
%ifarch ppc64
cp vmlinux arch/powerpc/boot
cp arch/powerpc/boot/$KBUILD_IMAGE $RPM_BUILD_ROOT/boot/vmlinuz-3.2.16-grsec
%else
cp arch/x86/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-3.2.16-grsec
%endif
%endif
make %{?_smp_mflags} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install
cp System.map $RPM_BUILD_ROOT/boot/System.map-3.2.16-grsec
cp .config $RPM_BUILD_ROOT/boot/config-3.2.16-grsec
%ifnarch ppc64
cp vmlinux vmlinux.orig
bzip2 -9 vmlinux
mv vmlinux.bz2 $RPM_BUILD_ROOT/boot/vmlinux-3.2.16-grsec.bz2
mv vmlinux.orig vmlinux
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%dir /lib/modules
/lib/modules/3.2.16-grsec
/lib/firmware
/boot/*

%files headers
%defattr (-, root, root)
/usr/include

