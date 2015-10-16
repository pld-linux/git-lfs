#
# Conditional build:
%bcond_with	tests		# build without tests
%bcond_with	doc		# build manual page

Summary:	Git extension for versioning large files
Name:		git-lfs
Version:	1.0.0
Release:	1
License:	MIT
Group:		Applications/Archiving
Source0:	https://github.com/github/git-lfs/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c05a2a2947b56fb0d7e2ede15d47a86c
URL:		https://git-lfs.github.com/
BuildRequires:	git-core
BuildRequires:	golang
%{?with_doc:BuildRequires:	ruby-ronn}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0

%description
Git Large File Storage (LFS) replaces large files such as audio
samples, videos, datasets, and graphics with text pointers inside Git,
while storing the file contents on a remote server like GitHub.com or
GitHub Enterprise.

%prep
%setup -q
mkdir -p src/github.com/github
ln -s $(pwd) src/github.com/github/%{name}

%build
export GOPATH=$(pwd)
%ifarch %{ix86}
	GOARCH=386 ./script/bootstrap
%endif
%ifarch %{x8664}
	GOARCH=amd64 ./script/bootstrap
%endif

%if %{with doc}
./script/man
%endif

%if %{with tests}
./script/test
./script/integration
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

install -p bin/git-lfs $RPM_BUILD_ROOT%{_bindir}/git-lfs
%if %{with doc}
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%attr(755,root,root) %{_bindir}/git-lfs
%{?with_doc:%{_mandir}/man1/*.1*}
