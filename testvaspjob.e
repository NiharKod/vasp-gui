
The following have been reloaded with a version change:
  1) openmpi/4.0.6 => openmpi/4.1.6

HDF5-DIAG: Error detected in HDF5 (1.10.7) MPI-process 0:
  #000: /tmp/rcactest/spack-stage-hdf5-1.10.7-ssjeoyymz75nnlaccdvgzh7kf3q5iwl7/spack-src/src/H5F.c line 366 in H5Fcreate(): unable to create file
    major: File accessibility
    minor: Unable to open file
  #001: /tmp/rcactest/spack-stage-hdf5-1.10.7-ssjeoyymz75nnlaccdvgzh7kf3q5iwl7/spack-src/src/H5Fint.c line 1713 in H5F_open(): unable to lock the file
    major: File accessibility
    minor: Unable to lock file
  #002: /tmp/rcactest/spack-stage-hdf5-1.10.7-ssjeoyymz75nnlaccdvgzh7kf3q5iwl7/spack-src/src/H5FD.c line 1675 in H5FD_lock(): driver lock request failed
    major: Virtual File Layer
    minor: Unable to lock file
  #003: /tmp/rcactest/spack-stage-hdf5-1.10.7-ssjeoyymz75nnlaccdvgzh7kf3q5iwl7/spack-src/src/H5FDsec2.c line 990 in H5FD__sec2_lock(): unable to lock file, errno = 11, error message = 'Resource temporarily unavailable'
    major: Virtual File Layer
    minor: Unable to lock file
 -----------------------------------------------------------------------------
|                     _     ____    _    _    _____     _                     |
|                    | |   |  _ \  | |  | |  / ____|   | |                    |
|                    | |   | |_) | | |  | | | |  __    | |                    |
|                    |_|   |  _ <  | |  | | | | |_ |   |_|                    |
|                     _    | |_) | | |__| | | |__| |    _                     |
|                    (_)   |____/   \____/   \_____|   (_)                    |
|                                                                             |
|     internal error in: vhdf5.F  at line: 78                                 |
|                                                                             |
|     HDF5 call in vhdf5.F:78 produced error: -1                              |
|                                                                             |
|     If you are not a developer, you should not encounter this problem.      |
|     Please submit a bug report.                                             |
|                                                                             |
 -----------------------------------------------------------------------------

--------------------------------------------------------------------------
MPI_ABORT was invoked on rank 0 in communicator MPI_COMM_WORLD
with errorcode 1.

NOTE: invoking MPI_ABORT causes Open MPI to kill all MPI processes.
You may or may not see output from other processes, depending on
exactly when Open MPI kills them.
--------------------------------------------------------------------------
