#!/bin/sh
#
# Copyright 2003-2019 Intel Corporation.
# 
# This software and the related documents are Intel copyrighted materials, and
# your use of them is governed by the express license under which they were
# provided to you (License). Unless the License provides otherwise, you may
# not use, modify, copy, publish, distribute, disclose or transmit this
# software or the related documents without Intel's prior written permission.
# 
# This software and the related documents are provided as is, with no express
# or implied warranties, other than those that are expressly stated in the
# License.
#

I_MPI_ROOT=I_MPI_SUBSTITUTE_INSTALLDIR; export I_MPI_ROOT

print_help()
{
    echo ""
    echo "Usage: mpivars.sh [-ofi_internal[=0|1]] [i_mpi_library_kind]"
    echo ""
    echo "i_mpi_library_kind can be one of the following:"
    echo "      debug           "
    echo "      debug_mt        "
    echo "      release         "
    echo "      release_mt      "
    echo ""
    echo "-ofi_internal specifies whether to use libfabric from the Intel(R) MPI Library."
    echo ""
    echo "If the arguments to the sourced script are ignored (consult docs"
    echo "for your shell) the alternative way to specify target is environment"
    echo "variable I_MPI_LIBRARY_KIND to pass"
    echo "i_mpi_library_kind to the script."
    echo "Use variable I_MPI_OFI_LIBRARY_INTERNAL to pass -ofi_internal setting."
    echo ""
}

if [ -z "${PATH}" ]
then
    PATH="${I_MPI_ROOT}/intel64/bin"; export PATH
else
    PATH="${I_MPI_ROOT}/intel64/bin:${PATH}"; export PATH
fi

if [ -z "${CLASSPATH}" ]
then
    CLASSPATH="${I_MPI_ROOT}/intel64/lib/mpi.jar"; export CLASSPATH
else
    CLASSPATH="${I_MPI_ROOT}/intel64/lib/mpi.jar:${CLASSPATH}"; export CLASSPATH
fi

if [ -z "${LD_LIBRARY_PATH}" ]
then
    LD_LIBRARY_PATH="${I_MPI_ROOT}/intel64/lib/release:${I_MPI_ROOT}/intel64/lib"; export LD_LIBRARY_PATH
else
    LD_LIBRARY_PATH="${I_MPI_ROOT}/intel64/lib/release:${I_MPI_ROOT}/intel64/lib:${LD_LIBRARY_PATH}"; export LD_LIBRARY_PATH
fi

if [ -z "${MANPATH}" ]
then
    MANPATH="${I_MPI_ROOT}/man":`manpath 2>/dev/null`; export MANPATH
else
    MANPATH="${I_MPI_ROOT}/man:${MANPATH}"; export MANPATH
fi

if [ -z "${I_MPI_OFI_LIBRARY_INTERNAL}" ]
then
    i_mpi_ofi_library_internal="1"
else
    i_mpi_ofi_library_internal="${I_MPI_OFI_LIBRARY_INTERNAL}"
fi

i_mpi_library_kind="${I_MPI_LIBRARY_KIND}"

while [ $# -gt 0 ]
do
    case "$1" in
        -ofi_internal|--ofi_internal)
            i_mpi_ofi_library_internal=1
            shift
            ;;
        -ofi_internal=*|--ofi_internal=*)
            i_mpi_ofi_library_internal="${1#*=}"
            shift
            ;;
        -h|--help)
            print_help
            shift
            ;;
        *)
            i_mpi_library_kind="$1"
            shift
            ;;
    esac
done

case "$i_mpi_library_kind" in
    debug|debug_mt|release|release_mt)
        LD_LIBRARY_PATH="${I_MPI_ROOT}/intel64/lib/${i_mpi_library_kind}:${I_MPI_ROOT}/intel64/lib:${LD_LIBRARY_PATH}"; export LD_LIBRARY_PATH
        ;;
esac

case "$i_mpi_ofi_library_internal" in
    0|no|off|disable)
        ;;
    *)
        PATH="${I_MPI_ROOT}/intel64/libfabric/bin:${PATH}"; export PATH
        LD_LIBRARY_PATH="${I_MPI_ROOT}/intel64/libfabric/lib:${LD_LIBRARY_PATH}"; export LD_LIBRARY_PATH
        if [ -z "${LIBRARY_PATH}" ]
        then
            LIBRARY_PATH="${I_MPI_ROOT}/intel64/libfabric/lib"; export LIBRARY_PATH
        else
            LIBRARY_PATH="${I_MPI_ROOT}/intel64/libfabric/lib:${LIBRARY_PATH}"; export LIBRARY_PATH
        fi
        FI_PROVIDER_PATH="${I_MPI_ROOT}/intel64/libfabric/lib/prov"; export FI_PROVIDER_PATH
        ;;
esac
