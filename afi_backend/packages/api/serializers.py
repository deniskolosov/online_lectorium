from rest_framework_json_api import serializers
from afi_backend.packages.models import VideoLecturePackage, VideoCoursePackage
from afi_backend.events.api.serializers import VideoLectureSerializer
from afi_backend.videocourses.api.serializers import VideoCourseSerializer


class VideoLecturePackageSerializer(serializers.ModelSerializer):
    videolectures = VideoLectureSerializer(read_only=True, many=True)

    class Meta:
        model = VideoLecturePackage
        fields = ['videolectures']


class VideoCoursePackageSerializer(serializers.ModelSerializer):
    videocourses = VideoCourseSerializer(read_only=True, many=True)

    class Meta:
        model = VideoCoursePackage
        fields = ['videocourses']
