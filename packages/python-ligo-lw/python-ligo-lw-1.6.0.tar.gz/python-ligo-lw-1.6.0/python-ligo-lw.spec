Name: 		python-ligo-lw
Summary:	LIGO Light-Weight XML I/O Library
Version:	1.6.0
Release:	1%{?dist}
License:	GPL
Group:		Development/Libraries
Source:		%{name}-%{version}.tar.gz
Url:		https://git.ligo.org/kipp.cannon/python-ligo-lw
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:  python-devel
BuildRequires:  python2-ligo-common
Requires:	glue
Requires:	python >= 2.7
Requires:	python-dateutil
Requires:	python-six
Requires:	python2-lal
# temporarily commented out to break cyclic dependency.  lalburst is an
# optional dependency, but the rpm version at CIT is too old for that
# feature
#Requires:	python2-lalburst
Requires:	python2-ligo-common
Requires:	python2-ligo-segments
Requires:	PyYAML
Conflicts:	glue-ligolw-tools
Obsoletes:	glue-ligolw-tools
Provides:	glue-ligolw-tools
Conflicts:	glue < 2.0 python-pylal
Prefix:         %{_prefix}
%description
The LIGO Light-Weight XML format is widely used within gravitational-wave
data analysis pipelines.  This package provides a Python library to read,
write, and interact with documents in this format.

%prep
%setup

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 \
        --skip-build \
        --root=%{buildroot} \
        --prefix=%{_prefix}
rm -rf $RPM_BUILD_ROOT/%{_prefix}/lib*/python*/site-packages/ligo/*.*
rm -rf $RPM_BUILD_ROOT/%{_prefix}/lib*/python*/site-packages/*.egg-info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/lib*/python*/site-packages/ligo/lw

%changelog
*  Tue May 8 2018 Kipp Cannon <kipp.cannon@ligo.org>
- Initial release.
