import os
from PIL import Image, ImageDraw, ExifTags, ImageColor
import io
import pandas as pd
import boto3
import time
import csv

path = '/Users/Download/project-AWS_FaceComparison/' 
path2 = path + 'students/'  
os.chdir(path)
namejpg = sorted(list(os.listdir(path2)))  
if ('.jpg' not in namejpg[0]): 
    del namejpg[0]  #第一項若為['.DS_Store']需刪除



def initial():
    print('資料建立中...')
    idno = []
    name  = []
    for i in namejpg:
        i = i.replace('.jpg', '')
        i1 = i[0:2]  #分割字串:前兩字元為座號
        i2 = i[2:]   #分割字串:第三字元後為姓名
        idno.append(i1)
        name.append(i2)   
    stuinfo = {"ID": idno, "name": name,}
    info_df = pd.DataFrame.from_dict(stuinfo)
    if os.path.isfile("./student_info.csv") == False:
        info_df.to_csv("./student_info.csv", sep=',', index=False)


photopath = []
for i in namejpg:
    i = './students/' + i
    photopath.append(i)
fsource = {"photo": photopath,
           "attended": -1}
fsource_df = pd.DataFrame.from_dict(fsource)

def compare_faces(sourceFile, targetFile):
    client = boto3.client('rekognition')
    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')
    response = client.compare_faces(SimilarityThreshold=70,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})
    return response
        
    
def compute(response):    
    position = 0
    similarity = 0    
    if (len(response['FaceMatches']) == 1):
        position = response['FaceMatches'][0]['Face']['BoundingBox']
        similarity = response['FaceMatches'][0]['Similarity']
    return similarity, position


def show_faces(position, targetFile):
    with open(targetFile, 'rb') as image:
        targetFile = image.read()
    stream = io.BytesIO(targetFile)
    image = Image.open(stream)
    
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    left = imgWidth * position['Left']
    top = imgHeight * position['Top']
    width = imgWidth * position['Width']
    height = imgHeight * position['Height']

    points = (
        (left, top),
        (left + width, top),
        (left + width, top + height),
        (left, top + height),
        (left, top)
    )
    draw.line(points, fill='#00d400', width=3)

    image.save('./result.jpg')


def main(target_file):
    oriPhoto = Image.open(target_file)
    oriPhoto.save('./result.jpg')
    initial()    
    n = len(namejpg)
    for i in range(n):
        source_file = fsource_df.iat[i, 0]
        print('正在比對人臉編號 %s...' %(i+1))
        response = compare_faces(source_file, target_file)
        sim, pos = compute(response)
    
        if (sim >= 70):  # 閾值自己設定
            fsource_df.iat[i, 1] = 1
            show_faces(pos, './result.jpg')
            print('人臉編號 %s matched' %(i+1))
        else:
            fsource_df.iat[i, 1] = 0
            print('人臉編號 %s unmatched' %(i+1))
   
    t = time.strftime("%m%d_%H%M", time.localtime()) 
    newname = t + '.jpg'
    os.rename('result.jpg', newname)  #更改輸出照片檔名為當下時間
    
    result_df = fsource_df.drop(columns='photo')
    result_df.columns = [t]
    print('Completed')
    showPhoto = Image.open(newname)
    showPhoto.show()
    
    return result_df

