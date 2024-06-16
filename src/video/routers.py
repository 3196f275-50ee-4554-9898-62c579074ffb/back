import os
import shutil
import uuid
from datetime import timedelta
from fastapi.exceptions import HTTPException
from random import randint
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from fastapi import BackgroundTasks, File, UploadFile, APIRouter, Body, Form
from fastapi import Depends
from fastapi.responses import FileResponse

from src.auth.core.jwt import decode_access_token
from src.dependencies import oauth2_scheme, get_db

from fastapi import WebSocket

from src.video import services
from src.video.services import dump_penalty

router = APIRouter(
    prefix="/video",
    tags=["Video"],
    responses={404: {"description": "Not found"}},
)

def mock_video():
    i = 0


    while True:
        random = randint(0, 10)
        mockdata = True if random > 9 else False
        yield {i:mockdata}

        i += 1


video_gen = mock_video()

@router.websocket("/ws/videooutput")
async def websocket_output(websocket: WebSocket):
    await websocket.accept()
    try:
        async with aiohttp.ClientSession() as Session:
            while True:
                img_file = await websocket.receive_text()
                # async with Session.post('http://<YOLO_server_address>', data=img_file) as resp:
                #     response = await resp.read()
                # это просто для дебага
                await websocket.send_text(str(next(video_gen)))

    except Exception:
        print("websocket disconnected")
        await websocket.close()

@router.websocket("/ws/videoinput")
async def websocket_output(websocket: WebSocket):

    try:
        await websocket.accept()
        async with aiohttp.ClientSession() as Session:
            while True:
                img_file = await websocket.receive_bytes()
                # async with Session.post('http://<YOLO_server_address>', data=img_file) as resp:
                #     response = await resp.read()
                # это просто для дебага
                print(img_file)
                await websocket.send_text(str(next(video_gen)))

    except Exception as e:
        print(f"websocket disconnected{e}")
        await websocket.close()
    finally:
        await websocket.close()



async def process_video(user_id: str,building_id: str, end: int, iter: int, fps: float, db: AsyncSession) -> list:
    i = 0
    index = 0
    results = []
    while i < end:
        rand = randint(0, 100)
        current_time = str(timedelta(seconds=i / fps))
        if rand > 95:
            header = "Danger"
            body = "Something is wrong"

            results.append({"index": index, "header": header, "body": body, "current_time":current_time})
            await dump_penalty(user_id=user_id, building_id=building_id, reason=body, grade = header, db=db)
            index+=1
        elif rand > 70:
            header = "Warning"
            body = "Just a warning"
            results.append({"index": index, "header": header, "body": body, "current_time":current_time})
            await dump_penalty(user_id=user_id,building_id=building_id, reason=body, grade=header, db=db)
            index+=1
        i += iter
    return results



