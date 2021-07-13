# FROM python
# ENV PATH /usr/src/app/bin:$PATH
# ENV PATH /usr/src/app/driver:$PATH

# WORKDIR /usr/src/app


# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# # Install Chrome.
# RUN apt-get update && apt-get -y install google-chrome-stable
# COPY chromedriver driver/
# COPY bin/* ./
# COPY python-manager.sh /

#ENTRYPOINT [ "/python-manager.sh" ]

FROM python:3
ENV PATH /usr/source/app:$PATH
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable && \
    apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

COPY bin/* ./
COPY python-manager.sh .
ENTRYPOINT [ "./python-manager.sh" ]