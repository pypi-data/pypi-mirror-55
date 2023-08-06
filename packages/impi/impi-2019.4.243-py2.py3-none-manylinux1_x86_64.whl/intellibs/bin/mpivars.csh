#!/bin/tcsh
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

setenv I_MPI_ROOT I_MPI_SUBSTITUTE_INSTALLDIR

if !($?PATH) then
    setenv PATH ${I_MPI_ROOT}/intel64/bin
else
    setenv PATH ${I_MPI_ROOT}/intel64/bin:${PATH}
endif

if !($?CLASSPATH) then
    setenv CLASSPATH ${I_MPI_ROOT}/intel64/lib/mpi.jar
else
    set noglob
    setenv CLASSPATH ${I_MPI_ROOT}/intel64/lib/mpi.jar:${CLASSPATH}
    unset noglob
endif

if !($?LD_LIBRARY_PATH) then
    setenv LD_LIBRARY_PATH ${I_MPI_ROOT}/intel64/lib/release:${I_MPI_ROOT}/intel64/lib
else
    setenv LD_LIBRARY_PATH ${I_MPI_ROOT}/intel64/lib/release:${I_MPI_ROOT}/intel64/lib:${LD_LIBRARY_PATH}
endif

if !($?MANPATH) then
    setenv MANPATH ${I_MPI_ROOT}/man:`manpath`
else
    setenv MANPATH ${I_MPI_ROOT}/man:${MANPATH}
endif

set i_mpi_library_kind=""
set i_mpi_ofi_library_internal="1"

if ($?I_MPI_LIBRARY_KIND) then
    set i_mpi_library_kind=$I_MPI_LIBRARY_KIND
endif
if ($?I_MPI_OFI_LIBRARY_INTERNAL) then
    set i_mpi_ofi_library_internal=$I_MPI_OFI_LIBRARY_INTERNAL
endif

while ($#argv > 0)
    switch ($argv[1])
        case -ofi_internal:
        case --ofi_internal:
            set i_mpi_ofi_library_internal=1
            shift
            breaksw
        case "-ofi_internal=*":
        case "--ofi_internal=*":
            set i_mpi_ofi_library_internal=`echo "$argv[1]" | sed "s/.*=//"`
            shift
            breaksw
        case --help:
        case -h:
            echo ""
            echo "Usage: mpivars.csh [-ofi_internal[=0|1]] [i_mpi_library_kind]"
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
            echo "i_mpi_library_kind  to the script."
            echo "Use variable I_MPI_OFI_LIBRARY_INTERNAL to pass -ofi_internal setting."
            echo ""
            shift
            breaksw
        default:
            set i_mpi_library_kind=$argv[1]
            shift
            breaksw
    endsw
end

switch ($i_mpi_library_kind)
    case debug:
    case debug_mt:
    case release:
    case release_mt:
        setenv LD_LIBRARY_PATH ${I_MPI_ROOT}/intel64/lib/${i_mpi_library_kind}:${I_MPI_ROOT}/intel64/lib:${LD_LIBRARY_PATH}
        breaksw
endsw

switch ($i_mpi_ofi_library_internal)
    case 0:
    case no:
    case off:
    case disable:
        breaksw
    default:
        setenv PATH ${I_MPI_ROOT}/intel64/libfabric/bin:${PATH}
        setenv LD_LIBRARY_PATH ${I_MPI_ROOT}/intel64/libfabric/lib:${LD_LIBRARY_PATH}
        if !($?LIBRARY_PATH) then
            setenv LIBRARY_PATH ${I_MPI_ROOT}/intel64/libfabric/lib
        else
            setenv LIBRARY_PATH ${I_MPI_ROOT}/intel64/libfabric/lib:${LIBRARY_PATH}
        endif
        setenv FI_PROVIDER_PATH ${I_MPI_ROOT}/intel64/libfabric/lib/prov
        breaksw
endsw
