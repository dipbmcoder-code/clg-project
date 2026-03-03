import boto3
import os
import shutil
from datetime import datetime
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()

def save_aws(id, lang, types):
    img_path = root_folder / 'result' / 'img_match' / f'{lang}_{id}_{types}.png'
    if not img_path.exists():
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_AWS_UPLOAD,
                MessageStatus.ERROR,
                "AWS upload failed",
                error_details="Image file does not exist"
            )
        return
    print("Image exists")
    try:
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_access_key = os.getenv('AWS_SECRET')
        client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
        bucket_name = os.getenv('AWS_BUCKET_NAME')
        key = f"match/{lang}_{id}_{types}.png"
        
        client.upload_file(str(img_path), bucket_name, key, ExtraArgs={'ACL':'public-read'})
        aws_url = f"{os.getenv('AWS_URL')}/{key}"

        # Track successful AWS upload
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_AWS_UPLOAD,
                MessageStatus.SUCCESS,
                f"Image uploaded to AWS successfully"
            )

        print(f"[INFO] Image uploaded to AWS: {aws_url}")
        return aws_url
    except Exception as _ex:
        error_msg = f"Error in saving image in aws: {_ex}"
        print(error_msg)

        # Track AWS upload error
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_AWS_UPLOAD,
                MessageStatus.ERROR,
                "AWS upload failed",
                error_details=str(_ex)
            )
        return


#save_aws('868044', 'preview')
def delete_img(id, lang, types):
    img_path = root_folder / 'result' / 'img_match' / f'{lang}_{id}_{types}.png'
    if img_path.exists():
        # Archive the image to a dated folder before deleting
        try:
            today_str = datetime.now().strftime("%Y-%m-%d")
            archive_dir = root_folder / 'result' / 'images' / today_str
            archive_dir.mkdir(parents=True, exist_ok=True)
            archive_path = archive_dir / f'{lang}_{id}_{types}.png'
            shutil.copy2(str(img_path), str(archive_path))
            print(f"📸 Image archived → {archive_path}")
        except Exception as e:
            print(f"⚠️ Failed to archive image: {e}")
        os.remove(img_path)


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
                MessageStage.IMAGE_AWS_UPLOAD,
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
                MessageStage.IMAGE_AWS_UPLOAD,
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
                MessageStage.IMAGE_AWS_UPLOAD,
                MessageStatus.ERROR,
                "Local image save failed",
                error_details=str(e)
            )
        return None
