def print1():
	print('substitution \n')
	print('''def encr(s, key):
    result = ""
    for c in s:
    	if(c.isupper()):
    		result += chr((ord(c) + key-65) % 26 + 65)
    	else:
    		result += chr((ord(c) + key-97) % 26 + 97)
    return result

if __name__ == "__main__":
        Ka = int(input("Value of offset: "))
        s = input("Enter string to encrypt: ")
        print(encr(s, Ka))
''')
def print2():
	print('transposition \n')
	print('''import numpy as np
from itertools import repeat
# Encryption
pt = input ("Enter Plain-Text: ")
_split = list(pt)
den = (len(_split) % 5)
d2 = 5 - den
if (den != 0):
	_split.extend(repeat(0, (d2)))
_2d = np.array(_split).reshape(-1,5)
print(_2d)
_2d_convt = (list(zip(*_2d)))
_convt = [y for x in _2d_convt for y in x]
CypherT = ''.join(_convt)
print("---------------------------")
print("Encrypted: " + CypherT)
print("---------------------------")

# Decryption
_cyt_split = list(CypherT)
_2d_cyp= np.array(_cyt_split).reshape(5,-1)
print(_2d_cyp)
_2d_convt_cyp = (list(zip(*_2d_cyp)))
_convt_cyp = [y for x in _2d_convt_cyp for y in x]
Plain = ''.join(_convt_cyp)
print("---------------------------")
print("Decrypted: " + Plain[:-d2])
print("---------------------------")
''')
def print3():
	print('RSA \n')
	print('''p = int(input("Enter the value of p (prime number)")) #5
q = int(input("Enter the value of q (prime number)")) #7

n = p * q
print("Value of n is: ",n)

totient = (p-1)*(q-1)
print("Value of totient is: ",totient)

for i in range(2,totient):
		if(totient%i!=0):
			e=i
			break

print("Value of e is: ",e)
		
d = (e**-1)% totient
 
plain_text = int(input("Enter plain text: ")) #2
cypher_text = (plain_text ** e) % n
print("Cipher text is: ",cypher_text)
 
plain_text2 = (cypher_text ** d) % n
print("Calculated plain text is: ",int(plain_text2))
''')
	
def print4():
	print('deffie  \n')
	print('''def exprcal(a, b, p):
	return ((a**b)%p)

def encr(s, key):
    result = ""
    for c in s:
        if(c.isupper()):
            result += chr((ord(c) + key-65) % 26 + 65)
        else:
            result += chr((ord(c) + key-97) % 26 + 97)
    return result

if __name__ == "__main__":
    P = int(input("Value of Public key for Alice: ")) #23
    G = int(input("Value of Public key for Bob: ")) #9
    a = int(input("Private key of Alice: ")) #4
    x = exprcal(G, a, P) #9^4 mod 23
    b = int(input("Private key of Bob: "))#3
    y = exprcal(G, b, P) #9^3 mod 23
    Ka = exprcal(y, a, P)
    Kb = exprcal(x, b, P)
    print("Secret key for Alice = ", Ka)
    print("Secret key for Bob = ", Kb)
    
    s = input("Enter string to encrypt: ") #abcd
    print(encr(s, Ka))
''')

def print5():
	print('shamd5 \n')
	print('''import hashlib
import time


def sha1(s):
	return (hashlib.sha1(s.encode()))

def md5(s):
	return (hashlib.md5(s.encode()))


if __name__ == "__main__":
	PT = input("Enter Text: ")
	#Time start
	t1 = time.time()	
	res1 = md5(PT).digest()
	print('Md5: ', res1)
	#Time end
	tf1 = time.time() - t1
	print('Time taken: ', tf1)
	#Time start
	t2 = time.time()
	res2 = sha1(PT).digest()
	print('SHA1: ', res2)
	#Time end
	tf2 = time.time() - t2
	print('Time taken: ', tf2)
	
''')
def print6():
	print('whois/nmap \n')
	print('''whois> https://www.whois.com/whois/kccemsr.edu.in	whois fb.com
dig> http://www.geektools.com/cgi-bin/do-dig.cgi	dig duckduckgo.com
traceroute> https://ping.eu/traceroute/			traceroute example.com
nslookup> http://www.kloth.net/services/nslookup.php	nslookup microsoft.com
nmap> 	1. multiple ports: nmap <pc ip addr>
	2. detect any running host: nmap -sP 192.168.2.1/24
	3. tcp port: nmap -sT <pc ip addr>
	4. udp port: nmap -sU <pc ip addr>''')
def print7():
	print('arpwatch \n')
	print('''sudo apt install arpwatch hping3 wireshark
arpwatch -i eth0
wireshark
sudo hping3 --flood <our ip>''')
def print8():
	print('ipsec \n')
	print('''---on pc 1---
sudo apt-get install ipsec-tools strongswan-starter
sudo gedit /etc/ipsec.conf

conn red-to-blue
	authby=secret
	auto=route
	keyexchange=ike
	left=192.168.18.131 #red ip i.e. our
	right=192.168.18.134 #blue ip i.e. remote
	type=transport
	esp=aes128gcm161

sudo gedit /etc/ipsec.secrets 
red blue : PSK "PASSWORD"
sudo ipsec restart
sudo ipsec statusall

---on pc 2---
sudo apt-get install ipsec-tools strongswan-starter
sudo gedit /etc/ipsec.conf

conn blue-to-red
	authby=secret
	auto=route
	keyexchange=ike
	left=192.168.18.134 #red ip i.e. our
	right=192.168.18.131 #blue ip i.e. remote
	type=transport
	esp=aes128gcm161

sudo gedit /etc/ipsec.secrets 
red blue : PSK "PASSWORD"
sudo ipsec restart

---on pc 1---
ping 192.168.18.134 (remote ip)
---on pc 2---
sudo tcpdump -i eth0 icmp''')
def print9():
	print('iptables \n')
	print('''sudo apt-get install iptables
sudo iptables -L
sudo iptables -A INPUT -s 192.168.18.134(remoteip) -j DROP
--pc2--
ping pc1
--pc1--
sudo iptables -F
sudo iptables -A INPUT -s 192.168.18.134(remoteip) -j ACCEPT
--pc2--
ping pc1''')
def print10():
	print('snort \n')
	print('''sudo apt-get install snort
setup
cd /etc/snort/
gedit snort.debian.conf -> home_net=<own ip>
gedit snort.conf -> include $RULE_PATH/test.rules
cd /etc/snort/rules/
sudo gedit test.rules -> alert tcp any any -> any any (content:"www.google.com";msg:"intruder detected";sid:212333;)
cd ../../../../
sudo snort -c /etc/snort/snort.conf -T
sudo snort -q -A console -i eth0 -c /etc/snort/snort.conf
''')
