"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import json
from ndlapi.api._interfaces.RecognitionService import IRService
from ndlapi.api._pyproto import api_common_pb2 as ac
from ndlapi.api._utils import iterate_over_file_bytes, print_progress


class IVideoService(IRService):
    def __init__(self, auth):
        super().__init__(auth)
        self.media_types.append('video')

    def process_video(self, video_path):
        def create_stream(blob_size):
            for blob_num, blob in enumerate(iterate_over_file_bytes(video_path, blob_size)):
                data = ac.BytesData(data=blob, pack_num=blob_num)
                request = ac.ProcessingRequest(data=data, file_extension=video_path.split('.')[-1])
                print_progress(send_progress=blob_size * blob_num + len(blob))
                yield request
            print()

        response_iterator = self.stub.process_video_stream(create_stream(16 * 2 ** 10))

        print("Establishing connection ... This may take a while")

        processing_ok, result = False, {}
        for response in response_iterator:
            if response.code == ac.TicketStatusCode.Queued:
                print('Your response in queue')

            elif response.code == ac.TicketStatusCode.InProgress:
                print_progress(units_progress=response.units_progress)

            elif response.code == ac.TicketStatusCode.OK:
                processing_ok = True
                for image_res in response.result:
                    result[image_res.num] = json.loads(image_res.result)

            elif response.code == ac.TicketStatusCode.Stopped:
                print("\nYour task had been stopped:", response.msg)

            elif response.code == ac.TicketStatusCode.Failed:
                print("\nThere is an error while processing video:", response.msg)

            elif response.code == ac.TicketStatusCode.Unknown:
                print("\nThere is an unhandled error while processing video:", response.msg)
        print()

        result = self._postprocess_result(result)

        return processing_ok, result

    @staticmethod
    def _postprocess_result(old_result):
        return old_result
