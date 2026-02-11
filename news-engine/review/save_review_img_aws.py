import boto3
import os
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
root_folder = Path(__file__).resolve().parents[1]
load_dotenv()

def save_review_aws(fixture_match, types):
    try:
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_access_key = os.getenv('AWS_SECRET')
        
        client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

        list_l = ['eng']
        for i in range(len(list_l)):
            img_path = root_folder / 'result' / 'img_match'
            image_path = img_path / f'{list_l[i]}_{fixture_match}_{types}.png'
            if not image_path.exists():
                # Track file not found error
                if types:
                    from publication.message_tracker import add_message, MessageStage, MessageStatus
                    add_message(
                        types,
                        MessageStage.IMAGE_AWS_UPLOAD,
                        MessageStatus.ERROR,
                        "AWS upload failed",
                        error_details=f"Image file not found: {image_path}"
                    )
                return
            print("Image exists")
            client.upload_file(str(img_path / f"{list_l[i]}_{fixture_match}_{types}.png"), os.getenv('AWS_BUCKET_NAME'), f"match/{list_l[i]}_{fixture_match}_{types}.png", ExtraArgs={'ACL':'public-read'})
        
        client.upload_file(str(img_path / f"{fixture_match}_graph_review.png"), os.getenv('AWS_BUCKET_NAME'), f"match/{fixture_match}_graph_{types}.png", ExtraArgs={'ACL':'public-read'})
        client.upload_file(str(img_path / f"{fixture_match}_lineups_review.png"), os.getenv('AWS_BUCKET_NAME'), f"match/{fixture_match}_lineups_{types}.png", ExtraArgs={'ACL':'public-read'})
        
        # Track successful AWS upload
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_AWS_UPLOAD,
                MessageStatus.SUCCESS,
                f"Images uploaded to AWS successfully"
            )
        
        print(f"[INFO] Review images uploaded to AWS successfully")
            
        sleep(5)
        os.remove(root_folder / 'result' / 'img_match' / f"{fixture_match}_graph_{types}.png")
        os.remove(root_folder / 'result' / 'img_match' / f"{fixture_match}_lineups_review.png")
    
    except Exception as _ex:
        error_msg = f"[ERROR] AWS upload failed: {_ex}"
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

# save_review_aws('855735', 'review')
def delete_review_img(fixture_match, types):
    list_l = ['eng', 'ru']
    for i in range(len(list_l)):
        img_path = root_folder / 'result' / 'img_match'
        img_file = img_path / f"{list_l[i]}_{fixture_match}_{types}.png"
        if img_file.exists():
            os.remove(img_file)
