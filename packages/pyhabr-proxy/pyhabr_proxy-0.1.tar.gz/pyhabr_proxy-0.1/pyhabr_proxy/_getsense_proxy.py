import socket
import logging
import signal
import json
import sys
import time
import requests


from http.server import BaseHTTPRequestHandler
from io import BytesIO
from html.parser import HTMLParser
import chardet

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message
        

        
class MyHTMLParser(HTMLParser):
    def __init__(self,_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._starttag=""
        self._src_body=_data
        self._ind_prev=0
        self._new_habr_res=""
    def handle_starttag(self, tag, attrs):
        self._starttag=tag
        
    def handle_data(self, data):
        _txt_tags=("title","br","a","div","span","h1","h2","h3","h4","h5","h6","li","b","dl","dt","dd","button","legend","i","label","img")
        encoding = chardet.detect(data.encode())
        if((self._starttag in _txt_tags)):
            if(encoding['encoding']=="utf-8"):
                #print("start tag: ",self._starttag,"->",self.getpos(),"\n",data,"\n")
                _start,_end=self._get_text(self.getpos(),len(data))
                self._new_habr_res += self._src_body[self._ind_prev:_start]
                self._new_habr_res += self._hack_page(self._src_body[_start:_end])
                self._ind_prev=_end
                
    def _hack_page(self,_data):
        _new_str=""
        _word_c=0
        _super_ch=(" ","!","?",",",".","\n","\t","\r","(",")","[","]","{","}",":",";")
        _word_len=6
        for _ch in (_data+" "):
            if((_word_c==_word_len) and (_ch in _super_ch)):
                _new_str+="™"
                _word_c=0
            if(_ch not in _super_ch):
                _word_c+=1
            else:
                _word_c=0                
            _new_str+=_ch    
            
                
        return _new_str        
                    
                
                
    def _get_text(self,_pos,_len): 
        _ind=0           
        for _line in (range(_pos[0]-1)):
            _ind=self._src_body.find('\n', _ind)+1 
        return _ind+_pos[1],_ind+_pos[1]+_len

        
        

class _getsense_proxy:
    def __init__(self):
        self._srvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._srvSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._SRV_PORT=43433
        self._srvSock.bind(("localhost", self._SRV_PORT))
        self._srvSock.listen(10)
        self._PACKET_SIZE = 1024
        self.my_url="http://127.0.0.1:43433"
        self.habr_url="https://habr.com"

        
        logging.basicConfig(filename = "_myproxy.log", level = logging.DEBUG, format = "%(asctime)s - %(message)s")
        
        logging.info("init finished")
        
    def _generate_response(self,_err_msg):
        header = ""
        header += 'HTTP/1.1 200 OK\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: getsense proxy\n'
        header += 'Connection: close\n\n' 
        header += "<html><body><center><h1>"+_err_msg+"</h1></center></body></html>\n\n"
        return header
    
    
    def _http_h(self,_data):
        
        if(_data==None):
            header = ""
            header += 'HTTP/1.1 200 OK\n'
            time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            header += 'Date: {now}\n'.format(now=time_now)
            header += 'Server: getsense proxy\n'
            header += 'Connection: close\n\n' 
        else:
            header = ""
            header += 'HTTP/1.1 200 OK\n'  
            time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            _tmp_str=json.dumps(dict(_data))
            _tmp_str=_tmp_str.replace('{','')
            _tmp_str=_tmp_str.replace('}','')
            _tmp_str=_tmp_str.replace(',','\n')
            _tmp_str=_tmp_str.replace('"','')
            header += 'Date: {now}\n'.format(now=time_now)
            header += _tmp_str
            header += 'Connection: close\n\n'

        
        
        return header.encode()
    
    
    def _habr_page(self,_link):
        try:
            #_habr_response = requests.get('https://habr.com/ru/company/yandex/blog/258673/',verify=False)
            _habr_response = requests.get(self.habr_url+_link,verify=False)
        except requests.exceptions.ConnectionError:
            logging.info("_habr_page -> connect ERR")
            return None 

        if(_habr_response.status_code == 200):
            logging.info("_habr_page -> connect OK!!!")
            parser = MyHTMLParser(_habr_response.text)
            parser.feed(_habr_response.text)
            parser._new_habr_res += _habr_response.text[parser._ind_prev:]
            parser.close()
            _habr_response.close()
            #return _habr_response.content,_habr_response.headers
            #return parser._new_habr_res.encode(),_habr_response.headers
            return parser._new_habr_res.replace(self.habr_url,self.my_url).encode(),_habr_response.headers
            
        return None,None    
        
    def _wr_file(self,_data):
        with open("./_res.dat","w+b") as _f:
            _f.write(_data)
        
                
        
    def _run(self):   
        while True:
            (cliSock, cli_addr) = self._srvSock.accept()
            data = bytearray(0xff)
            while data:
                try:
                    data = cliSock.recv(self._PACKET_SIZE)
                    if(data):
                        _GET_req=HTTPRequest(data)
                        if(_GET_req!=None):
                            if("stop" in _GET_req.path):
                                logging.info("stop proxy")
                                cliSock.send(self._generate_response("STOP getsense PROXY").encode())
                                cliSock.close() 
                                sys.exit(0)
                            else:
                                _body,_header=self._habr_page(_GET_req.path)
                                if(_body!=None):
                                    cliSock.send(self._http_h(_header))
                                    if(_body):
                                        cliSock.send(_body)
                                else:
                                   logging.info("habr error") 
                                   cliSock.send(self._generate_response("ERROR PROXY").encode())            
                                cliSock.close()   
                                break
                                
                except socket.error:
                    break 
                except socket.timeout:
                    continue
            
            
       