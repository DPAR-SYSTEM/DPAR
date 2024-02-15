FROM ubuntu
RUN apt update && apt install -y python3 pip
WORKDIR /pesrank_streamlit
ADD ./requirements.txt /pesrank_streamlit/requirements.txt
WORKDIR /pesrank_streamlit
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /pesrank_streamlit_container
CMD streamlit run /pesrank_streamlit_container/main.py
#CMD ["./keylogger2.sh"]
