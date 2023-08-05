# Initial packages

By default the `packages` command lists packages in the `gpkg`
namespace). We don't have any installed yet so this is an empty list.

    >>> run("guild packages")
    <BLANKLINE>
    <exit 0>

If we use the `-a` option, we get all packages, which at this point
consists of all of the pip packages that are installed in the env.

Note that we're cutting (showing) only col 1 to avoid using any `...`
to match versions and descriptions (`...` matches across lines, which
leaves room for false positives).

    >>> run("guild packages -a", cut=[0],
    ...     # Some additional Python 2 packages land that we just
    ...     # ignore in our list below.
    ...     ignore=["enum34", "futures", "ipaddress"]) # doctest: +REPORT_UDIFF
    Jinja2
    Markdown
    MarkupSafe
    Pillow
    PyYAML
    Werkzeug
    absl-py
    cachetools
    certifi
    chardet
    click
    daemonize
    docutils
    google-auth
    google-auth-oauthlib
    grpcio
    guildai
    idna
    numpy
    oauthlib
    pip
    pkginfo
    protobuf
    psutil
    pyasn1
    pyasn1-modules
    requests
    requests-oauthlib
    rsa
    scikit-learn
    scikit-optimize
    scipy
    setuptools
    six
    tabview
    tensorboard
    urllib3
    virtualenv
    wheel
    <exit 0>
