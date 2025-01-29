# tbtui
A terminal board for your ML experiments
> **Pronounced:** "Tee-Bee-Too-EE"

**tbtui** aims to, someday, be a full ML experiment monitoring tool that can be accessed through the terminal. It allows you to check your metrics during training, with the condition that you are saving them as individually named csv files. 
![image](https://github.com/user-attachments/assets/ef815570-d09c-4dc9-9d30-e330fc038df8)

---

## 🚀 Features
1. View experiment metrics right from the terminal.
2. Lightweight and fast.
3. Can be used on remote ssh servers wihtout the need for port-forwarding.
4. Works with any csv-formatted experiment info file.
5. Easily visualize minimum and maximum values in a plot.

## 🎯 Future goals
- [ ] Compare experiments by plotting them in the same graph.
- [ ] Update live on running experiment.
- [ ] Zoom into section to see plot-line better.
- [ ] Search and filter experiments.
- [ ] Multiple metrics plots in the same view.
- [ ] Resizable/Collapsible sidebar.

## 📦 Installation
Install requirements in your python environment (`python=3.9.19` in my experiments) via
```
pip install -r  requirements.txt
```

## 🛠️ Usage
Given a root directory to look for experiments (type `python tbtui.py --help` for more info) the script recursively searches for csv files that end in `.tbtui.csv`. Therefore you are required to save your metrics in a csv file named as 
```
<experiment-name>_tbtui.csv
```
e.g. `exp1.tbtui.csv`. `what_an_awesome_experiment.tbtui.csv`, `another_one_byte_the_dust.tbtui.csv`, etc...
Depending on the ML framework of choice there are different options to do so:
| Framework               | How to Save Metrics |
|-------------------------|----------------------------------------------------------------|
| **TensorFlow/Keras**    | Save `history.history` with `polars` or `pandas` (`pl.DataFrame(history.history).write_csv("experiment_name.tbtui.csv")`) or use the [CSVLogger callback](https://keras.io/api/callbacks/csv_logger/). |
| **PyTorch Lightning**   | Use the [CSVLogger callback](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.loggers.csv_logs.html). |
| **PyTorch**            | Keep a dictionary of your metrics and save it using `polars` or `pandas`. |

When one or more csvs are present, you can use the app to visualize the metrics across all the session's epochs!
An added functionality is that you can type `M` (caps) to toggle an annotation on the maximum value in the current plot, and `m` to toggle a corresponding annotation for the minimum value.


**EXAMPLE**
See example plots by navigating to the tbtui folder and typing 
```
python tbtui.py --path examples
```

## Remarks
As an ML engineer myself, I would find great usability in a tool like this, were it feature-rich. I hope that I can reach this project to a state that I will happily use it myself for both personal and professional experiments, and that it will prove usefull to other ML engineers as well.
  
