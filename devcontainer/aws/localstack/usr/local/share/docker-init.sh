#!/usr/bin/env bash

# Sourced from: https://github.com/devcontainers/features/blob/main/src/docker-in-docker/install.sh
#  - So we can avoid having to install the docker-in-docker devcontainer feature
#  - Removed irrelevant startup handling so supervisor can handle it

# explicitly remove dockerd and containerd PID file to ensure that it can start properly if it was stopped uncleanly
find /run /var/run -iname 'docker*.pid' -delete || :
find /run /var/run -iname 'container*.pid' -delete || :

# -- Start: dind wrapper script --
# Maintained: https://github.com/moby/moby/blob/master/hack/dind

export container=docker

if [ -d /sys/kernel/security ] && ! mountpoint -q /sys/kernel/security; then
    mount -t securityfs none /sys/kernel/security || {
        echo >&2 'Could not mount /sys/kernel/security.'
        echo >&2 'AppArmor detection and --privileged mode might break.'
    }
fi

# Mount /tmp (conditionally)
if ! mountpoint -q /tmp; then
    mount -t tmpfs none /tmp
fi

set_cgroup_nesting()
{
    # cgroup v2: enable nesting
    if [ -f /sys/fs/cgroup/cgroup.controllers ]; then
        # move the processes from the root group to the /init group,
        # otherwise writing subtree_control fails with EBUSY.
        # An error during moving non-existent process (i.e., "cat") is ignored.
        mkdir -p /sys/fs/cgroup/init
        xargs -rn1 < /sys/fs/cgroup/cgroup.procs > /sys/fs/cgroup/init/cgroup.procs || :
        # enable controllers
        sed -e 's/ / +/g' -e 's/^/+/' < /sys/fs/cgroup/cgroup.controllers \
            > /sys/fs/cgroup/cgroup.subtree_control
    fi
}

# Set cgroup nesting, retrying if necessary
retry_cgroup_nesting=0

until [ "${retry_cgroup_nesting}" -eq "5" ];
do
    set +e
        set_cgroup_nesting

        if [ $? -ne 0 ]; then
            echo "(*) cgroup v2: Failed to enable nesting, retrying..."
        else
            break
        fi

        retry_cgroup_nesting=`expr $retry_cgroup_nesting + 1`
    set -e
done

# -- End: dind wrapper script --

# Handle DNS
set +e
    cat /etc/resolv.conf | grep -i 'internal.cloudapp.net' > /dev/null 2>&1
    if [ $? -eq 0 ] && [ "${AZURE_DNS_AUTO_DETECTION}" = "true" ]
    then
        echo "Setting dockerd Azure DNS."
        CUSTOMDNS="--dns 168.63.129.16"
    else
        echo "Not setting dockerd DNS manually."
        CUSTOMDNS=""
    fi
set -e

if [ -z "$DOCKER_DEFAULT_ADDRESS_POOL" ]
then
    DEFAULT_ADDRESS_POOL=""
else
    DEFAULT_ADDRESS_POOL="--default-address-pool $DOCKER_DEFAULT_ADDRESS_POOL"
fi

# Start docker/moby engine
exec dockerd $CUSTOMDNS $DEFAULT_ADDRESS_POOL --tls=false -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375 2>&1
