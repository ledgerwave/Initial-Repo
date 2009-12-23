class Perspective:
    # Set up the perspective matrix
    def __init__(self):
        self.update_matrix()

    def warp(self, frame):
        self.frame2 = cvCreateImage(cvSize(width, height), IPL_DEPTH_8U, 3)
        cvWarpPerspective(frame, self.frame2, self.mmat)
        return self.frame2

    def update_matrix(self):
        global height, width, warp_points

        # Create Warp Map
        self.mmat = cvCreateMat(3,3,CV_32FC1)

        # Set up source points
        self.storageSrc = cvCreateMemStorage(0)
        self.src = cvCreateSeq(CV_SEQ_ELTYPE_POINT, sizeof_CvContour, sizeof_CvPoint, self.storageSrc)
        self.src = CvSeq_CvPoint2D32f_cast(self.src)
        self.srcp = [ (warp_points[0][0], warp_points[0][1]), (warp_points[3][0], warp_points[3][1]), (warp_points[1][0], warp_points[1][1]), (warp_points[2][0], warp_points[2][1]) ]
        [cvSeqPush (self.src, cvPoint2D32f(*p)) for p in self.srcp]

        # Now setup DESTINATION points (into dst)
        self.storageDst = cvCreateMemStorage(0)
        self.dst = cvCreateSeq(CV_SEQ_ELTYPE_POINT, sizeof_CvContour, sizeof_CvPoint, self.storageDst)
        self.dst = CvSeq_CvPoint2D32f_cast(self.dst)
        self.dstp = [ (0, 0), (0, height), (width, 0), (width, height) ]
        [cvSeqPush(self.dst, cvPoint2D32f(*p)) for p in self.dstp]

        # Calculate transform MATRIX
        cvGetPerspectiveTransform(self.src[0], self.dst[0], self.mmat)
