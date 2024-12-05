import csv
import math


MODEL_TEMPLATE = """
    <model name='unit_box_{index}'>
      <static>true</static>
      <pose>{x} {y} 0 0 0 {th}</pose>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <box>
              <size>0.000005 0.000005 0.000005</size>
            </box>
          </geometry>
          <max_contacts>10</max_contacts>
          <surface>
            <contact>
              <ode/>
            </contact>
            <bounce/>
            <friction>
              <torsional>
                <ode/>
              </torsional>
              <ode/>
            </friction>
          </surface>
        </collision>
        <visual name='visual'>
          <geometry>
            <box>
              <size>{length} {width} {height}</size>
            </box>
          </geometry>
          <material>
            <script>
              <name>Gazebo/Green</name>
              <uri>file://media/materials/scripts/gazebo.material</uri>
            </script>
          </material>
        </visual>
      </link>
    </model>
"""

# Worldテンプレート(include部分とcylinderモデルの追加場所)
WORLD_TEMPLATE = """<?xml version="1.0" ?>
<sdf version="1.5">
  <world name="default">
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://ground_plane</uri>
    </include>
    {models}
    <gui>
      <camera name="user_camera">
        <pose>{view_point_x} {view_point_y} {view_point_z} 0 1.57 1.57 0</pose>
      </camera>
    </gui>
  </world>
</sdf>
"""

def read_csv(file_path):
    """CSVファイルを読み込み、座標リストを返す"""
    coordinates = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            x, y, th = map(float, row)  # x, y, thをfloat型に変換
            coordinates.append((x, y, th))
    return coordinates

def offset_positon(x, y, th, offset):
    x_offset = x + offset * math.cos(th)
    y_offset = y + offset * math.sin(th)
    return x_offset, y_offset

def generate_models(coordinates, length, width, height):
    """座標リストからモデルを生成"""
    models = []
    for index, (x, y, th) in enumerate(coordinates):
        # 一つ目の物体は長さを半分にし, 中心をth方向に0.25 * lengthずらす
        if index == 0:
            offset = 0.25 * length
            x_offset, y_offset = offset_positon(x, y, th, offset)
            obj_length = 0.5 * length
            models.append(MODEL_TEMPLATE.format(index=index, x=x_offset, y=y_offset, th=th, length=obj_length, width=width, height=height))
        elif index == len(coordinates) - 1:
            offset = -0.25 * length
            x_offset, y_offset = offset_positon(x, y, th, offset)
            obj_length = 0.5 * length
            models.append(MODEL_TEMPLATE.format(index=index, x=x_offset, y=y_offset, th=th, length=obj_length, width=width, height=height))
        else:
            obj_length = length
            models.append(MODEL_TEMPLATE.format(index=index, x=x, y=y, th=th, length=obj_length, width=width, height=height))
    return "\n".join(models)

def create_world_file(output_path, models, view_point_x, view_point_y, view_point_z):
    """worldファイルを生成"""
    with open(output_path, mode='w') as file:
        file.write(WORLD_TEMPLATE.format(models=models, view_point_x=view_point_x, view_point_y=view_point_y, view_point_z=view_point_z))

def main():
    # 入力CSVファイル
    input_csv = "bezier_curve_x_y_th.csv"
    # 出力worldファイル
    output_world = "bezier_box.world"

    # 経路用に使う直方体のパラメータ
    length = 0.24
    width  = 0.05
    height = 0.0005

    # 視点位置(上から真下を見下ろす)
    view_point_x = 4
    view_point_y = 4
    view_point_z = 20

    # CSVから座標を読み込む
    coordinates = read_csv(input_csv)

    # モデルを生成
    models = generate_models(coordinates, length, width, height)

    # worldファイルを生成
    create_world_file(output_world, models, view_point_x, view_point_y, view_point_z)

    print(f"Worldファイルが生成されました: {output_world}")

if __name__ == "__main__":
    main()
