import cv2
import matplotlib.pyplot as plt
import shutil
import uvicorn

from fastapi import FastAPI,UploadFile,File,Response,status
from utils import get_plate_rest,lp_mapping
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/predict",status_code=200)
async def read_root(response: Response,media: UploadFile=File(...)):
    with open("img.jpg", "wb") as buffer:
        shutil.copyfileobj(media.file, buffer)
    try:
        lp_img, cors = get_plate_rest("img.jpg")
    except:
        response.status_code = 404
        return
    img=cv2.cvtColor(cv2.imread('img.jpg'),cv2.COLOR_BGR2RGB)/255
    lp_map_img=lp_mapping(img,lp_img[0])
    plt.imsave('lp.jpg',lp_map_img)

    return FileResponse('lp.jpg')

if __name__ == '__main__':
    uvicorn.run("main:app",host="0.0.0.0",port=8080)