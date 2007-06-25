%define am_i_cooker 0
%define distrib Cooker
%define version 2008.0
%define rel 0.2
%define distname China
%define distsuffix mdv
%define distribution Mandriva Linux

%define product_vendor Mandriva
%define product_distribution %distribution
%define product_type Basic
%define product_version %version
%define product_branch Devel
%define product_release 1
%define product_arch %{_target_cpu}

%define product_id_base vendor=%product_vendor,distribution=%product_distribution,type=%product_type,version=%product_version,branch=%product_branch,release=%product_release,arch=%product_arch

%if %am_i_cooker
    %define distrib Cooker
    %define unstable %%_with_unstable --with-unstable
%endif

# The mandriva release, what is written on box
%define mandriva_release %version

# The mandriva branch: Cooker, Community or Official
%define mandriva_branch %distrib

# The mandriva arch, notice: using %_target_cpu is bad
# elsewhere because this depend of the config of the packager
# _target_cpu => package build for
# mandriva_arch => the distribution we are using
%define mandriva_arch %_target_cpu

# To be coherent with %mandriva_arch I provide os too
# be I wonder it will be linux for a long time
%define mandriva_os %_target_os

%define realversion %version
%define mdkver %(echo %version | sed 's/\\.//')0

Summary:	Mandriva release file
Name:		mandriva-release
Version:	%version
Release:	%mkrel %rel
License:	GPL
URL:		http://www.mandrivalinux.com/
Group:		System/Configuration/Other
Source:		%name.tar.bz2
Source1:	10mandriva-release.sh
Source2:	10mandriva-release.csh
Source3:	CREDITS
# edited lynx -dump of wiki:
Source4:	release-notes.txt
Source5:	README.urpmi
Obsoletes:	rawhide-release redhat-release mandrake-release mandrakelinux-release
BuildRoot:	%{_tmppath}/%{name}-root

%description
Mandriva Linux release file.

%package common
Summary: Mandriva release common files
Group: System/Configuration/Other
Conflicts: %name < %version-%release

%description common
Mandriva Linux release file.

%define release_package(s) \
%{-s:%package %1} \
Summary: Mandriva release file%{?1: for %1} \
Group: System/Configuration/Other \
Requires:	mandriva-release-common \
Provides:	redhat-release rawhide-release mandrake-release mandrakelinux-release \
Provides:	%name = %version-%release \
Obsoletes: %name < %version-%release rawhide-release redhat-release mandrake-release mandrakelinux-release

%define release_descr(s) \
%description %{-s:%1} \
Mandriva Linux release file. \


%define release_post(s) \
%post %{-s:%1} \
ln -fs product.id.%1 /etc/product.id


%define release_install(s) \
cat > %buildroot/etc/product.id.%{1} << EOF \
%{product_id_base},product=%1\
EOF\
 \
mkdir -p %buildroot%_sys_macros_dir \
cat > %buildroot%_sys_macros_dir/%{1}.macros <<EOF \
%%distribution      %distribution\
%%mandriva_release  %mandriva_release\
%%mandriva_branch   %mandriva_branch\
%%mandriva_arch     %mandriva_arch\
%%mandriva_os       %mandriva_os\
%%mandriva_class    %%(. %_sysconfdir/sysconfig/system; echo \\\$META_CLASS)\
%%mdkver            %mdkver\
%%mdvver            %mdkver\
%%distsuffix        %distsuffix\
\
# productid variable\
%%product_id %{product_id_base},product=%{1}\
\
%%product_vendor        %product_vendor\
%%product_distribution  %product_distribution\
%%product_type          %product_type\
%%product_version       %product_version\
%%product_branch        %product_branch\
%%product_release       %product_release\
%%product_arch          %product_arch\
%%product_product       %1\
\
%{?unstable}\
EOF\
 \
mkdir -p %buildroot%_sysconfdir/sysconfig \
cat > %buildroot%_sysconfdir/sysconfig/system <<EOF \
SECURITY=3\
CLASS=beginner\
LIBSAFE=no\
META_CLASS=download\
EOF\


