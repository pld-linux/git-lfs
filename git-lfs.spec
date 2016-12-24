#
# Conditional build:
%bcond_with	tests		# build without tests
%bcond_without	doc		# build manual page

Summary:	Git extension for versioning large files
Name:		git-lfs
Version:	1.5.3
Release:	1
License:	MIT
Group:		Applications/Archiving
Source0:	https://github.com/github/git-lfs/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	10c5acfaecfefd26c2e77d6747621425
URL:		https://git-lfs.github.com/
BuildRequires:	git-core
BuildRequires:	golang
BuildRequires:	groff
%{?with_doc:BuildRequires:	ronn}
Requires:	git-core >= 1.8.5
ExclusiveArch:	%{ix86} %{x8664} %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		import_path	github.com/git-lfs/%{name}

%ifarch %{ix86}
%define GOARCH 386
%endif
%ifarch %{x8664}
%define GOARCH amd64
%endif

%description
Git Large File Storage (LFS) replaces large files such as audio
samples, videos, datasets, and graphics with text pointers inside Git,
while storing the file contents on a remote server like GitHub.com or
GitHub Enterprise.

%prep
%setup -qc

# preserve for %doc
mv %{name}-%{version}/*.md .

install -d src/$(dirname %{import_path})
mv %{name}-%{version} src/%{import_path}

%build
unset GOROOT
export GOPATH=$(pwd)
export GOARCH=%{GOARCH}

cd src/%{import_path}
sh -x ./script/bootstrap

%if %{with doc}
./script/man
%endif

%if %{with tests}
# ensure there are no GIT env vars for testing
env | grep GIT_ && exit 3

./script/test
./script/integration
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

cd src/%{import_path}
install -p bin/git-lfs $RPM_BUILD_ROOT%{_bindir}/git-lfs
%if %{with doc}
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md ROADMAP.md CHANGELOG.md
%attr(755,root,root) %{_bindir}/git-lfs
%{?with_doc:%{_mandir}/man1/*.1*}
