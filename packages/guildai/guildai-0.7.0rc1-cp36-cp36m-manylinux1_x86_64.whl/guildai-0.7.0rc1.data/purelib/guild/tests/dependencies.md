# Dependencies

Guild dependencies are managed by the `deps` module:

    >>> from guild import deps

The primary function of `deps` is to resolve dependencies defined in
operations.

To illustrate, we'll define a model operation that requires a
resource:

    >>> gf = guildfile.for_string("""
    ... - model: sample
    ...   operations:
    ...    test:
    ...      main: <not used>
    ...      requires: data
    ...   resources:
    ...     data:
    ...       sources:
    ...       - abc.txt
    ...       - file: def.txt
    ...       - url: http://foo.com/bar.tar.gz
    ...       - operation: foo/bar:baz
    ... """, "test")

We can get the list of dependencies for an operation with the
`dependencies` attribute:

    >>> test_op = gf.models["sample"]["test"]
    >>> test_op.dependencies
    [<guild.guildfile.OpDependencyDef 'data'>]

The value of `requires` may be a single string or a list of
strings. Each string must be a reference to a model resource. Multiple
values indicate that all resources must be met.

Resource labels may be one of the following types:

- Resource in defined in the operation model
- Resource defined in anothet model in the guildfile
- Resource defined in a model provided by a package

Labels have this grammar:

    [ ( [ PACKAGE '/' ] MODEL ':' ) | ( PACKAGE '/' MODEL ) ] NAME

Where `NAME` is the resource name, `MODEL` is the model the resource
is defined in, and `PACKAGE` is the package containing the model
resource. When referring to a package resource, the model may be
omitted provided there is only one resource with `NAME` provided by
the package.

Here are some examples of dependencies:

| Example           | Dependency                                            |
|-------------------|-------------------------------------------------------|
| data              | resource `data` in the current model                  |
| common:data       | on resource `data` in model `common` in the guildfile |
| mnist/common:data | on `common:data` resource in package `mnist`          |
| mnist/data        | on `data` resource in package `mnist`                 |

Let's look at the required resource:

    >>> data_res = gf.models["sample"].get_resource("data")

This resource has the following sources:

    >>> data_res.sources
    [<guild.resourcedef.ResourceSource 'file:abc.txt'>,
     <guild.resourcedef.ResourceSource 'file:def.txt'>,
     <guild.resourcedef.ResourceSource 'http://foo.com/bar.tar.gz'>,
     <guild.resourcedef.ResourceSource 'operation:foo/bar:baz'>]

## Operation sources

The sample `data` resource above provides a source generated from an
operation. These are known as *operation sources*.

Operation sources must reference a model operation. The operation may
be defined for the source model, another model in the guildfile, or a
model defined in a package. Operation references must be in a format
that can be parsed using `op.OpRef.for_string`.

    >>> from guild.opref import OpRef

`OpRef.for_string` returns a `OpRef` instance if the string can be
parsed as an op ref or raises an exception if it cannot.

Below are various examples.

Operation name only:

    >>> OpRef.for_string("foo")
    OpRef(pkg_type=None,
          pkg_name=None,
          pkg_version=None,
          model_name=None,
          op_name='foo')

Operation of a model in the same guildfile:

    >>> OpRef.for_string("foo:bar")
    OpRef(pkg_type=None,
          pkg_name=None,
          pkg_version=None,
          model_name='foo',
          op_name='bar')

Operation in a packaged model:

    >>> OpRef.for_string("foo/bar:baz")
    OpRef(pkg_type=None,
          pkg_name='foo',
          pkg_version=None,
          model_name='bar',
          op_name='baz')

Some invalid op references:

    >>> OpRef.for_string("")
    Traceback (most recent call last):
    OpRefError: invalid reference: ''

    >>> OpRef.for_string("foo/bar")
    Traceback (most recent call last):
    OpRefError: invalid reference: 'foo/bar'

Here's a helper function to return OpRefs for a give sample run.

    >>> from guild import run as runlib
    >>> def for_run(id):
    ...     path = join_path(sample("opref-runs"), id)
    ...     return runlib.Run(id, path).opref

