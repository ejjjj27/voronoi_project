#   $LAN=python$ 
# Author: 陳宜杰
# Student ID: M133040097
# Class: 資工碩一
# Date: 2024-11-15

import re
import tkinter as tk
import math
from tkinter import filedialog
from typing import List
import os

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_value(self):
        return self.x, self.y
    
    def get_mid(self, other):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)
    
    def get_length(self, other):
        return math.sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
    
    def __lt__(self, other) -> bool:
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
        
class Edge:
    def __init__(self, start: Point, end: Point, start_BS = None, end_BS = None):
        self.start = start
        self.end = end
        self.start_BS = start_BS
        self.end_BS = end_BS
        
    def get_vector(self):
        vector = Point(self.end.x - self.start.x, self.end.y - self.start.y)
        return vector
    
    def get_mid(self):
        mid = Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)
        return mid
    
    def get_normal(self):
        v = self.get_vector()
        normal = Point(-v.y, v.x)
        return normal
    
    def plus(self, a, b):
        x = a.x + b.x
        y = a.y + b.y
        return Point(x, y)
    
    def get_BS(self):
        BS_start = Point(self.get_normal().x * 300, self.get_normal().y * 300)
        BS_end = Point(self.get_normal().x * -300, self.get_normal().y * -300)
        bisector = Edge(self.plus(self.get_mid(), BS_start), self.plus(self.get_mid(), BS_end), self.start, self.end)
        return bisector
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Edge):
            return (self.start == other.start and self.end == other.end) or (self.start == other.end and self.end == other.start)
        return False
        
    def __repr__(self):
        return f"({self.start}, {self.end}, {self.start_BS}, {self.end_BS})"

class VD:
    def __init__(self, ):
        self.P_list : List[Point] = []
        self.HP_list : List[Edge] = []
        self.E_list : List[Edge] = []
        
    def VD_clear(self):
        self.P_list = []
        self.HP_list = []
        self.E_list = []
        
