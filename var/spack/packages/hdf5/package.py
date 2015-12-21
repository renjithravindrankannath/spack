from spack import *

class Hdf5(Package):
    """HDF5 is a data model, library, and file format for storing and managing
       data. It supports an unlimited variety of datatypes, and is designed for
       flexible and efficient I/O and for high volume and complex data.
    """

    homepage = "http://www.hdfgroup.org/HDF5/"
    url      = "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.13/src/hdf5-1.8.13.tar.gz"
    list_url = "http://www.hdfgroup.org/ftp/HDF5/releases"
    list_depth = 3
    
    version('1.8.16', 'b8ed9a36ae142317f88b0c7ef4b9c618')
    version('1.8.15', '03cccb5b33dbe975fdcd8ae9dc021f24')
    version('1.8.13', 'c03426e9e77d7766944654280b467289')

    variant('mpi', default=False, description='Enable MPI support')

    depends_on("mpi", when='+mpi')
    depends_on("zlib")

    # TODO: currently hard-coded to use OpenMPI
    def install(self, spec, prefix):
        extra_args = []
        if '+mpi' in spec:
            extra_args.extend([
                "--enable-parallel",
                "CC=%s" % spec['mpi'].prefix.bin + "/mpicc",
                "CXX=%s" % spec['mpi'].prefix.bin + "/mpic++",
            ])

        configure(
            "--prefix=%s" % prefix,
            "--with-zlib=%s" % spec['zlib'].prefix,
            "--enable-shared",
            *extra_args)

        make()
        make("install")

    def url_for_version(self, version):
        v = str(version)

        if version == Version("1.2.2"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + v + ".tar.gz"
        elif version < Version("1.7"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + version.up_to(2) + "/hdf5-" + v + ".tar.gz"
        else:
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + v + "/src/hdf5-" + v + ".tar.gz"