Below are various examples.

    >>> for_run("guildfile")
    OpRef(pkg_type='guildfile',
          pkg_name='/foo/bar',
          pkg_version='7253deeeaeb6dc85466cf691facff24e',
          model_name='test',
          op_name='go')

    >>> for_run("package")
    OpRef(pkg_type='package',
          pkg_name='fashion',
          pkg_version='1.0',
          model_name='fashion',
          op_name='train')

    >>> for_run("with_space")
    OpRef(pkg_type='guildfile',
          pkg_name='/foo/project with spaces',
          pkg_version='7253deeeaeb6dc85466cf691facff24e',
          model_name='test',
          op_name='go')

    >>> for_run("invalid")
    Traceback (most recent call last):
    OpRefError: invalid opref for run 'invalid'
    (.../samples/opref-runs/invalid): not a valid opref

OpRefs are encoded by converting them to strings.

    >>> str(OpRef("type", "pkg", "ver", "model", "op"))
    'type:pkg ver model op'

If the package name contains a space, it's quoted:

    >>> str(OpRef("type", "pkg with spaces", "ver", "model", "op"))
    "type:'pkg with spaces' ver model op"

OpRefs are compared using their string representations:

    >>> for _ in range(100):
    ...     # If OpRef is using object __cmp__ then this should fail
    ...     # over 100 attempts.
    ...     assert OpRef("", "", "", "", "a") < OpRef("", "", "", "", "b")

## Resolvers

Resolvers are objects that resolve dependency sources. Resolvers can
be obtained for a source via a resource def using
`guild.resolver.for_resdef_source`.

    >>> from guild.resolver import for_resdef_source as get_resolver

To illustrate, we'll use a sample project that defines various
resources.

    >>> gf = guildfile.for_dir(sample("projects/resources"))
    >>> res_model = gf.models["resources"]

Here are the model resources:

    >>> res_model.resources
    [<guild.guildfile.ResourceDef 'test'>,
     <guild.guildfile.ResourceDef 'test2'>,
     <guild.guildfile.ResourceDef 'test3'>,
     <guild.guildfile.ResourceDef 'test4'>]

The test resource has the following sources:

    >>> test_resdef = res_model.get_resource("test")
    >>> test_resdef.sources
    [<guild.resourcedef.ResourceSource 'file:archive1.zip'>,
     <guild.resourcedef.ResourceSource 'file:archive2.tar'>,
     <guild.resourcedef.ResourceSource 'file:archive3.tar'>,
     <guild.resourcedef.ResourceSource 'file:test.txt'>,
     <guild.resourcedef.ResourceSource 'file:badhash.txt'>,
     <guild.resourcedef.ResourceSource 'file:files'>,
     <guild.resourcedef.ResourceSource 'file:files'>,
     <guild.resourcedef.ResourceSource 'file:doesnt-exist'>,
     <guild.resourcedef.ResourceSource 'file:test.txt'>]

In the tests below, we'll use a resolver to resolve each source.

In addition to a source, a resolver needs a resource (see
`guild.deps.Resource`), which is a live representation of the resource
definition. The resource provides additional context to the resolver,
including resource location, the operation that requires the resource,
and additional configuration that may be provided for the resolution
process.

Let's create a resource for our resolvers. The resource requires a
resource def, a location, which is the sample project directory, and a
context.

    >>> test_location = sample("projects/resources")
    >>> test_ctx = deps.ResolutionContext(
    ...   target_dir=None,
    ...   opdef=None,
    ...   resource_config={})

    >>> test_res = deps.Resource(test_resdef, test_location, test_ctx)

### Zip source file

    >>> zip_source = test_resdef.sources[0]
    >>> zip_source.uri
    'file:archive1.zip'

By default, archives are unpacked. See *No unpack archive* below for
an example of an archive that isn't unpacked.

    >>> zip_source.unpack
    True