%release_package default
%release_package -s One
Conflicts: mandriva-release-Discovery mandriva-release-Flash mandriva-release-Free mandriva-release-Powerpack mandriva-release-Powerpack+
%release_package -s Flash
Conflicts: mandriva-release-Discovery mandriva-release-Free mandriva-release-One mandriva-release-Powerpack mandriva-release-Powerpack+
%release_package -s Free
Conflicts: mandriva-release-Discovery mandriva-release-Flash mandriva-release-One mandriva-release-Powerpack mandriva-release-Powerpack+
%release_package -s Discovery
Conflicts: mandriva-release-Flash mandriva-release-Free mandriva-release-One mandriva-release-Powerpack mandriva-release-Powerpack+
%release_package -s Powerpack
Conflicts: mandriva-release-Discovery mandriva-release-Flash mandriva-release-Free mandriva-release-One mandriva-release-Powerpack+
%release_package -s Powerpack+
Conflicts: mandriva-release-Discovery mandriva-release-Flash mandriva-release-Free mandriva-release-One mandriva-release-Powerpack

%release_descr default
%release_descr -s Flash
%release_descr -s One
%release_descr -s Free
%release_descr -s Discovery
%release_descr -s Powerpack
%release_descr -s Powerpack+

%prep
%setup -q -n %{name}
cp -a %SOURCE3 CREDITS
cp -a %SOURCE4 release-notes.txt
cp -a %SOURCE5 README.urpmi

# check that CREDITS file is in UTF-8, fail otherwise
if iconv -f utf-8 -t utf-8 < CREDITS > /dev/null
then
	true
else
	echo "the CREDITS file *MUST* be encoded in UTF-8"
	echo "please fix it before continuing"
	false
fi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot/etc
echo "Mandriva Linux release %{realversion} (%{distrib}) for %{_target_cpu}" > $RPM_BUILD_ROOT/etc/mandriva-release
ln -sf mandriva-release $RPM_BUILD_ROOT/etc/redhat-release
ln -sf mandriva-release $RPM_BUILD_ROOT/etc/mandrake-release
ln -sf mandriva-release $RPM_BUILD_ROOT/etc/release
ln -sf mandriva-release $RPM_BUILD_ROOT/etc/mandrakelinux-release
echo "%{version}.0 %{rel} %{distname}" > $RPM_BUILD_ROOT/etc/version

mkdir -p %buildroot%_sysconfdir/profile.d
install -m755 %SOURCE1 %SOURCE2 %buildroot%_sysconfdir/profile.d

%release_install Free
%release_install Discovery Discovery
%release_install Flash Flash
%release_install One One
%release_install Powerpack Powerpack
%release_install Powerpack+ Powerpack+

touch %buildroot%_sysconfdir/product.id


%check
%if %am_i_cooker
case %release in
    0.*) ;;
    *)
    echo "Cooker distro should have this package with release < %{mkrel 1}"
    exit 1
    ;;
esac
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%release_post -s Flash
%release_post -s Free
%release_post -s Discovery
%release_post -s One 
%release_post -s Powerpack
%release_post -s Powerpack+ Powerpack+

%define release_files(s:) \
%files %{-s:%{-s*}} \
%defattr(-,root,root) \
%_sys_macros_dir/%{1}.macros \
/etc/product.id.%1 \
%ghost /etc/product.id\
\

%release_files -s Flash Flash
%release_files -s Free Free
%release_files -s Discovery Discovery
%release_files -s One One
%release_files -s Powerpack Powerpack
%release_files -s Powerpack+ Powerpack+


%files common
%defattr(-,root,root)
%doc CREDITS distro.txt README.urpmi release-notes.txt
/etc/mandrake-release
/etc/mandrakelinux-release
/etc/redhat-release
/etc/mandriva-release
/etc/release
/etc/version
/etc/profile.d/10mandriva-release.sh
/etc/profile.d/10mandriva-release.csh
%config(noreplace) %verify(not md5 size mtime) %_sysconfdir/sysconfig/system



