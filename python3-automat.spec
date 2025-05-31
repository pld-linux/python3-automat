#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Self-service finite-state machines for the programmer on the go
Summary(pl.UTF-8):	Bezobsługowe automaty skończone dla programisty w biegu
Name:		python3-automat
Version:	24.8.1
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/automat/
Source0:	https://files.pythonhosted.org/packages/source/a/automat/automat-%{version}.tar.gz
# Source0-md5:	c023f8848366053a76f99cffba3ea34e
Patch0:		no-git.patch
URL:		https://pypi.org/project/Automat/
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-setuptools >= 1:35.0.2
BuildRequires:	python3-setuptools_scm
BuildRequires:	python3-wheel >= 0.29.0
%if %{with tests}
BuildRequires:	python3-attrs >= 19.2.0
BuildRequires:	python3-graphviz >= 0.5.2
BuildRequires:	python3-pytest
BuildRequires:	python3-twisted >= 16.1.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-pydoctor
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Automat is a library for concise, idiomatic Python expression of
finite-state automata (particularly deterministic finite-state
transducers).

%description -l pl.UTF-8
Automat to biblioteka do zwięzłego wyrażania automatów skończonych (w
szczególności deterministycznych automatów skończończonych z wyjściem,
tj. transduktorów) w Pythonie.

%package apidocs
Summary:	API documentation for Python automat module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona automat
Group:		Documentation

%description apidocs
API documentation for Python automat module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona automat.

%prep
%setup -q -n automat-%{version}
%patch -P0 -p1

%{__sed} -i -e 's/@@VERSION@@/%{version}/' docs/conf.py

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest automat/_test
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
PYTHONPATH=$(pwd)/build-3-doc \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/automat-visualize{,-3}
ln -sf automat-visualize-3 $RPM_BUILD_ROOT%{_bindir}/automat-visualize
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-automat-%{version}
cp -p docs/examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-automat-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/automat-visualize
%attr(755,root,root) %{_bindir}/automat-visualize-3
%{py3_sitescriptdir}/automat
%{py3_sitescriptdir}/automat-%{version}.dist-info
%{_examplesdir}/python3-automat-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,*.html,*.js}
%endif
