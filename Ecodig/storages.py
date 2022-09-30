from storages.backends.s3boto3 import S3Boto3Storage 
class MediaStorage(S3Boto3Storage):    
    location = 'mediaProt/media'    
    file_overwrite = False




class ProtectedMediaStorage(S3Boto3Storage):
    location = 'mediaProt/protected'
    file_overwrite = False