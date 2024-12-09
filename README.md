# VORONOI DIAGRAM PROJECT
**資工系碩一 M133040097 陳宜杰**  
  
> **打包工具&指令**  
> pip install pyinstaller  
> pyinstall --onefile main.py
## 軟體規格書 :
###  輸出與輸入（資料）規格 :
- 輸出 : 在畫布上任意點擊以新增點；可以讀入點集資料，格式如vd_testdata.in(有干擾資料，以#為開頭)、vd_testdata_pure.in
- 輸出 : 在畫布上畫出voronoi diagram；亦可將點集、邊集存入txt檔
---
###  功能規格與介面規格 :
- 畫布規格600x600、介面規格700x750

![image](https://github.com/user-attachments/assets/53356a7b-f0bb-4674-b639-0d6dcb03ad17)

- 執行結果 : 直接畫出voronoi diagram及convex hull。
- Step by step : 一步一步展現divide-and-conquer的過程，包括切分點集(直到點集為2、3點)、畫出左右點集之voronoi diagram、畫出左右點集之convex hull、合併左右點集之convex hull、畫出hyperplane、消除多餘的線。
- 開啟檔案 : 可讀入vd_testdata.in或vd_testdata_pure.in
- 下一筆資料 : 適用於讀入檔案後的操作
- 開啟輸出檔案 : 可讀入執行後儲存之檔案(內有點集與邊集)
- 儲存檔案 : 將畫完的voronoi diagram之點集與邊集存入txt檔，並以字典序排列
- 清除畫布 : 就清除畫布
---
### 軟體說明 : 
- 直接點擊main.exe即可使用
- 請勿將「執行結果」與「Step by step」搭配使用
- 「下一筆資料」請在「開啟檔案」後使用
- 「開啟檔案」只能用在格式如vd_testdata.in或vd_testdata_pure.in的資料
- 「開啟輸出檔案」只能開啟 - 透過「儲存檔案」所儲存的檔案
- 有任何問題請點擊「清除畫布」
- Warning ! ! ! 有部分資料會造成程式掛掉，請直接重新開啟程式
---
### 程式設計 : 
- **Class說明** : 包括Point、Edge、VD及VoronoiApp。Point中用來存放點的x、y座標，同時也有幾個function可用於程式內，點的比較與相關操作；Edge是用兩個點來描述，Point start及Point end，Edge內的function可以用來求該條線的向量、法向量、中點、中垂線等等，也提供了比較的功能(__eq__)；VD則由三個list組成，分別是Point的list、Edge的list、hyperplane(也是Edge)的list；最後VoronoiApp提供了各種互動式的按鈕、輸入輸出以及主要做出voronoi diagram的邏輯也放在裡面。
- **三點求VD** : 我是利用cross的方法去找方向，同時也要找出重心及外心，透過重心與其中兩點的方向，來決定VD的edge要從外心往哪邊畫；三點共線的判別也是用外積(=0)。
- **多點求VD** : 用divide-conquer的方式將點集縮小到2、3點，就能直接求得VD，再利用merge的方式將其合成大的VD，依此類推。
- **Merge** : 首先要先求出左右兩點集各自的convex hull然後再求整個convex hull，透過一點在左convex hull、一點在右convex hull的邏輯，找出上下切線，之後就可以開始求hyperplane。第一段hp必定是從上切線進入，再看這一條hp與哪些edge有交點，並且該交點離無窮遠處(也就是hp的另一端)最近，則該交點就是下一段hp的起始，碰到的邊是左VD的那就往右邊轉(把scan line的左端點往下移一個點)，反之亦然，直到掃描到下切線。最後就把多餘的線段消掉(hp向右轉就消右邊的線，反之亦然)，就能畫出merge後的VD。
---
### 軟體測試與實驗結果 : 
- 測試環境 : Window10, Intel Core i7-9750H CPU @ 2.60GHz, VScode, Python3.8
- 測試數據 : 如vd_testdata.in、vd_testdata_pure.in
- 測試極限 : 六點(含)以下，七點以上由於divide 2 次，故畫線會畫錯，應該是因為我是邊做邊畫線，而不是將當前要畫的圖暫存起來，等到最後再畫，例如二次遞迴時畫的線，在回到一次遞迴時應該有部分要消去，但沒有將需要消去的線紀錄下來；應該可以多用個物件將執行divide-and-conquer過程中的數據存起來，就能避免程式中明明已經沒有那個edge了，但是畫布上卻不知道要消掉那個edge。
- ![6點](https://github.com/user-attachments/assets/ed9251e1-9429-47a8-8e93-004032c1edad)
- ![7點(錯誤)](https://github.com/user-attachments/assets/6bacc282-f035-44fc-b631-4b27da04075d)
---
### 結論與心得 : 
這份專題要做到好真的很難，有些數據都很例外暫且不談，光是要想怎麼讓程式照著我的想法去執行就很燒腦了，我認為將腦中的想法轉換成邏輯去讓程式執行是這項作業最困難的地方，聽教授上課時所講的都很好理解，但要這些想法轉化成一個一個的邏輯就很難想像，總之這份作業花了我不少時間，感覺腦細胞也死了不少，好險也有做出一點點成果。
---
### 附錄 : 
- 求外心、重心 : https://ccjou.wordpress.com/2014/04/08/%E5%88%A9%E7%94%A8%E8%A1%8C%E5%88%97%E5%BC%8F%E6%8E%A8%E5%B0%8E%E4%B8%89%E8%A7%92%E5%BD%A2%E7%9A%84%E5%9B%9B%E5%BF%83%E5%BA%A7%E6%A8%99%E5%85%AC%E5%BC%8F/
- 外積求方向 : https://hackmd.io/@peienwu/geometry
