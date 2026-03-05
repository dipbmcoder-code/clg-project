import os
import shutil
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()


def save_image_locally(id, lang, types):
    """
    Save the generated image to a persistent dated local directory.
    Replaces AWS upload — images stay on disk organized by date.
    
    Source: result/img_match/{lang}_{id}_{types}.png  (temp generation path)
    Dest:   result/images/YYYY-MM-DD/{lang}_{id}_{types}.png  (permanent archive)
    
    The temp file in img_match/ is kept so WordPress upload in publish() still works.
    """
    img_path = root_folder / 'result' / 'img_match' / f'{lang}_{id}_{types}.png'
    if not img_path.exists():
        print(f"⚠️ Image file not found for local save: {img_path}")
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_LOCAL_SAVE,
                MessageStatus.ERROR,
                "Local image save failed",
                error_details="Image file does not exist"
            )
        return None

    try:
        today_str = datetime.now().strftime("%Y-%m-%d")
        archive_dir = root_folder / 'result' / 'images' / today_str
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_path = archive_dir / f'{lang}_{id}_{types}.png'
        shutil.copy2(str(img_path), str(archive_path))

        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_LOCAL_SAVE,
                MessageStatus.SUCCESS,
                f"Image saved locally: {archive_path}"
            )

        print(f"💾 Image saved locally → {archive_path}")
        return str(archive_path)

    except Exception as e:
        error_msg = f"Error saving image locally: {e}"
        print(f"❌ {error_msg}")
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_LOCAL_SAVE,
                MessageStatus.ERROR,
                "Local image save failed",
                error_details=str(e)
            )
        return None
