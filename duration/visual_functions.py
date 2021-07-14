import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def save_visual(location,name):
    """Save the visualisation in specified location with specified name"""
    
    link = location + name + '.jpg'
    plt.savefig(link,dpi=200)
    print(f'Visalisation saved in {link}')