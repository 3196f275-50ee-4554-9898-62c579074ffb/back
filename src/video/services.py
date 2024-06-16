import shutil
import uuid
from datetime import timedelta
from enum import Enum
from pathlib import Path
from random import randint

from sqlalchemy import select, delete
from typing import List
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from fastapi.background import BackgroundTasks
from src.statistics.models import Penalty as PenaltyModel, PenaltyBuilding as PenaltyBuildingModel
from src.statistics.schemas import Penalty as PenaltySchema
import cv2
from src.video import schemas
from src.video import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

def rand_danger():
    rint = randint(0, 10)
    danger = {
        1: "Нет каски",
        2: "Техника безопасности нарушена",
        3: "Виден неправильный свет",
        4: "Трещины",
        5: "Работа с видео невозможна",
        6: "кадр невидимый",
        7: "Плохое видео",
        8: "Плохое видео",
        9: "Плохое видео",
        10:"Плохое видео",
    }
    return danger[rint]
def rand_warning():
    rint = randint(0, 10)
    warning = {
        1: "Подозрительное видео",
        2: "Плохое видео",
        3: "Не видно",
        4: "Цвет не определен",
        5: "Работа с видео невозможна",
        6: "кадр невидимый",
        7: "Плохое видео",
        8: "Плохое видео",
        9: "Плохое видео",
        10: "Плохое видео",
    }
    return warning[rint]

async def bind_penalty(db: AsyncSession, penalty, building_id: uuid4):
    stmt = insert(PenaltyBuildingModel).values(penalty_id=penalty.id, building_id=building_id)
    await db.execute(stmt)
    await db.commit()


async def dump_penalty(db: AsyncSession, building_id: uuid4, user_id: uuid4, reason: str, grade: str):
    penalty = PenaltyModel(user_id=user_id, reason=reason, grade=grade)
    db.add(penalty)

    await db.commit()
    await bind_penalty(db=db, penalty=penalty, building_id=building_id)


async def process_video2(user_id: uuid.UUID, building_id: uuid.UUID, video_path: str, img_id: str, db: AsyncSession) -> list:
    index = 0
    results = []

    # Открываем видео файл с помощью OpenCV
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise HTTPException(status_code=500, detail="Не удалось открыть видеофайл.")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        raise HTTPException(status_code=500, detail="Не удалось получить FPS из видеофайла.")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_count == 0:
        raise HTTPException(status_code=500, detail="Не удалось получить количество кадров из видеофайла.")

    duration_seconds = frame_count / fps

    # Создание директории для хранения кадров (если она не существует)
    frames_dir = Path(f"temp/frames_{img_id}")
    frames_dir.mkdir(parents=True, exist_ok=True)

    for i in range(int(duration_seconds)):
        # Устанавливаем позицию на каждую секунду
        set_pos_success = cap.set(cv2.CAP_PROP_POS_MSEC, i * 1000)

        if not set_pos_success:
            print(f"Не удалось установить позицию на {i} секунде.")
            continue

        ret, frame = cap.read()

        if not ret or frame is None or frame.size == 0:
            print(f"Не удалось прочитать кадр {i}.")
            continue

        # Записываем кадр из видео на диск
        frame_path = frames_dir / f"frame_{i}.png"
        cv2.imwrite(str(frame_path), frame)

        rand = randint(0, 100)
        current_time = timedelta(seconds=i).__str__()

        header = ''
        body = ''

        if rand > 95:
            header = "Danger"
            body = rand_warning()

        elif rand > 70:
            header = "Warning"
            body = rand_danger()

        if rand > 70:
            results.append({"index": index, "header": header, "body": body, "current_time": current_time})

            await dump_penalty(db=db, user_id=user_id, building_id=building_id, reason=body, grade=header)


        index += 1

    cap.release()
    return results