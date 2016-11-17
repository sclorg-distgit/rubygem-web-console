%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from web-console-2.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name web-console

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.2.1
Release: 3%{?dist}
Summary: A debugging tool for your Ruby on Rails applications
Group: Development/Languages
License: MIT
URL: https://github.com/rails/web-console
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/web-console.git && cd web-console
# git checkout v2.2.1 && tar czvf web-console-2.2.1-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
Requires:      %{?scl_prefix}rubygem(railties) >= 4.0
Requires:      %{?scl_prefix}rubygem(activemodel) >= 4.0
Requires:      %{?scl_prefix}rubygem(sprockets-rails) >= 2.0
Requires:      %{?scl_prefix}rubygem(sprockets-rails) < 4.0
Requires:      %{?scl_prefix}rubygem(binding_of_caller) >= 0.7.2
BuildRequires: %{?scl_prefix}rubygem(binding_of_caller)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(mocha)
BuildRequires: %{?scl_prefix}rubygem(rails)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
A debugging tool for your Ruby on Rails applications.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

# We don't care about code coverage.
sed -i '/imple.ov/ s/^/#/' test/test_helper.rb

# Couldn't find a way how to execute the test suite without Bundler,
# so give it some reasonable Gemfile.
cat << \EOF > Gemfile
source 'https://rubygems.org'

gem 'binding_of_caller'
gem 'mocha', require: false
gem 'rails'
gem 'sqlite3'
EOF

%{?scl:scl enable %{scl} - << \EOF}
ruby -Itest -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.markdown
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile

%changelog
* Thu Mar 03 2016 Pavel Valena <pvalena@redhat.com> - 2.2.1-3
- Add scl macros
  - Resolves: rhbz#1317080

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 22 2015 Vít Ondruch <vondruch@redhat.com> - 2.2.1-1
- Update to web-console 2.2.1.

* Fri Jun 19 2015 Vít Ondruch <vondruch@redhat.com> - 2.1.3-1
- Update to web-console 2.1.3.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Vít Ondruch <vondruch@redhat.com> - 2.0.0-1
- Initial package
