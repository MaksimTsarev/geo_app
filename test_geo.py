import pygame, sys, os, requests, math
from geopy.distance import great_circle as gd

class MapParams(object):
    
    def __init__(self):
        self.lat = 55.755833
        self.lon = 37.617623
        self.lon_a = self.lon
        self.lat_a = self.lat
        self.lon_sch = 37.596570
        self.lat_sch = 55.502467
        self.zoom = 15
        self.type = "map"
        self.size_h =650
        self.size_w = 450
        self.api_key = "d743673c-16a2-405b-9676-ac3265ae4318"
        self.text = ""
        
    def ll(self):
        return str(self.lon)+","+str(self.lat)

    def pt(self):
        return str(self.lon_a)+","+str(self.lat_a)+",pm2am~"+str(self.lon_sch)+","+str(self.lat_sch)+",pm2bm"

    def pl(self):
        return str(self.lon_a)+","+str(self.lat_a)+","+str(self.lon_sch)+","+str(self.lat_sch)

    def hw(self):
        return str(self.size_h)+","+str(self.size_w)

    def update(self, event):
        #print(event.key)
        if ((event.key == 1073741911 or event.key == 61) and self.zoom<19):
            self.zoom+=1
        if ((event.key == 1073741910 or event.key == 45) and self.zoom>1):
            self.zoom-=1
        if event.key == 1073741906:
            self.lat+=0.001 * (2**(15-self.zoom))
        if event.key == 1073741905:
            self.lat-=0.001 * (2**(15-self.zoom))
        if event.key == 1073741903:
            self.lon+=0.001 * (2**(15-self.zoom))
        if event.key == 1073741904:
            self.lon-=0.001 * (2**(15-self.zoom))

def load_map(mp):#&pt={pt}&pl={pl}
    
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}&size={size}&pt={pt}&pl={pl}".format(ll=mp.ll(), z=mp.zoom, type=mp.type, size=mp.hw(), pt=mp.pt(), pl=mp.pl())

    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    # Запись полученного изображения в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file

def load_geo(mp):#&pt={pt}&pl={pl}0
   
    geo_request = "https://geocode-maps.yandex.ru/1.x/?format=json&apikey={api}&geocode={geo}".format(api=mp.api_key, geo=mp.text)

    response = requests.get(geo_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(geo_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    # Запись полученного изображения в файл.
    geo_file = "geo.txt"
    try:
        with open(geo_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return geo_file

def main():
    pygame.init()
    screen = pygame.display.set_mode((650,450))
    mp = MapParams()
    while True:
        event = pygame.event.wait()
        if (event.type == pygame.QUIT):
            break
        #print("distance",gd((mp.lat_a,mp.lon_a),(mp.lat_sch,mp.lon_sch)),"km")
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file),(0,0))
        pygame.display.flip()
        if (event.type == pygame.KEYDOWN):
            mp.update(event)
            if (event.key == 13):
                mp.text=input()
                geo_file=load_geo(mp)
    pygame.quit()
    os.remove(map_file)
    os.remove(geo_file)

if __name__ == "__main__":
    main()
