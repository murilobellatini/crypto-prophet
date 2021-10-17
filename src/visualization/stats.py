import matplotlib.pyplot as plt


def plot_stats_regressor(model, X, y, test_name=None):
    y_pred = model.predict(X)

    score = model.score(X, y)  
    print(f"{test_name} - R^2 score: ", score)

    plt.scatter(y, y_pred, label="original", alpha=0.2)
    plt.xlabel('groud truth (y)')
    plt.ylabel('prediction (y)')
    plt.title(f"Model ground truth and predicted data ({test_name})")
    plt.legend()
    plt.show()