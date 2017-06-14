FROM nvidia/cuda:8.0-cudnn5-runtime

RUN apt update && apt install -y python3-pip xvfb libglu1-mesa

# avoid pyglet + NVIDIA OpenGL error
RUN echo 'cp -r /usr/local/nvidia /usr/local/_nvidia' >> /entrypoint.sh
RUN echo 'rm /usr/local/_nvidia/{lib,lib64}/*GL*' >> /entrypoint.sh
ENV LD_LIBRARY_PATH /usr/local/_nvidia/lib:/usr/local/_nvidia/lib64

# create fake display
RUN echo 'Xvfb :1 -screen 0 800x600x24 +extension GLX &' >> /entrypoint.sh
ENV DISPLAY :1

WORKDIR /app
ADD . /app
RUN pip3 install -e .

RUN echo 'exec "$@"' >> /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]

CMD ["bash"]
