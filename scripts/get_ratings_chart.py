from RoadMapView.models import RoadData_snapped

def run():
    rds =  RoadData_snapped.objects.all()
    arr = []
    for r in rds:
        # print()
        # arr.append(r.rating)
        print(r.rating)

    # f=open('f1.txt','w')
    # s1='\n'.join(arr)
    # f.write(s1)
    # f.close()