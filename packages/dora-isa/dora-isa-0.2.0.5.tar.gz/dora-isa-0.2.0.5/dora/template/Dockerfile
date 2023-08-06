ARG IMAGE_BASE

FROM $IMAGE_BASE

LABEL maintainer="Compasso"
LABEL app="DORA"
LABEL version="0.2.0"
ARG DORA_MEM="4g"
ENV DORA_MEM ${DORA_MEM}

ARG DORA_BUCKET
ENV DORA_BUCKET ${DORA_BUCKET}

ARG DORA_USER
ENV DORA_USER ${DORA_USER}

ENV DORA_MLD /etc/ml
ENV DORA_LOG ${DORA_MLD}/score/logs

ENV PYSPARK_PYTHON /usr/local/bin/python3.7
ENV PYSPARK_DRIVER_PYTHON ipython3

COPY ./cp ${DORA_MLD}
RUN mkdir -p ${DORA_LOG}

RUN echo "Setting CHMOD" && \
    chmod u+x /bin/*.sh && \
    chmod u+x ${DORA_MLD}/score/*.sh

RUN pip install -r ${DORA_MLD}/requirements.txt

RUN ln -s ${DORA_MLD}/score/run.sh ${DORA_MLD}/score/run

ENV PATH $PATH:${DORA_MLD}/score/run

WORKDIR ${DORA_MLD}/score
# ENTRYPOINT ["/etc/ml/score/run.sh","$@"]