class VoronoiApp:
    def __init__(self, root):
        self.voronoi = VD()     # store point, hp, edge
        self.root = root
        self.data_lines = []    # for input data
        self.current_index = 0
        self.i = 0
        self.var = tk.IntVar(value=self.i)
        self.root.title("Voronoi Diagram")
        self.root.geometry("700x750")
        self.isrun = False

        # 設置畫布
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack()
        
        # 設置按鈕
        self.run = tk.Button(self.root, text="執行結果", command=self.run).pack(side=tk.LEFT)
        self.step_by_step = tk.Button(self.root, text="Step by step", command=self.step_by_step).pack(side=tk.LEFT)
        self.open_file_button = tk.Button(self.root, text="開啟檔案", command=self.open_file).pack(side=tk.LEFT)
        self.next_line = tk.Button(self.root, text="下一筆資料", command=self.load_next_line).pack(side=tk.LEFT)
        self.open_output_file_button = tk.Button(self.root, text="開啟輸出檔案", command=self.open_output_file).pack(side=tk.LEFT)
        self.save_file_button = tk.Button(self.root, text="儲存檔案", command=self.save_file).pack(side=tk.LEFT)
        self.clear_button = tk.Button(self.root, text="清除畫布", command=self.clear_canvas).pack(side=tk.LEFT)
        
        # 標籤顯示資料
        self.label = tk.Label(root, text="點擊畫布或開啟檔案", wraplength=380)
        self.label.place(x=500, y=620)
        
        # 註冊滑鼠點擊事件
        self.canvas.bind("<Button-1>", self.add_point)
        # self.canvas.bind('<Key>', self.load_next_line)  # 綁定任意鍵事件
         
    def step_by_step(self):
        if self.i == 0:
            self.i += 1
            voronoi = self.VD_divide_and_conquer(self.voronoi.P_list)
            self.voronoi.E_list = voronoi.E_list
            self.draw_voronoi(voronoi)
            self.step_or_run()
            self.canvas.delete("processing_point")
        else:
            self.i += 1
            self.var.set(self.i)
            
    def run(self):
        self.isrun = True
        self.voronoi = self.VD_divide_and_conquer(self.voronoi.P_list)
        self.draw_voronoi(self.voronoi)
        self.canvas.delete("processing_point")
        
    def step_or_run(self):
        if self.isrun == False:
            self.canvas.wait_variable(self.var)
    
    def open_output_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.read_output_file(filepath)
            
    def read_output_file(self, filepath):
        with open(filepath, 'r', errors="ignore") as file:
            self.voronoi.P_list = []
            for line in file:
                # line = file.readline().strip()
                line = line.strip()
                parts = re.split(r'\s+', line)
                
                if len(parts) == 0:
                    continue
                
                if parts[0] == 'P':
                    if len(parts) == 3:
                        x, y = float(parts[1]), float(parts[2])
                        p = Point(x, 600 - y)   #   把座標變為往上為+Y
                        self.voronoi.P_list.append(p)
                        self.canvas.create_oval(p.x - 2, p.y - 2, p.x + 2, p.y + 2, fill="black")
                elif line.startswith("E"):
                    if len(parts) == 5:
                        x1, y1, x2, y2 = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                        e = Edge(Point(x1, 600 - y1), Point(x2, 600 - y2))   #   把座標變為往上為+Y
                        self.voronoi.E_list.append(e)
                        self.canvas.create_line(e.start.x, e.start.y, e.end.x, e.end.y, fill="black")
                # print(p.x, p.y)
            # print(self.voronoi.P_list)
            # self.VD_divide_and_conquer()
            
    def open_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.read_input_file(filepath)
        
    def read_input_file(self, filepath):
        try:
            with open(filepath, 'r', errors="ignore") as file:
                self.data_lines = file.readlines()
                self.load_next_line(event=None)
                self.canvas.focus_set()
        
            if not self.data_lines:
                self.label.config(text="empty file")
                
        except FileNotFoundError:
            self.label.config(text="找不到檔案！請確認檔案名稱。")
    
    def load_next_line(self, event=None):
        self.voronoi.VD_clear()
        self.canvas.delete("all")
        self.i = 0
        self.isrun = False
        if self.current_index < len(self.data_lines):
            current_data = self.data_lines[self.current_index].strip()
            # print(current_data)
            self.label.config(text=f"讀取點數: {current_data}")
            self.current_index += 1
            
            # 資料檢查
            if current_data.startswith("#") or not current_data:
                return self.load_next_line()
            if current_data == "0":
                return
            
            # 取得該段落的點數量, 清空上一次的紀錄
            num_points = int(current_data)

            for _ in range(num_points):
                current_data = self.data_lines[self.current_index].strip()
                # print(current_data)
                self.current_index += 1
                x, y = map(int, re.split(r'\s+', current_data))
                p = Point(x, 600 - y)   #   把座標變為往上為+Y
                self.draw_point(p, "black", "point")
                self.voronoi.P_list.append(p)
            
            # 去做VD，做完暫停並等待按鍵
            self.step_or_run()  #   wait for step by step
        else:
            self.label.config(text="所有資料已讀取完畢！")
                
    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            self.write_output_file(filepath)
            
    def write_output_file(self, filepath):
        with open(filepath, 'w') as file:
            for p in self.voronoi.P_list:
                p.y = 600 - p.y
            self.voronoi.P_list.sort(key=lambda v: v.y)  # 先按 y 排序
            self.voronoi.P_list.sort(key=lambda v: v.x)  # 再按 x 排序
            for p in self.voronoi.P_list:
                x = p.x
                y = 600 - p.y
                file.write(f"P {x} {y}\n")
            self.voronoi.E_list.sort(key=lambda seg: (seg.start.x, seg.start.y, seg.end.x, seg.end.y))  # 做線段排序
            for seg in self.voronoi.E_list:
                if seg.start.x > seg.end.x or (seg.start.x == seg.end.x and 600 - seg.start.y > 600 - seg.end.y):
                    seg.start, seg.end = seg.end, seg.start
            for e in self.voronoi.E_list:
                x1 = e.start.x
                y1 = e.start.y
                x2 = e.end.x
                y2 = e.end.y
                file.write(f"E {x1} {y1} {x2} {y2}\n")                    
            
    def add_point(self, event):
        # self.canvas.delete("line")
        # self.voronoi.E_list = []
        x, y = event.x, event.y
        p = Point(x, 600 - y)   #   把座標變為往上為+Y
        self.voronoi.P_list.append(p)
        print(p.get_value())
        self.draw_point(p, "black", "point")
        
    def draw_point(self, p : Point, color, name):
        draw_y = 600 - p.y
        self.canvas.create_oval(p.x - 2, draw_y - 2, p.x + 2, draw_y + 2, fill=color, tags=name)
        
    def draw_edge(self, e : Edge, color, name):
        draw_start_y = 600 - e.start.y
        draw_end_y = 600 - e.end.y
        self.canvas.create_line(e.start.x, draw_start_y, e.end.x, draw_end_y, fill=color, tags=name)
        
    def draw_voronoi(self, v : VD):
        self.canvas.delete("line")
        for e in v.E_list:
            if e.start == e.end:
                v.E_list.remove(e)
                continue
            # print(e)
            self.draw_edge(e, "black", "edge")
        
    def clear_canvas(self):
        self.canvas.delete("all")
        self.current_index = 0
        self.data_lines = []
        self.voronoi.VD_clear()
        self.i = 0
        self.isrun = False
        self.label.config(text=f"讀取點數: {0}")
    
    def VD_divide_and_conquer(self, p_list : List[Point]):
        p_list.sort(key=lambda v: (v.x, v.y))  # 先按 x 排序, 再按 y 排序
        voronoi = VD()
        voronoi.P_list = p_list
        if len(p_list) == 1:
            return voronoi
        elif len(p_list) == 2:
            for p in p_list:
                self.draw_point(p, "yellow", "processing_point")
                
            self.step_or_run()  #   wait for step by step
            
            voronoi = self.VD_2point(p_list, voronoi)
            return voronoi
        elif len(p_list) == 3:
            for p in p_list:
                self.draw_point(p, "yellow", "processing_point")
            self.step_or_run()  #   wait for step by step
            voronoi = self.VD_3point(p_list, voronoi)
            return voronoi
        else:
            num = len(p_list)
            
            left_P_list = p_list[:(num + 1) // 2]
            right_P_list = p_list[(num + 1) // 2:]
            # print("dividing.")
            self.canvas.itemconfig("gray", fill="black")
            mid_point_x = left_P_list[-1].get_mid(right_P_list[0]).x
            divide_line = Edge(Point(mid_point_x, 1000), Point(mid_point_x, -1000))
            self.draw_edge(divide_line, "gray", "divide")    #   畫出分線
            
            self.step_or_run()  #   wait for step by step
            left_voronoi : VD = self.VD_divide_and_conquer(left_P_list)
            for e in left_voronoi.E_list:
                self.draw_edge(e, "red", "processing_left_VD")    #   畫出左邊的VD
            self.step_or_run()  #   wait for step by step
            self.canvas.delete("processing_point")
            
            self.step_or_run()  #   wait for step by step
            right_voronoi : VD = self.VD_divide_and_conquer(right_P_list)
            for e in right_voronoi.E_list:
                self.draw_edge(e, "blue", "processing_right_VD")    #   畫出右邊的VD
            self.step_or_run()  #   wait for step by step
            self.canvas.delete("processing_point")
            # print("divide done.")
            
            self.step_or_run()  #   wait for step by step
            self.canvas.delete("divide")
            
            self.step_or_run()  #   wait for step by step
            v = self.VD_merge(left_voronoi, right_voronoi)
            self.canvas.delete("processing_left_VD")
            self.canvas.delete("processing_right_VD")
            self.draw_voronoi(v)
            return v
    
    def VD_merge(self, left_VD : VD, right_VD : VD):
        # print("ready to calculate convexhull.")
        left_convex_hull = self.cal_convexhull(left_VD.P_list)
        self.step_or_run()  #   wait for step by step
        
        right_convex_hull = self.cal_convexhull(right_VD.P_list)
        self.step_or_run()  #   wait for step by step
        # print("convexhull done.")
        
        # print("ready to calculate tangents.")
        tangents = self.cal_tangents(left_convex_hull, right_convex_hull)   #   同時也得到merge後的convexhull
        self.step_or_run()  #   wait for step by step
        # print("tangents done.")
        
        # print("ready to calculate hyperplane.")
        v = self.cal_hyperplane_and_graph(left_VD, right_VD, tangents)
        self.canvas.delete("hyperplane")
        return v
    
    def cal_convexhull(self, p_list : List[Point]):
        p_list = sorted(p_list) #   排序
        lower : List[Point] = []
        
        # 下半部分的凸包
        for p in p_list:
            while len(lower) >= 2 and self.cross(lower[-2], lower[-1], p) >= 0:
                lower.pop()
            lower.append(p)
        
        upper : List[Point] = []
        
        # 上半部分的凸包
        for p in reversed(p_list):
            while len(upper) >= 2 and self.cross(upper[-2], upper[-1], p) >= 0:
                upper.pop()
            upper.append(p)
        convex = lower[:-1] + upper[:-1]
        self.draw_convexhull(convex)
        
        return convex
    
    def draw_convexhull(self, convex : List[Point]):
        for i, p in enumerate(convex):
            self.draw_edge(Edge(convex[i], convex[(i + 1) % len(convex)]), "yellow", "convex")
        
    def cal_tangents(self, left_hull : List[Point], right_hull : List[Point]):
        tangents : List[Edge] = []
        total_point = left_hull + right_hull
        total_point = sorted(total_point, key=lambda p: (p.x, p.y))
        convex_hull = self.cal_convexhull(total_point)
        self.canvas.delete("convex")
        self.draw_convexhull(convex_hull)
        
        for i, p in enumerate(convex_hull):
            # print(p.get_value())
            next_p = convex_hull[(i + 1) % len(convex_hull)]
            if (p in left_hull and next_p in right_hull) or (p in right_hull and next_p in left_hull):
                tangents.append(Edge(convex_hull[i], convex_hull[(i + 1) % len(convex_hull)]))

        #   here need to record convex hull
        return tangents
        
    def cal_hyperplane_and_graph(self, left_VD : VD, right_VD : VD, tangents : List[Edge]):
        v = VD()
        cut : List[int] = []    # index of the line needed to cut
        delete : List[int] = [] # index of the line needed to delete
        last_hited_edge = Edge(None, None)
        last_hited_point = Point(None, None)
        hit_point = Point(None, None)
        candidate = Edge(None, None)
        for i in left_VD.P_list:
            v.P_list.append(i)
        for i in right_VD.P_list:
            v.P_list.append(i)
        for i in left_VD.E_list:
            v.E_list.append(i)  #   無限延伸的邊
        for i in right_VD.E_list:
            v.E_list.append(i)  #   無限延伸的邊
        # for i in v.E_list:
        #     self.draw_edge(i)
        
        scan_line = Edge(tangents[0].start, tangents[0].end)    #   上切線是一開始
        last_hited_point = scan_line.get_BS().start
        
        while not scan_line == tangents[1]: #   每個iterator換一條scan_line直到下切線
            hyperplane = scan_line.get_BS()
            hit_point = Point(None, None)
            for i, e in enumerate(v.E_list):
                if not last_hited_edge == Edge(None, None) and last_hited_edge == e:
                    continue
                
                # print(f'HP : {hyperplane}\te : {e}')
                p = self.cal_intersection(hyperplane, e)    #   用來儲存HP跟VD的每一個交點
                if p is not None and last_hited_point is not Point(None, None):
                    if last_hited_point.y is not None and p.y is not None and last_hited_point.y >= p.y:
                        if hit_point == Point(None, None):  #   第一次的交點
                            hit_point = p
                            candidate = e
                            continue
                        if hyperplane.start.get_length(p) < hyperplane.start.get_length(hit_point): #   在線段上離HP的起點越近的話
                            hit_point = p
                            candidate = e
            if last_hited_point != Point(None, None):
                hyperplane.start = last_hited_point
            v.HP_list.append(Edge(hyperplane.start, hit_point, scan_line.start, scan_line.end))
            # print(f"Candidate: {candidate}")
            # print(f"Index of candidate in v.E_list: {v.E_list.index(candidate)}")
            cut.append(v.E_list.index(candidate))
            # print("candidate : ", candidate)
            # print()
            last_hited_edge = candidate
            last_hited_point = hit_point
            
            #   find next scan_line
            if scan_line.start == candidate.start_BS:
                scan_line.start = candidate.end_BS
            elif scan_line.start == candidate.end_BS:
                scan_line.start = candidate.start_BS
            elif scan_line.end == candidate.start_BS:
                scan_line.end = candidate.end_BS
            elif scan_line.end == candidate.end_BS:
                scan_line.end = candidate.start_BS
        # print("while loop done.")
        #   debug end
        if tangents[0] == tangents[1]:
            v.HP_list.append(Edge(tangents[0].get_BS().start, tangents[0].get_BS().end, scan_line.start, scan_line.end))
        else:
            v.HP_list.append(Edge(hit_point, tangents[1].get_BS().start, scan_line.start, scan_line.end))
        # here need to record hyperplane
        for e in v.HP_list:
            self.draw_edge(e, "green", "hyperplane")
        self.step_or_run()  #   wait for step by step
        for i, c in enumerate(cut): #   往哪邊轉就消哪邊
            if self.cross(v.HP_list[i].start, v.HP_list[i].end, v.HP_list[i+1].end) >= 0:   #   往逆時針轉
                if self.cross(v.HP_list[i].start, v.HP_list[i].end, v.E_list[c].start) > 0: #   要消除的線的start在右邊
                    for e in v.E_list:
                        if e.start == v.E_list[c].start and not e.end == v.E_list[c].end:   #   檢查除了cut以外的線，有沒有經過HP
                            if self.cross(v.HP_list[i].end, e.start, e.end) > 0:
                                delete.append(v.E_list.index(e))
                        elif e.end == v.E_list[c].start and not e.start == v.E_list[c].end: #   檢查除了cut以外的線，有沒有經過HP
                            if self.cross(v.HP_list[i].end, e.end, e.start) > 0:
                                delete.append(v.E_list.index(e))
                    v.E_list[c].start = v.HP_list[i].end                                    #   讓HP轉向的線
                else:                                                                       #   要消除的線的start在左邊
                    for e in v.E_list:
                        if e.start == v.E_list[c].end and not e.end == v.E_list[c].start:
                            if self.cross(v.HP_list[i].end, e.start, e.end) > 0:
                                delete.append(v.E_list.index(e))
                        elif e.end == v.E_list[c].end and not e.start == v.E_list[c].start:
                            if self.cross(v.HP_list[i].end, e.end, e.start) > 0:
                                delete.append(v.E_list.index(e))
                    v.E_list[c].end = v.HP_list[i].end
            elif self.cross(v.HP_list[i].start, v.HP_list[i].end, v.HP_list[i+1].end) < 0:  #   往HP順時針轉
                if self.cross(v.HP_list[i].start, v.HP_list[i].end, v.E_list[c].start) < 0: #   要消除的線的start在左邊
                    for e in v.E_list:
                        if e.start == v.E_list[c].start and not e.end == v.E_list[c].end:   #   
                            if self.cross(v.HP_list[i].end, e.start, e.end) < 0:
                                delete.append(v.E_list.index(e))
                        elif e.end == v.E_list[c].start and not e.start == v.E_list[c].end:
                            if self.cross(v.HP_list[i].end, e.end, e.start) < 0:
                                delete.append(v.E_list.index(e))
                    v.E_list[c].start = v.HP_list[i].end
                else:                                                                       #   要消除的線的start在右邊
                    for e in v.E_list:
                        if e.start == v.E_list[c].end and not e.end == v.E_list[c].start:
                            if self.cross(v.HP_list[i].end, e.start, e.end) < 0:
                                delete.append(v.E_list.index(e))
                        elif e.end == v.E_list[c].end and not e.start == v.E_list[c].start:
                            if self.cross(v.HP_list[i].end, e.end, e.start) < 0:
                                delete.append(v.E_list.index(e))
                    v.E_list[c].end = v.HP_list[i].end
        delete = sorted(set(delete), reverse=True)
        for i in delete:
            v.E_list.pop(i)
        # here need to record voronoi
        
        for e in v.HP_list:
            v.E_list.append(e)
        # here need to record merge
        
        return v
            
    def cal_intersection(self, e1 : Edge, e2 : Edge):
        x1, y1 = e1.start.x, e1.start.y
        x2, y2 = e1.end.x, e1.end.y
        x3, y3 = e2.start.x, e2.start.y
        x4, y4 = e2.end.x, e2.end.y
        
        # 計算線段的方向向量和行列式
        det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if det == 0:
            # 平行或共線
            return None
        # 使用行列式法計算交點坐標
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

        # 檢查交點是否在線段內
        if (min(x1, x2) <= px <= max(x1, x2) and 
            min(y1, y2) <= py <= max(y1, y2) and 
            min(x3, x4) <= px <= max(x3, x4) and 
            min(y3, y4) <= py <= max(y3, y4)):
            return Point(px, py)

        return None  # 交點在延長線上，不在線段內
   
    def VD_2point(self, p_list : List[Point], twopoint_VD : VD):
        e = Edge(p_list[0], p_list[1])
        bs = e.get_BS()
        twopoint_VD.E_list.append(bs)
        return twopoint_VD
    
    def VD_3point(self, p_list : List[Point], threepoint_VD : VD):
        p0, p1, p2 = p_list[0], p_list[1], p_list[2]
        if self.cross(p0, p1, p2) == 0:
            e0 = Edge(p_list[0], p_list[1])
            e1 = Edge(p_list[1], p_list[2])
            threepoint_VD.E_list.append(e0.get_BS())
            threepoint_VD.E_list.append(e1.get_BS())
        else:
            out_center = self.cal_outer_center(p0, p1, p2)
            gravity_center = self.cal_gravity_center(p_list)
            
            for i in range(len(p_list) - 1):
                for j in range(len(p_list) - i - 1):
                    if self.cross(gravity_center, p_list[j], p_list[j + 1]) < 0:
                        tmp = p_list[j + 1]
                        p_list[j + 1] = p_list[j]
                        p_list[j] = tmp
            
            for i in range(len(p_list)):
                e = Edge(out_center, Edge(p_list[i], p_list[(i + 1) % 3]).get_BS().end, p_list[i], p_list[(i + 1) % 3])
                threepoint_VD.E_list.append(e)
        return threepoint_VD
     
    def cal_outer_center(self, p0 : Point, p1 : Point, p2 : Point):
        if p0 == p1 and p1 == p2:
            return p0
        
        Ox_up = (pow(p0.x, 2) + pow(p0.y, 2)) * p1.y + (pow(p2.x, 2) + pow(p2.y, 2)) * p0.y + (pow(p1.x, 2) + pow(p1.y, 2)) * p2.y \
                - (pow(p2.x, 2) + pow(p2.y, 2)) * p1.y - (pow(p0.x, 2) + pow(p0.y, 2)) * p2.y - (pow(p1.x, 2) + pow(p1.y, 2)) * p0.y
        Oy_up = p0.x * (pow(p1.x, 2) + pow(p1.y, 2)) + p2.x * (pow(p0.x, 2) + pow(p0.y, 2)) + p1.x * (pow(p2.x, 2) + pow(p2.y, 2)) \
                - p2.x * (pow(p1.x, 2) + pow(p1.y, 2)) - p0.x * (pow(p2.x, 2) + pow(p2.y, 2)) - p1.x * (pow(p0.x, 2) + pow(p0.y, 2))
        area_triangle = (1/2)*(p0.x * p1.y + p0.y * p2.x + p1.x * p2.y - p2.x * p1.y - p0.x * p2.y - p0.y * p1.x)
        
        Ox = Ox_up / (4*area_triangle)
        Oy = Oy_up / (4*area_triangle)
        return Point(Ox, Oy)
        
    def cal_gravity_center(self, P_list : List[Point]):
        G_x = 0
        G_y = 0
        for i in range(len(P_list)):
            G_x += P_list[i].x
            G_y += P_list[i].y
        return Point(G_x/len(P_list), G_y/len(P_list))
    
    def cross(self, p1 : Point, p2 : Point, p3 : Point):
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = VoronoiApp(root)
    root.mainloop()