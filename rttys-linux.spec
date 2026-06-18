Name:           rttys-linux
Version:        1.0
Release:        1%{?dist}
Summary:        RTTY TCP + WebUI server (no SDR)

License:        MIT
BuildArch:      noarch

Requires:       python3, python3-flask, nc

%description
RTTY server similar to rttys-windows.
Provides TCP stream on 5912 and Web UI on 5913.

%install
mkdir -p %{buildroot}/opt/rttys-linux/app
cp -r app/* %{buildroot}/opt/rttys-linux/app/

mkdir -p %{buildroot}/etc/systemd/system
cp rttys.service %{buildroot}/etc/systemd/system/

%files
/opt/rttys-linux
/etc/systemd/system/rttys.service

%post
systemctl daemon-reload
systemctl enable rttys

%postun
systemctl daemon-reload

%changelog
* Wed Jun 17 2026 Georgios Demelis <your@email.com> - 1.0-1
- Initial release
