from bokeh.io import curdoc, show
from bokeh.layouts import column, widgetbox
from bokeh.models import ColumnDataSource, Slider, Button, TextInput
from bokeh.plotting import figure
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

t= np.arange(0,3000,10) #t outside function
def f(k1,k2,initial): #function to return the numpy array
    def rxn(initial,t): #function for the differential equations
        r1=k1*initial[0]
        r2=k2*initial[1]
        
        dAdt=-r1
        dBdt=r1-r2
        dCdt=r2
        
        return [dAdt, dBdt,dCdt]
    
    x0=[1,0,0]
    Conc = odeint(rxn, x0,t)
    
    return Conc

Conc=f(0.01,0.005,[1,0,0]) #Assign variable conc to resutls from function, f(initial conditions)

A=Conc[:,0]
B=Conc[:,1]
C=Conc[:,2]

source1 = ColumnDataSource(data = {'t': t,'A': A})
source2 = ColumnDataSource(data = {'t': t,'B': B})
source3 = ColumnDataSource(data = {'t': t,'C': C })

plot=figure()

plot.line('t','A', source=source1, color = 'red')
plot.line('t','B', source=source2, color = 'blue')
plot.line('t','C', source=source3, color = 'black')

slider1 = Slider(start = 0.001, end = 0.1, step = 0.001, value = 0.01, title = 'k1')
slider2 = Slider(start = 0.0005, end = 0.05, step = 0.0005, value = 0.005, title = 'k2')
input = TextInput(value = '0.1', title = 'Initial Concentration')

def callback(attr, old, new):
    k1 = slider1.value
    k2 = slider2.value
    A0 = float(input.value)
    
    new_conc=f(k1,k2,[A0,0,0])
    
    new_A=new_conc[:,0]
    new_B=new_conc[:,1]
    new_C=new_conc[:,2]
    
    source1.data={'t': t,'A': new_A}
    source2.data={'t': t,'B': new_B}
    source3.data={'t': t,'C': new_C}
    
input.on_change('value',callback)
slider1.on_change('value', callback)
slider2.on_change('value', callback)

layout = column(widgetbox(slider1, slider2, input),plot)

curdoc().add_root(layout)
