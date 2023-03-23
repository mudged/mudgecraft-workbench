FROM ubuntu

ARG PYTHON_VERSION="3.11.1"
ARG OPENVSCODE_SERVER_ROOT="/home/.openvscode-server"
ARG OPENVSCODE_SERVER_RELEASE_TAG="openvscode-server-v1.76.2"
ARG HOST_USER_UID="1000"
ARG HOST_USER_NAME="steve"
ARG HOST_USER_GID="1000"
ARG HOST_USER_GROUP_NAME="mudgecraft"
ARG WORKSPACE_DATA_DIR="/data/workspace"
ARG MINECRAFT_SERVER_DATA_DIR="/data/minecraft-server"
ARG TARGETPLATFORM="linux/amd64"

# Update packages and add utilities
RUN apt update && \
  apt install --no-install-recommends curl -y && \
  apt install --no-install-recommends wget -y && \
  apt install --no-install-recommends jq -y && \
  apt install --no-install-recommends git -y && \
  apt install --no-install-recommends sudo -y && \
  apt install --no-install-recommends libatomic1 -y && \
  apt install --no-install-recommends apt-transport-https -y && \
  apt install --no-install-recommends gnupg-agent -y && \
  apt install --no-install-recommends software-properties-common -y && \
  apt install --no-install-recommends ca-certificates -y && \
  apt install --no-install-recommends unzip -y && \
  apt install --no-install-recommends openssh-client -y && \
  apt install --no-install-recommends python3 -y && \
  apt install --no-install-recommends python3-venv -y && \
  apt install --no-install-recommends python3-pip -y && \
  rm -rf /var/lib/apt/lists/*

# Install Docker
RUN curl -sSL https://get.docker.com/ | sh

# VSCode Server
RUN if [ -z "${OPENVSCODE_SERVER_RELEASE_TAG}" ]; then \
        echo "The OPENVSCODE_SERVER_RELEASE_TAG build arg must be set." >&2 && \
        exit 1; \
    fi && \
    arch=$(uname -m) && \
    if [ "${arch}" = "x86_64" ]; then \
        OPENVSCODE_SERVER_ARCH="x64"; \
    elif [ "${arch}" = "aarch64" ]; then \
        OPENVSCODE_SERVER_ARCH="arm64"; \
    elif [ "${arch}" = "armv7l" ]; then \
        OPENVSCODE_SERVER_ARCH="armhf"; \
    fi && \
    wget https://github.com/gitpod-io/openvscode-server/releases/download/${OPENVSCODE_SERVER_RELEASE_TAG}/${OPENVSCODE_SERVER_RELEASE_TAG}-linux-${OPENVSCODE_SERVER_ARCH}.tar.gz && \
    tar -xzf ${OPENVSCODE_SERVER_RELEASE_TAG}-linux-${OPENVSCODE_SERVER_ARCH}.tar.gz && \
    mv -f ${OPENVSCODE_SERVER_RELEASE_TAG}-linux-${OPENVSCODE_SERVER_ARCH} ${OPENVSCODE_SERVER_ROOT} && \
    cp ${OPENVSCODE_SERVER_ROOT}/bin/remote-cli/openvscode-server ${OPENVSCODE_SERVER_ROOT}/bin/remote-cli/code && \
    rm -f ${OPENVSCODE_SERVER_RELEASE_TAG}-linux-${OPENVSCODE_SERVER_ARCH}.tar.gz

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    EDITOR=code \
    VISUAL=code \
    GIT_EDITOR="code --wait" \
    OPENVSCODE_SERVER_ROOT=$OPENVSCODE_SERVER_ROOT

# Creating the user and usergroup
RUN groupadd -f --gid ${HOST_USER_GID} ${HOST_USER_GROUP_NAME} \
    && useradd --uid ${HOST_USER_UID} --gid ${HOST_USER_GROUP_NAME} -m -s /bin/bash ${HOST_USER_NAME} \
    && echo ${HOST_USER_NAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${HOST_USER_NAME} \
    && chmod 0440 /etc/sudoers.d/${HOST_USER_NAME}

# Add user to docker group
RUN usermod -a -G docker ${HOST_USER_NAME}

# Create the standard directory structure
RUN mkdir -p /home/${HOST_USER_NAME}/.openvscode-server/data/Machine /home/${HOST_USER_NAME}/.openvscode-server/extensions ${WORKSPACE_DATA_DIR} ${MINECRAFT_SERVER_DATA_DIR} /minecraft/plugins /minecraft/mods
RUN chown -R ${HOST_USER_NAME}:${HOST_USER_GROUP_NAME} /home/${HOST_USER_NAME} ${WORKSPACE_DATA_DIR} ${MINECRAFT_SERVER_DATA_DIR} ${OPENVSCODE_SERVER_ROOT} /minecraft/plugins /minecraft/mods

# Add the VS Code settings, scripts and README
COPY --chown=${HOST_USER_NAME}:${HOST_USER_GROUP_NAME} .bashrc /home/${HOST_USER_NAME}/.bashrc
COPY --chown=${HOST_USER_NAME}:${HOST_USER_GROUP_NAME} scripts/ /home/${HOST_USER_NAME}/
COPY --chown=${HOST_USER_NAME}:${HOST_USER_GROUP_NAME} vscode-machine-settings.json /home/${HOST_USER_NAME}/.openvscode-server/data/Machine/settings.json

# Make scripts executable
RUN chmod +x /home/${HOST_USER_NAME}/.bashrc /home/${HOST_USER_NAME}/*.sh

USER ${HOST_USER_NAME}
WORKDIR /home/${HOST_USER_NAME}

# Install Python Packages
RUN pip3 install mciwb mcpi

# Install VSCode Extensions
RUN cd /home/${HOST_USER_NAME}/.openvscode-server/extensions && wget https://open-vsx.org/api/ms-python/python/2023.4.0/file/ms-python.python-2023.4.0.vsix && \
    $OPENVSCODE_SERVER_ROOT/bin/openvscode-server --install-extension ms-python.python-2023.4.0.vsix

# Copy Minecraft Plugins and Mods
COPY --chown=${HOST_USER_NAME}:${HOST_USER_GROUP_NAME} plugins/ /minecraft/plugins
#COPY --chown=${HOST_USER_NAME}:${HOST_USER_GROUP_NAME} mods/ /minecraft/mods

# Create a persistant workspace directory in the users home directory
RUN cd /home/${HOST_USER_NAME} && ln -s ${WORKSPACE_DATA_DIR} workspace

EXPOSE 3400
VOLUME ${WORKSPACE_DATA_DIR}
VOLUME ${MINECRAFT_SERVER_DATA_DIR}

ENV WORKSPACE_DATA_DIR=${WORKSPACE_DATA_DIR} \
    MINECRAFT_SERVER_DATA_DIR=${MINECRAFT_SERVER_DATA_DIR}

ENTRYPOINT [ "/bin/sh", "-c", "exec ${OPENVSCODE_SERVER_ROOT}/bin/openvscode-server --host 0.0.0.0 --port 3400 --without-connection-token \"${@}\"", "--" ]
