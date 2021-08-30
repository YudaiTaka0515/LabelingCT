# What is
CT画像を読み込み, 画像処理を用いてアノテーションを行うスクリプト.
![output](https://user-images.githubusercontent.com/65318542/131350047-7a383897-d142-4e75-9eb8-d17585528228.gif)

# How to Use

## 使用前の注意

- 下記ファイルが存在するか確認する.
  - `AnnotationGUI.py`
  - `Utils.py`
  - `Const.py`
  - `LoadCT.py`

- `Const.py`内のの`DEFAULT_DIR = r"C:\Users\Ritter\Documents\eso_limphCTData2"` を自分の作業フォルダなどに適当に変更する.



## 主な機能

### Dicomファイル /の読み込み

- 左上部の`FIle->Open dicom file`でDicomが格納されているフォルダを開く.

### rawファイルの読み込み

- 左上部の`File->Open Raw File`でrawファイルを開く.

### rawファイルの保存

- 左上部の`File->Save Raw File`でrawファイルを開く.

### 領域拡張法

- `region growing`ボタンを押した後，画像内の任意の点をクリックして実行
- スライドバー`threshold`を変更することで，パラメータを調整する.
  - 値が大きいほどペイントされる領域が大きくなる.

### ブラシ

- `brush`ボタンを押した後，画像内でマウスを動かすことで実行
- スライドバー`太さ`を変更することで，ブラシの太さを変更する.

### クロージング

- ペイントで塗り残した小さい穴を埋める処理.
- `closing`ボタンを押すことで実行.

### 色選択

- 右中段のR, G, Bボタンでペイントの色を赤，緑，青に変更.

### Zoom in/out

- 画像内で右クリック+マウスホイールで画像を拡大/縮小を行う.

### スライスの変更

- `index`スライドバーで値を変更することでスライスを変更．
- マウスホイールでも使用可能．

