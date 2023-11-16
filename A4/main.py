from http.server import HTTPServer
from server import MyHandler 
import sys



def main():
    #create the website
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    httpd.serve_forever()
    
if __name__ == "__main__":
    main()