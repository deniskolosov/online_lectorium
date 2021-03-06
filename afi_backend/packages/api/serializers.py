
from rest_framework_json_api import serializers
from afi_backend.packages.models import VideoLecturePackage, VideoCoursePackage
from afi_backend.events.api.serializers import VideoLectureSerializer
from afi_backend.videocourses.api.serializers import VideoCourseSerializer


class VideoLecturePackageSerializer(serializers.ModelSerializer):
    videolectures = VideoLectureSerializer(read_only=True, many=True)
    included_serializers = {'videolectures': VideoLectureSerializer}

    class Meta:
        model = VideoLecturePackage
        fields = ['videolectures', 'price', 'image', 'description', 'release_date']


class VideoCoursePackageSerializer(serializers.ModelSerializer):
    videocourses = VideoCourseSerializer(read_only=True, many=True)
    included_serializers = {
        'videocourses': VideoCourseSerializer,
    }

    class Meta:
        model = VideoCoursePackage
        fields = ['videocourses', 'price', 'image', 'description', 'release_date']
