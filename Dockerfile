FROM amazon/aws-lambda-python:3.12

WORKDIR /var/task

RUN curl -L -o clamav-1.5.1.linux.x86_64.rpm https://github.com/Cisco-Talos/clamav/releases/download/clamav-1.5.1/clamav-1.5.1.linux.x86_64.rpm \
 && rpm -ivh clamav-1.5.1.linux.x86_64.rpm \
 && rm -f clamav-1.5.1.linux.x86_64.rpm

RUN echo "DatabaseMirror database.clamav.net" > /usr/local/etc/freshclam.conf \
 && echo "CompressLocalDatabase yes" >> /usr/local/etc/freshclam.conf \
 && echo "DatabaseOwner root" >> /usr/local/etc/freshclam.conf \
 && echo "DatabaseDirectory /tmp/clamav_defs" >> /usr/local/etc/freshclam.conf

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
 && rm -f requirements.txt

COPY ./*.py ./
