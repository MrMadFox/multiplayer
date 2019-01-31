import socket
p1_position_y=50#percentage
p2_position_y=30
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1",5005))
p1_ready=0
p2_ready=0
p1_addr=0
p2_addr=0
p1_fire=0
p2_fire=0
p1_health=100
p2_health=100
while(1):
    data, addr = s.recvfrom(1024)
    if p1_addr==0:
        p1_addr=addr
    else:
        p2_addr=addr
    print(1)
    playingid,ready=data.decode().split()
    userid="1" if addr==p1_addr else "2"
    ready=int(ready)
    if userid=="1":
        p1_ready=ready
    elif userid=="2":
        p2_ready=ready
    if p1_ready+p2_ready==2:
        s.sendto(b"1", p2_addr)
        s.sendto(b"1", p1_addr)
        break
while(1):
    data,addr=s.recvfrom(1024)
    z=-1
    playingid,position,fire,health=list(map(int,data.decode().split()))
    userid = "1" if addr == p1_addr else "2"
    if userid=="1":
        p1_health=health
        p1_fire=fire
        p1_position_y=position
        z=p2_position_y
        firez=p2_fire
        healthz=p2_health
    if userid=="2":
        p2_health=health
        p2_fire=fire
        p2_position_y=position
        z=p1_position_y
        firez=p1_fire
        healthz=p1_health
    if z!=-1:
        s.sendto((str(z)+" "+str(firez)+" "+str(healthz)).encode("utf-8"), addr)
    #conn.send(str(p1_position_y).encode("utf-8"))

