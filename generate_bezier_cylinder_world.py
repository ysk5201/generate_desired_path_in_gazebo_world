import csv

MODEL_TEMPLATE = """
    <model name='unit_cylinder_{index}'>
      <pose>{x} {y} 0 0 0 0</pose>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <cylinder>
              <radius>0.000005</radius>
              <length>0.000005</length>
            </cylinder>
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
            <cylinder>
              <radius>0.04</radius>
              <length>0.0005</length>
            </cylinder>
          </geometry>
          <material>
            <script>
              <name>Gazebo/Red</name>
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
            x, y = map(float, row)  # x, y座標をfloat型に変換
            coordinates.append((x, y))
    return coordinates

def generate_models(coordinates):
    """座標リストからモデルを生成"""
    models = []
    for index, (x, y) in enumerate(coordinates):
        models.append(MODEL_TEMPLATE.format(index=index, x=x, y=y))
    return "\n".join(models)

def create_world_file(output_path, models):
    """worldファイルを生成"""
    with open(output_path, mode='w') as file:
        file.write(WORLD_TEMPLATE.format(models=models))

def main():
    # 入力CSVファイル
    input_csv = "bezier_curve_x_y.csv"
    # 出力worldファイル
    output_world = "bezier_cylinder.world"

    # CSVから座標を読み込む
    coordinates = read_csv(input_csv)

    # モデルを生成
    models = generate_models(coordinates)

    # worldファイルを生成
    create_world_file(output_world, models)

    print(f"Worldファイルが生成されました: {output_world}")

if __name__ == "__main__":
    main()
