FROM python:3.5

RUN apt update && apt install -y xvfb libglu1-mesa

# create fake display
RUN echo 'Xvfb :1 -screen 0 800x600x24 +extension GLX &' >> /entrypoint.sh
RUN echo 'exec "$@"' >> /entrypoint.sh
ENV DISPLAY :1

WORKDIR /app
ADD . /app
RUN pip install -e .

CMD ["bash"]
ENTRYPOINT ["bash", "/entrypoint.sh"]
