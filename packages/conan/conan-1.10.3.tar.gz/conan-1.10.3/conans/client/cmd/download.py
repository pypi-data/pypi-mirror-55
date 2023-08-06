import os

from conans.client.output import ScopedOutput
from conans.client.source import complete_recipe_sources
from conans.errors import NotFoundException
from conans.model.ref import PackageReference, ConanFileReference


def download(reference, package_ids, remote_name, recipe, registry, remote_manager,
             client_cache, out, recorder, loader, hook_manager):

    assert(isinstance(reference, ConanFileReference))
    output = ScopedOutput(str(reference), out)
    remote = registry.remotes.get(remote_name) if remote_name else registry.remotes.default

    hook_manager.execute("pre_download", reference=reference, remote=remote)
    # First of all download package recipe
    try:
        remote_manager.get_recipe(reference, remote)
    except NotFoundException:
        raise NotFoundException("'%s' not found in remote '%s'" % (str(reference), remote.name))
    registry.refs.set(reference, remote.name)
    conan_file_path = client_cache.conanfile(reference)
    conanfile = loader.load_class(conan_file_path)

    if not recipe:
        # Download the sources too, don't be lazy
        complete_recipe_sources(remote_manager, client_cache, registry,
                                conanfile, reference)

        if package_ids:
            _download_binaries(reference, package_ids, client_cache, remote_manager,
                               remote, output, recorder, loader)
        else:
            output.info("Getting the complete package list "
                        "from '%s'..." % str(reference))
            packages_props = remote_manager.search_packages(remote, reference, None)
            if not packages_props:
                output = ScopedOutput(str(reference), out)
                output.warn("No remote binary packages found in remote")
            else:
                _download_binaries(reference, list(packages_props.keys()), client_cache,
                                   remote_manager, remote, output, recorder, loader)
    hook_manager.execute("post_download", conanfile_path=conan_file_path, reference=reference,
                         remote=remote)


def _download_binaries(reference, package_ids, client_cache, remote_manager, remote, output,
                       recorder, loader):
    conanfile_path = client_cache.conanfile(reference)
    if not os.path.exists(conanfile_path):
        raise Exception("Download recipe first")
    conanfile = loader.load_class(conanfile_path)
    short_paths = conanfile.short_paths

    for package_id in package_ids:
        package_ref = PackageReference(reference, package_id)
        package_folder = client_cache.package(package_ref, short_paths=short_paths)
        output.info("Downloading %s" % str(package_ref))
        remote_manager.get_package(package_ref, package_folder, remote, output, recorder)
