import cv2 as cv
from itertools import count
from util import get_features
from sklearn.neighbors import NearestCentroid


def scale(frame, dim):
    d = min(frame.shape[:2])
    view = frame[:d, :d]
    return cv.resize(view, dim)


def extractor(cap, dim):
    _, frame = cap.read()
    frame = scale(frame, dim)
    prev_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    prev_flow = None
    for i in count(0):
        _, frame = cap.read()
        if frame is None:
            break
        frame = scale(frame, dim)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])

        if i > 1:
            yield get_features(prev_flow, flow)

        prev_gray = gray
        prev_flow = flow


clf = NearestCentroid()
X, y = [], []
X2, y2 = [], []
for folder in ['mecca', 'marathon', 'wave', 'mecca', 'marathon', 'wave']:
    cap = cv.VideoCapture(f'./{folder}/crop_1.mkv')
    cnt = 0
    for feature in extractor(cap, (128, 128)):
        cnt += 1
        X.append(feature)
        y.append(folder)
        if cnt >= 5:
            X2.append([sum(i)/5 for i in zip(*X[-5:])])
            y2.append(folder)

clf.fit(X2, y2)

folders = ['mecca', 'marathon', 'wave']
files = ['crop_1.mkv', 'crop_2.mkv', 'crop_3.mkv']
features = []
for video in [i+'/'+j for i in folders for j in files]:
    cap = cv.VideoCapture(f'./{video}')

# while True:
#     video = input('path to file: ')
#     video = 0 if video == '0' else video
#     try:
#         cap = cv.VideoCapture(video)
#     except:
#         print('not found')
#         continue
    cnt = 0
    for feature in extractor(cap, (128, 128)):
        features.append(feature)
        cnt += 1
        if cnt >= 5:
            print(f'{video}, {clf.predict([[sum(i)/5 for i in zip(*features[-5:])]])[0]}')
