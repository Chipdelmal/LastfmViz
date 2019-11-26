
def padList(l, n):
    l.extend([None] * n)
    l = l[:n]
    return l


def getTopGenres(info, top=3):
    tags = info.get('tag-list')
    # Check that genres are available
    if tags is not None:
        lst=[]
        for i in info.get('tag-list'):
            lst.append((int(i.get('count')), i.get('name')))
        lst.sort(reverse=True)
        # Check that there are enough tags and pad with None
        if (len(lst) >= top):
            return [i[1] for i in lst[0:top]]
        else:
            tmp = [i[1] for i in lst[0:len(lst)]]
            return padList(tmp, top)
    else:
        return [None] * top


def getArea(info):
    area = info.get('begin-area')
    if area is not None:
        city = area.get('name')
        if city is not None:
            return city
    else:
        return None
