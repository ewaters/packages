%filter_from_provides /.*/d
%filter_setup

Name:           rock-runtime-python33
Version:        1
Release:        2%{?dist}
Summary:        python33 runtime for rock

Group:          Development/Languages
License:        MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rock-runtime-python33-core-rpmbuild
Requires:       rock-runtime-python33-core >= 3.3.0-1
Requires:       rock-runtime-python33-distribute-setup >= 0.6.34-1

%description
python33 runtime for rock.

%prep

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{python33_rootdir}

cat << EOF > %{buildroot}%{python33_rootdir}/rock.yml
env:
  PATH: "%{python33_rootdir}/usr/bin:\${PATH}"
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python33_rootdir}/rock.yml

%changelog
* Sun Feb 03 2013 Silas Sewell <silas@sewell.org> - 1-2
- distribute-setup 0.6.34-1

* Sat Sep 29 2012 Silas Sewell <silas@sewell.org> - 1-1
- Initial build
