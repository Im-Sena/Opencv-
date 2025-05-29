import cv2
import numpy as np
import matplotlib.pyplot as plt


#ファイル名を指定
#あとでfor文でまとめるかつはコマンドライン引数で指定できるようにする
file1 = "samples/sample1.pgm" #女
file2 = "samples/sample2.pgm" #光
file3 = "samples/sample3.pgm" #文字

#画像の読み込み
#後でfor文でまとめる
img = []
img1 = cv2.imread(str(file1))
img2 = cv2.imread(str(file2))
img3 = cv2.imread(str(file3))

img = [img1, img2, img3]

#画像をHSV方式に変換
#輝度に使うのはv

hsv = []
h,s,v=[],[],[]
for i in range(3):
    hsv_img = cv2.cvtColor(img[i], cv2.COLOR_BGR2HSV)
    hsv.append(hsv_img)
    hi, si, vi = cv2.split(hsv_img)  # ←ここが正しい
    h.append(hi)
    s.append(si)
    v.append(vi)
    #ヒストグラムをファイルに出力
    plt.hist(v[i].ravel(),256,[0,256])
    plt.savefig(f"hist{i}.png")
    #ヒストグラムの値をcsvに出力
    # 256階調ヒストグラム
    hist256, _ = np.histogram(v[i].ravel(), bins=256, range=(0,256))
    hist256_csv = ",".join(map(str, hist256)) + "\n"
    with open(f"hist256_{i}.csv", "w") as f:
        f.write(hist256_csv)

    # 128階調ヒストグラム（2つずつ合計）
    hist128 = hist256.reshape(128, 2).sum(axis=1)
    hist128_csv = ",".join(map(str, hist128)) + "\n"
    with open(f"hist128_{i}.csv", "w") as f:
        f.write(hist128_csv)