If a `sha256` hash is specified, the file will be verified before
use. See *Invalid source file* below for an example of a file with an
invalid hash.

    >>> zip_source.sha256
    '8d172fde27ec89ae0a76832f8ff714e3e498b23d14bac7edfb55e3c4729e3265'

    >>> zip_source.select
    [SelectSpec(pattern='a.txt', reduce=None)]

    >>> resolver = get_resolver(zip_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> log = LogCapture()
    >>> with log:
    ...   resolver.resolve(unpack_dir)
    ['/.../a.txt']

    >>> log.print_all()
    Unpacking .../samples/projects/resources/archive1.zip

    >>> dir(unpack_dir)
    ['.guild-cache-archive1.zip.unpacked', 'a.txt', 'b.txt']

`.guild-cache-FILE.unpacked` is used by Guild to avoid re-scanning the
archive `FILE` for members. For large archives, this saves a lot of
time.

Note that `b.txt` was also extracted into the temp directory. This is
by design - a resource is always fully unpacked when resolved. Files
are selected by way of the source files returned by `resolve`.

### Tar source file

    >>> tar_source = test_resdef.sources[1]
    >>> tar_source.uri
    'file:archive2.tar'

    >>> tar_source.unpack
    True

    >>> print(tar_source.sha256)
    None

    >>> print(tar_source.select)
    []

    >>> resolver = get_resolver(tar_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> log = LogCapture()
    >>> with log:
    ...   sorted(resolver.resolve(unpack_dir))
    ['/.../c.txt', '/.../d.txt']

    >>> log.print_all()
    Unpacking .../samples/projects/resources/archive2.tar

    >>> dir(unpack_dir)
    ['.guild-cache-archive2.tar.unpacked', 'c.txt', 'd.txt']

### No unpack archive

    >>> nounpack_source = test_resdef.sources[2]
    >>> nounpack_source.uri
    'file:archive3.tar'

This source should not be unpacked:

    >>> nounpack_source.unpack
    False

    >>> print(nounpack_source.sha256)
    None

    >>> print(nounpack_source.select)
    []

    >>> resolver = get_resolver(nounpack_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> resolver.resolve(unpack_dir)
    ['.../samples/projects/resources/archive3.tar']

    >>> dir(unpack_dir)
    []

Note the source file is a path directly to the archive and not an
extracted file.

### Plain source file

    >>> plain_source = test_resdef.sources[3]
    >>> plain_source.uri
    'file:test.txt'

    >>> plain_source.sha256
    'f33ae3bc9a22cd7564990a794789954409977013966fb1a8f43c35776b833a95'

    >>> resolver = get_resolver(plain_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> resolver.resolve(unpack_dir)
    ['.../samples/projects/resources/test.txt']

    >>> dir(unpack_dir)
    []

### Invalid source file

    >>> invalid_source = test_resdef.sources[4]
    >>> invalid_source.uri
    'file:badhash.txt'

    >>> invalid_source.sha256
    'xxx'

    >>> resolver = get_resolver(invalid_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> resolver.resolve(unpack_dir)
    Traceback (most recent call last):
    ResolutionError: '.../samples/projects/resources/badhash.txt' has an unexpected
    sha256 (expected xxx but got ...)

    >>> dir(unpack_dir)
    []

### Directory source file

When a file is a directory and it doesn't specify a `select`
attribute, just the directory path is resolved:

    >>> dir_source = test_resdef.sources[5]
    >>> dir_source.uri
    'file:files'
    >>> dir_source.select
    []

    >>> resolver = get_resolver(dir_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> sorted(resolver.resolve(unpack_dir))
    ['.../samples/projects/resources/files']

    >>> dir(unpack_dir)
    []

When a file is a directory and specifies a `select`, files that are
selected from the directory are resolved:

    >>> dir_source = test_resdef.sources[6]
    >>> dir_source.uri
    'file:files'
    >>> dir_source.select # doctest: -NORMALIZE_PATHS
    [SelectSpec(pattern='.+\\.txt', reduce=None)]

    >>> resolver = get_resolver(dir_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> sorted(resolver.resolve(unpack_dir))
    ['.../samples/projects/resources/files/e.txt',
     '.../samples/projects/resources/files/f.txt']

    >>> dir(unpack_dir)
    []

### Non existing source file

Non-existing files generate an error when resolved:

    >>> noexist_source = test_resdef.sources[7]
    >>> noexist_source.uri
    'file:doesnt-exist'

    >>> resolver = get_resolver(noexist_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> resolver.resolve(unpack_dir)
    Traceback (most recent call last):
    ResolutionError: cannot find source file doesnt-exist

    >>> dir(unpack_dir)
    []

### Renaming sources

The `rename` attribute can be used to rename resolved sources.

    >>> rename_source = test_resdef.sources[8]
    >>> rename_source.uri
    'file:test.txt'

The rename attr can be a string or a list of strings. Each string
contains two parts, each part separated by a space. If a part contains
spaces it must be quoted.

Here's the rename spec for our source:

    >>> rename_source.rename # doctest: -NORMALIZE_PATHS
    [RenameSpec(pattern='(.+)\\.txt', repl='\\1.config')]

Resolve doesn't apply renames - it just resolves the source locations.

    >>> resolver = get_resolver(rename_source, test_res)
    >>> unpack_dir = mkdtemp()
    >>> resolver.resolve(unpack_dir)
    ['.../samples/projects/resources/test.txt']

    >>> dir(unpack_dir)
    []

### test3 resource

The `test3` resource contains a more complex rename spec.

    >>> test3_resdef = res_model.get_resource("test3")
    >>> test3_resdef.sources
    [<guild.resourcedef.ResourceSource 'file:files'>,
     <guild.resourcedef.ResourceSource 'file:files'>,
     <guild.resourcedef.ResourceSource 'file:archive1.zip'>,
     <guild.resourcedef.ResourceSource 'file:archive2.tar'>]

A resource to resolve sources with:

    >>> test3_res = deps.Resource(test3_resdef, test_location, test_ctx)

### Renamed directory

The first source specifies the `files` directory but renames it to
`all_files`.

    >>> all_files = test3_resdef.sources[0]
    >>> all_files
    <guild.resourcedef.ResourceSource 'file:files'>

    >>> print(all_files.path)
    None

    >>> all_files.select
    []

    >>> all_files.rename
    [RenameSpec(pattern='files', repl='all_files')]

    >>> test_ctx.target_dir = mkdtemp()
    >>> test3_res.resolve_source(all_files)
    ['.../samples/projects/resources/files']

    >>> find(test_ctx.target_dir)
    all_files

### bin files

The second source selects *.bin files from `files` and renames them to
strip off the `.bin` suffix. The files are additionally stored in a
`bin` directory (path).

    >>> bin_files = test3_resdef.sources[1]
    >>> bin_files
    <guild.resourcedef.ResourceSource 'file:files'>

    >>> print(bin_files.path)
    bin

    >>> bin_files.select # doctest: -NORMALIZE_PATHS
    [SelectSpec(pattern='.+\\.bin', reduce=None)]

    >>> bin_files.rename
    [RenameSpec(pattern='.bin', repl='')]

    >>> test_ctx.target_dir = mkdtemp()
    >>> test3_res.resolve_source(bin_files)
    ['.../samples/projects/resources/files/a.bin']

    >>> find(test_ctx.target_dir)
    bin/a

### archive1 text files

The third source selects text files from `archive1.zip`, stores them
in an `archive1` directory (path) and adds a `2` to their basename.

    >>> archive1_txt_files = test3_resdef.sources[2]
    >>> archive1_txt_files
    <guild.resourcedef.ResourceSource 'file:archive1.zip'>

    >>> print(archive1_txt_files.path)
    archive1

    >>> archive1_txt_files.select # doctest: -NORMALIZE_PATHS
    [SelectSpec(pattern='.+\\.txt', reduce=None)]

    >>> archive1_txt_files.rename # doctest: -NORMALIZE_PATHS
    [RenameSpec(pattern='(.+)\\.txt', repl='\\g<1>2.txt')]

    >>> test_ctx.target_dir = mkdtemp()
    >>> unpack_dir = mkdtemp()
    >>> with LogCapture() as logs:
    ...   test3_res.resolve_source(archive1_txt_files, unpack_dir)
    ['.../a.txt', '.../b.txt']

    >>> logs.print_all()
    Unpacking .../samples/projects/resources/archive1.zip

    >>> find(test_ctx.target_dir)
    archive1/a2.txt
    archive1/b2.txt

### All archive2 files

The fourth source selects all of the files from `archive2.tar` and
renames them with an `archive2_` prefix.

    >>> archive2_files = test3_resdef.sources[3]
    >>> archive2_files
    <guild.resourcedef.ResourceSource 'file:archive2.tar'>

    >>> print(archive2_files.path)
    None

    >>> archive2_files.select
    []

    >>> archive2_files.rename # doctest: -NORMALIZE_PATHS
    [RenameSpec(pattern='(.+)', repl='archive2_\\1')]

    >>> test_ctx.target_dir = mkdtemp()
    >>> unpack_dir = mkdtemp()
    >>> with LogCapture() as logs:
    ...   resolved = test3_res.resolve_source(archive2_files, unpack_dir)
    ...   sorted(resolved)
    ['.../c.txt', '.../d.txt']

    >>> logs.print_all()
    Unpacking .../samples/projects/resources/archive2.tar

    >>> find(test_ctx.target_dir)
    archive2_c.txt
    archive2_d.txt

### Config sources

The test4 resource contains a config sources. We'll use those to
illustrate the config source type.

    >>> test4_resdef = res_model.get_resource("test4")
    >>> test4_resdef.sources
    [<guild.resourcedef.ResourceSource 'config:config.yml'>,
     <guild.resourcedef.ResourceSource 'config:config.yml'>,
     <guild.resourcedef.ResourceSource 'config:config.yml'>]

A resource to resolve sources with:

    >>> test4_res = deps.Resource(test4_resdef, test_location, test_ctx)

Let's resolve each source in turn. First we need a target directory.

    >>> test_ctx.target_dir = mkdtemp()

#### Simple config

The first config source simply resolves the source file as is.

    >>> simple_config = test4_resdef.sources[0]

    >>> resolved = test4_res.resolve_source(simple_config)
    >>> resolved
    ['.../.guild/generated/.../config.yml']

The resolved source is generated under the run directory:

    >>> resolved[0].startswith(test_ctx.target_dir)
    True

Here's another view with the resolved link to the generated config:

    >>> find(test_ctx.target_dir)
    .guild/generated/.../config.yml
    config.yml

And the config:

    >>> cat(join_path(test_ctx.target_dir, "config.yml"))
    a: 1
    b: 2
    c:
      d: 3

Here the config is the same as the source:

    >>> cat(sample("projects/resources/config.yml"))
    a: 1
    b: 2
    c:
      d: 3

#### Renamed config with flags

The second config is renamed:

    >>> renamed_config = test4_resdef.sources[1]
    >>> renamed_config.rename
    [RenameSpec(pattern='config', repl='c2')]

When we resolve this source, we'll apply flag values. Flag values are
provided by way of the resource context.

In our previous tests, the context does not provide an operation def:

    >>> print(test_ctx.opdef)
    None

Let's provide an operation def that has some flag values. We'll use a
proxy.

    >>> class OpDefProxy(object):
    ...
    ...   def __init__(self, flags):
    ...     self._flags = flags
    ...
    ...   def flag_values(self):
    ...     return self._flags
    ...
    ...   @staticmethod
    ...   def get_flagdef(_name):
    ...     return None

And set some flag values that will be used when resolving the config
file:

    >>> test_ctx.opdef = OpDefProxy({
    ...   "a": 11,
    ...   "b": "22",
    ...   "c.d": 33
    ... })

Let's resolve the config source:

    >>> resolved = test4_res.resolve_source(renamed_config)
    >>> resolved
    ['.../.guild/generated/.../config.yml']

Here's the target dir:

    >>> find(test_ctx.target_dir)
    .guild/generated/.../config.yml
    .guild/generated/.../config.yml
    c2.yml
    config.yml

Note the second generated config. Generated config files are created
under a unique directory of `.guild/generated` to ensure that their
base names are preserved.

Here's the resolved and renamed config file:

    >>> cat(join_path(test_ctx.target_dir, "c2.yml"))
    a: 11
    b: '22'
    c:
      d: 33

Note that the flag values are applied to each of the applicable config
values using the "nested flags" syntax, which uses dots to delimit
config levels (see flag names above).

#### Config with params

Out third source defines params that are applied to config.

    >>> param_config = test4_resdef.sources[2]
    >>> pprint(param_config.params)
    {'a': 111, 'c.d': 333}

This source is also stored under a path:

    >>> param_config.path
    'c3'

To see how params are applied, let's first reset our context to use no
flags.

    >>> test_ctx.opdef = None

Let's resolve the config source:

    >>> resolved = test4_res.resolve_source(param_config)
    >>> resolved
    ['.../.guild/generated/.../config.yml']

Here's the target dir:

    >>> find(test_ctx.target_dir)
    .guild/generated/.../config.yml
    .guild/generated/.../config.yml
    .guild/generated/.../config.yml
    c2.yml
    c3/config.yml
    config.yml

Again, note the third generated config.

Here's the resolved config under a path:

    >>> cat(join_path(test_ctx.target_dir, "c3/config.yml"))
    a: 111
    b: 2
    c:
      d: 333

Note the new values for `a` and `c.d` -- these values are provided by
the params (see above).

We can redefine params using flags. Let's re-resolve with flags for
our context.

    >>> test_ctx.opdef = OpDefProxy({"b": 222, "c.d": 444})

We'll also use a new target directory since we've already resolve this
source.

    >>> test_ctx.target_dir = mkdtemp()

Let's resolve the source:

    >>> test4_res.resolve_source(param_config)
    [...]

Here's our target directory:

    >>> find(test_ctx.target_dir)
    .guild/generated/.../config.yml
    c3/config.yml

And the resolved config:

    >>> cat(join_path(test_ctx.target_dir, "c3/config.yml"))
    a: 111
    b: 222
    c:
      d: 444

## Resolving sources

NOTE: These tests modify `test_resdef` sources (defined above) in
place. Any tests on the original source list should be run before
these tests.

In these tests we'll resolve some sources to our target
directory. We'll modify `test_resdef` with resolvable sources and
modify `test_ctx` with new target directories so we can see the
resolution results.

### Plain source file

Here's `plain_source` resolved:

    >>> test_resdef.sources = [plain_source]
    >>> test_ctx.target_dir = mkdtemp()
    >>> test_res.resolve()
    ['.../samples/projects/resources/test.txt']

The target directory contains a link to the resolved file.

    >>> dir(test_ctx.target_dir)
    ['test.txt']

    >>> realpath(join_path(test_ctx.target_dir, "test.txt")) # doctest: -WINDOWS
    '.../samples/projects/resources/test.txt'

Note that under Windows os.path.realpath doesn't reliably resolve
symlink paths (see https://bugs.python.org/issue9949).

### Tar source file

Here's the resolved tar source. We'll use a temp directory for
unpacking.

    >>> unpack_dir = mkdtemp("guild-test-unpack-dir-")

And resolve the archive source:

    >>> test_resdef.sources = [tar_source]
    >>> test_ctx.target_dir = mkdtemp()
    >>> with log:
    ...   sorted(test_res.resolve(unpack_dir))
    ['.../guild-test-unpack-dir-.../c.txt',
     '.../guild-test-unpack-dir-.../d.txt']

    >>> log.print_all()
    Unpacking .../samples/projects/resources/archive2.tar

The target directory contains links to unpacked files:

    >>> dir(test_ctx.target_dir)
    ['c.txt', 'd.txt']

    >>> realpath(join_path(test_ctx.target_dir, "c.txt")) # doctest: -WINDOWS
    '.../guild-test-unpack-dir-.../c.txt'

    >>> realpath(join_path(test_ctx.target_dir, "d.txt")) # doctest: -WINDOWS
    '.../guild-test-unpack-dir-.../d.txt'

### No unpack archive

The unpack archive source resolves to the unpacked archive.

    >>> test_resdef.sources = [nounpack_source]
    >>> test_ctx.target_dir = mkdtemp()
    >>> test_res.resolve()
    ['.../samples/projects/resources/archive3.tar']

And the target directory:

    >>> dir(test_ctx.target_dir)
    ['archive3.tar']

    >>> realpath(join_path(test_ctx.target_dir, "archive3.tar")) # doctest: -WINDOWS
    '.../samples/projects/resources/archive3.tar'

### Renamed file

In this test we'll resolve `rename_source`.

    >>> test_resdef.sources = [rename_source]
    >>> test_ctx.target_dir = mkdtemp()
    >>> test_res.resolve()
    ['.../samples/projects/resources/test.txt']

Unlike the previous test, the link is renamed using the source
`rename` spec.

    >>> dir(test_ctx.target_dir)
    ['test.config']

    >>> realpath(join_path(test_ctx.target_dir, "test.config")) # doctest: -WINDOWS
    '.../samples/projects/resources/test.txt'

## Resolving sources - part 2

These tests continue testing resource resolution, but use the `test2`
resource, which specifically tests `path`

    >>> test2_resdef = res_model.get_resource("test2")
    >>> test2_resdef.sources
    [<guild.resourcedef.ResourceSource 'file:test.txt'>,
     <guild.resourcedef.ResourceSource 'file:files/a.bin'>]

To illustrate how paths are used, we'll resolve each source.

Here's the resource we'll use to resolve sources:

    >>> test2_ctx = deps.ResolutionContext(
    ...   target_dir=None,
    ...   opdef=None,
    ...   resource_config={})
    >>> test2_res = deps.Resource(test2_resdef, test_location, test2_ctx)

### Resource paths

A path may be defined for a resource:

    >>> test2_resdef.path
    'foo'

This path is used when resolving any resource sources.

Our first source:

    >>> source1 = test2_resdef.sources[0]
    >>> source1
    <guild.resourcedef.ResourceSource 'file:test.txt'>
    >>> print(source1.path)
    None

Let's resolve the source to a new temp dir:

    >>> test2_ctx.target_dir = mkdtemp()
    >>> test2_res.resolve_source(source1)
    ['.../samples/projects/resources/test.txt']

The resolved files are under the resource path `foo`:

    >>> find(test2_ctx.target_dir)
    foo/test.txt

### Source paths

A source may also have a path, in which case that path is appended to
any resource path.

Here's the second source:

    >>> source2 = test2_resdef.sources[1]
    >>> source2
    <guild.resourcedef.ResourceSource 'file:files/a.bin'>
    >>> source2.path
    'bar'

Let's resolve the source:

    >>> test2_ctx.target_dir = mkdtemp()
    >>> test2_res.resolve_source(source2)
    ['.../samples/projects/resources/files/a.bin']

The resolved files are under the resource path `foo/bar`, which is
defined by both the resource and the source:

    >>> find(test2_ctx.target_dir)
    foo/bar/a.bin

## Alternative resource defs

### Implicit sources

If a resource is defined as a list, the list is assumed to be the
resource sources.

    >>> gf = guildfile.for_string("""
    ... - model: ''
    ...   resources:
    ...     res:
    ...       - file: foo.txt
    ...       - operation: bar
    ... """)

    >>> gf.default_model.get_resource("res").sources
    [<guild.resourcedef.ResourceSource 'file:foo.txt'>,
     <guild.resourcedef.ResourceSource 'operation:bar'>]

### Invalid data

    >>> guildfile.for_string("""
    ... - model: ''
    ...   resources:
    ...     res: 123
    ... """)
    Traceback (most recent call last):
    GuildfileError: error in <string>: invalid resource value 123:
    expected a mapping or a list
