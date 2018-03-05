import requests

# use post call to give the image to server
# use get call to get the response back

r = requests.post(url="http://127.0.0.1:5000/upload",
                  files={'file': open("/home/ankush/Desktop/openFace/Api/hello.jpg", 'rb')})
r1 = requests.get(url="http://127.0.0.1:5000/recognize")

print r1.text
print(r1.status_code)
print(r.text)