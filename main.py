import cv2
import numpy as np
import matplotlib.pyplot as plt

print("処理したい内容を選択してください\n-0 : 画像の輝度値の取得\n-1 : 画像の二値化")
mode = int(input(">"))
if mode == 0:
    print("出力方式を選択してください\n-0 : csvファイル\n-1 : ヒストグラム(.png)\n-2 : 両方")
    vMode = int(input(">"))
#ファイル名を指定
print("操作したい画像の個数を教えてください")
howMany = int(input(">"))
print("操作したい画像のディレクトリを相対パスで入力してください")
files = []
for i in range(howMany):
    bcn = input(">")
    files.append(bcn)
    if(i!=howMany):
        print("次の画像のディレクトリを入力してください")

#画像の読み込み
imgs = []
for i in range(howMany):
    imgs.append(cv2.imread(str(files[i])))

#輝度に使うのはv
hsv = []
h,s,v=[],[],[]
for i in range(len(imgs)):
    #画像をHSV方式に変換
    hsv_img = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2HSV)
    hsv.append(hsv_img)
    hi, si, vi = cv2.split(hsv_img)
    h.append(hi)
    s.append(si)
    v.append(vi)#輝度に使うのはv
    if mode == 0 and (vMode == 1 or vMode == 2):
        #ヒストグラムをファイルに出力
        plt.hist(v[i].ravel(), bins=256, range=(0,256))
        plt.savefig(f"hist{i}.png")
        plt.clf()  # グラフをクリア
    elif mode == 0 and (vMode == 0 or vMode == 2):
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
    elif mode == 1:
        # 画像をPタイル法で二値化
        gray = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2GRAY)
        print("画像の閾値を指定してください(0-1)")
        p_tile = float(input(">"))  # 50%を白にする
        total_pixels = gray.size
        target_white = int(total_pixels * p_tile)

        # ヒストグラムを計算
        hist = cv2.calcHist([gray], [0], None, [256], [0,256]).flatten()
        # 上位から何画素目まででtarget_whiteを超えるか
        cumulative = np.cumsum(hist[::-1])  # 画素値255から累積
        threshold = 255 - np.searchsorted(cumulative, target_white)

        # 二値化
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f"binary_{i}.png", binary)  
        print(f"二値化画像を保存しました: binary_{i}.png")
    else:
        break
    