@router.post("/videoinput", response_model=list, status_code=200)
async def video_input(
        building_id: uuid.UUID = Body(...), video: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        size = int(video.size)
        iter_size = size // 10
        fps = 30.0  # заменить на реальную частоту кадров вашего видео
        user_id = '649b657c-3859-4680-b478-2dceb1d4bb8f'
        # if not user:
        #     raise HTTPException(status_code=401, detail="Unauthorized")
        # Получаем результаты из генератора
        results = await process_video(user_id=user_id, building_id=building_id, end=size, iter=iter_size, fps=fps, db=db)

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/video_to_ml")
async def video_to_ml(
        building_id: uuid.UUID = Form(...),
        video: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    try:
        video_path = f"temp/{video.filename}"
        with open(video_path, 'wb') as buffer:
            shutil.copyfileobj(video.file, buffer)
        img_id=str(uuid.uuid4())
        frames_dir = f"temp/frames_{img_id}"
        os.makedirs(frames_dir)

        results = await services.process_video2(video_path=video_path, db=db, building_id=building_id, user_id="649b657c-3859-4680-b478-2dceb1d4bb8f",img_id=img_id)

        shutil.rmtree(frames_dir)
        os.remove(video_path)


        return results
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mediacatalog")
async def media_catalog():
    catalog = os.listdir("src/media")
    return catalog

@router.get("/imagesmock", status_code=200)
async def images_mock(image: str):
    print(f"src/media/{image}")
    return FileResponse(f"src/media/{image}")

# @router.get("/employees", response_model=list[schemas.Employee])
# async def get_employees(
#         db: AsyncSession = Depends(get_db)
# ):
#     scalar = await services.get_employees(db=db)
#     return scalar
#
#
# @router.post("/add_employee/", response_model=schemas.CreatedResponse)
# async def add_employee(employee: schemas.Employee, db: AsyncSession = Depends(get_db)):
#     new_employee = await services.create_employee(db=db,
#                                    first_name=employee.first_name,
#                                    middle_name=employee.middle_name,
#                                    last_name=employee.last_name)
#
#     return schemas.CreatedResponse()
#
#
# @router.post("/add_violations/", response_model=schemas.CreatedResponse)
# async def add_violation(violation: schemas.Violation, db: AsyncSession = Depends(get_db)):
#     await services.create_violation(db=db,
#                                     name=violation.name,
#                                     description=violation.description)
#
#     return schemas.CreatedResponse()
#
#
#
# @router.get("/get_violations/", response_model=list[schemas.Violation])
# async def get_violations(db: AsyncSession = Depends(get_db)):
#     scalar = await services.get_violations(db=db)
#     return scalar
# @router.delete("/del_violations/{violation_id}", response_model=schemas.DeletedResponse)
# async def del_violation(violation_id : int, db: AsyncSession = Depends(get_db)):
#
#     if await services.get_violation(db, violation_id=violation_id) is None:
#         raise HTTPException(status_code=404, detail="Violation not found")
#     await services.delete_violation(db=db, violation_id=violation_id)
#     return schemas.DeletedResponse()
#
#
# def random_video():
#     return randint(0, 10)
#
#
#
#
#
#
#
#
# # @router.post("/", response_model=GetVideo)
# # async def create_video(
# #         title: str = Form(...),
# #         description: str = Form(...),
# #         file: UploadFile = File(...),
# #         user: User = Depends(get_user)
# # ):
# #     """ Add video """
# #     return await save_video(user, file, title, description)
#
#
# @router.get("/videos/", response_model=List[schemas.Video])
# async def read_videos(db: AsyncSession = Depends(get_db)):
#     return await services.get_videos(db)
#
#
# @router.get("/videos/{video_id}", response_model=schemas.Video)
# async def read_video(video_id: int, db: AsyncSession = Depends(get_db)):
#     video = await services.get_video(db, video_id=video_id)
#     if video is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return video
#
#
# # Routes for Violations
# # @router.get("/violations/", response_model=List[schemas.Violation])
# # def read_violations(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_db)):
# #     return services.get_violations(db, skip=skip, limit=limit)
#
# @router.get("/violations/", response_model=List[schemas.Violation])
# async def read_violations(db: AsyncSession = Depends(get_db)):
#     violation = await services.get_violations(db)
#     if violation is None:
#         raise HTTPException(status_code=404, detail="Violation not found")
#     return violation
#
# @router.get("/violation/{violation_id}", response_model=schemas.Violation)
# async def read_violation(violation_id: int, db: AsyncSession = Depends(get_db)):
#     violation = await services.get_violation(db, violation_id=violation_id)
#     if violation is None:
#         raise HTTPException(status_code=404, detail="Violation not found")
#     return violation
#
#
# # Routes for Employee
# # @router.get("/employees/", response_model=List[schemas.Employee])
# # def read_employees(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_db)):
# #     return services.get_employees(db, skip=skip, limit=limit)
#
#
# @router.get("/employee/{employee_id}", response_model=schemas.Employee)
# async def read_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
#     employee = await services.get_employee(db, employee_id=employee_id)
#     if employee is None:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return employee
#
#
# # Update and delete routes for Video
# @router.put("/videos/{video_id}", response_model=schemas.Video)
# async def update_video(video_id: int, video: schemas.Video, db: AsyncSession = Depends(get_db)):
#     db_video = await services.get_video(db, video_id=video_id)
#     if db_video is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return services.update_video(db, db_video=video.db_video, video=video.video)
#
# @router.delete("/videos/{video_id}", response_model=schemas.Video)
# async def delete_video(video_id: int, db: AsyncSession = Depends(get_db)):
#     db_video = await services.get_video(db, video_id=video_id)
#     if db_video is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return services.delete_video(db, video_id=video_id)
#
#
# # Update and delete routes for Violation
# @router.put("/violations/{violation_id}", response_model=schemas.Violation)
# async def update_violation(violation_id: int, violation: schemas.Violation, db: AsyncSession = Depends(get_db)):
#     db_violation = await services.get_violation(db, violation_id=violation_id)
#     if db_violation is None:
#         raise HTTPException(status_code=404, detail="Violation not found")
#     return services.update_violation(db, db_violation=db_violation, violation=violation)
#
# @router.delete("/violations/{violation_id}", response_model=schemas.Violation)
# async def delete_violation(violation_id: int, db: AsyncSession = Depends(get_db)):
#     db_violation = await services.get_violation(db, violation_id=violation_id)
#     if db_violation is None:
#         raise HTTPException(status_code=404, detail="Violation not found")
#     return services.delete_violation(db, violation_id=violation_id)
#
#
# # Update and delete routes for Employee
# @router.put("/employees/{employee_id}", response_model=schemas.Employee)
# async def update_employee(employee_id: int, employee: schemas.Employee, db: AsyncSession = Depends(get_db)):
#     db_employee = services.get_employee(db, employee_id=employee_id)
#     if db_employee is None:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return services.update_employee(db, db_employee=db_employee)
#
# @router.delete("/employees/{employee_id}", response_model=schemas.Employee)
# async def delete_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
#     db_employee = services.get_employee(db, employee_id=employee_id)
#     if db_employee is None:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return services.delete_employee(db, db_employee=db_employee)
