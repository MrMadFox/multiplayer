import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("172.17.28.123",5005))
playinglist=[0]*5
class sai:
    def __init__(self):
        self.p1_position_y = 50  # percentage
        self.p2_position_y = 30
        self.p1_ready=0
        self.p2_ready=0
        self.p1_addr=0
        self.p2_addr=0
        self.p1_fire=0
        self.p2_fire=0
        self.p1_health=100
        self.p2_health=100
while(1):
    data, addr = s.recvfrom(1024)
    playingid, position, fire, health = list(map(int, data.decode().split()))
    if playingid==-1:
        zz=0
        for createplayingid in range(1,len(playinglist)):
            if playinglist[createplayingid]!=0:
                if playinglist[createplayingid].p2_addr==0:
                    playinglist[createplayingid].p2_addr=addr
                    zz=createplayingid
                    break
        if zz==0:
            for createplayingid in range(1, len(playinglist)):
                if playinglist[createplayingid] == 0:
                    playinglist[createplayingid]=sai()
                    playinglist[createplayingid].p1_addr = addr
                    zz = createplayingid
                    break
        s.sendto((str(zz)).encode("utf-8"), addr)
        continue

    if playinglist[playingid].p1_ready==0 or playinglist[playingid].p2_ready==0:
        ready=position
        # if playinglist[playingid]==0:
        #     playinglist[playingid]=sai()
        # if playinglist[playingid].p1_addr==0:
        #     playinglist[playingid].p1_addr=addr
        # else:
        #     playinglist[playingid].p2_addr=addr

        userid="1" if addr==playinglist[playingid].p1_addr else "2"
        if userid=="1":
            playinglist[playingid].p1_ready=ready
        elif userid=="2":
            playinglist[playingid].p2_ready=ready
        if playinglist[playingid].p1_ready+playinglist[playingid].p2_ready==2:
            s.sendto(b"1", playinglist[playingid].p2_addr)
            s.sendto(b"1", playinglist[playingid].p1_addr)
    else:
        #if not playinglist[playingid].p1_addr==addr or playinglist[playingid].p2_addr==addr:
        #    continue
        positionz=-1
        userid = "1" if addr == playinglist[playingid].p1_addr else "2"
        if userid=="1":
            playinglist[playingid].p1_health=health
            playinglist[playingid].p1_fire=fire
            playinglist[playingid].p1_position_y=position
            positionz=playinglist[playingid].p2_position_y
            firez=playinglist[playingid].p2_fire
            healthz=playinglist[playingid].p2_health
        if userid=="2":
            playinglist[playingid].p2_health=health
            playinglist[playingid].p2_fire=fire
            playinglist[playingid].p2_position_y=position
            positionz=playinglist[playingid].p1_position_y
            firez=playinglist[playingid].p1_fire
            healthz=playinglist[playingid].p1_health
        if positionz!=-1:
            s.sendto((str(positionz)+" "+str(firez)+" "+str(healthz)).encode("utf-8"), addr)
            if healthz<=0:
                playinglist[playingid]=0