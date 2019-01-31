import socket
p1_position_y=50#percentage
p2_position_y=30
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1",5005))
p1_ready=0
p2_ready=0
p1_addr=0
p2_addr=0
while(1):
    data, addr = s.recvfrom(1024)
    playingid,userid,ready=data.decode().split()
    if userid=="1":
        p1_ready=ready
        p1_addr=addr
    elif userid=="2":
        p2_ready=ready
        p1_addr = addr
    if p1_ready+p2_ready==2:
        s.sendto(b"1", p2_addr)
        s.sendto(b"1", p1_addr)
        break



while(1):
    data,addr=s.recvfrom(1024)
    z=-1
    playingid,userid,position=data.decode().split()
    position=int(position)
    if userid=="1":
        p1_position_y=position
        z=p2_position_y
    if userid=="2":
        p2_position_y=position
        z=p1_position_y
    if z!=-1:
        s.sendto(str(z).encode("utf-8"), addr)

    #conn.send(str(p1_position_y).encode("utf-8"))

