from pop.AI import Linear_Regression
# import matplotlib.pyplot as plt

x_data = [[173], [171], [162], [187], [157], [169], [177], [159], [182]] #키(cm) -> 데이터(x)
y_data = [[270], [275], [245], [280], [230], [265], [270], [250], [275]] #발크기(mm) -> 레이블/정답(y)
new_x = [[159], [172], [201], [148]]

linear = Linear_Regression(True, ckpt_name="height_free")
prediction_y = linear.run(new_x)

print(prediction_y)
"""
plt.xlabel("height(cm)")
plt.ylabel("feet(mm)")
plt.scatter(x_data, y_data)
plt.scatter(new_x, prediction_y, color='#f0f000', linestyle="-.", marker='o')

plt.show()
"""