import numpy as np

def gaussian_pdf(x, mu, sigma):
    """ Gauss PDF fonksiyonu """
    return ( 1. / np.sqrt(2*np.pi) * sigma ) * np.exp( -0.5 * (x-mu/sigma)**2 ) 


def gaussian_cdf(x, mu, sigma):
    """ 
    Metod sadece x>=0 icin calisiyor ama Gaussian CDF'in ozelliginden dolayi 
    x <= 0 icin
    GaussianCDF(x) = 1 - GaussianCDF(-x) 
    """
    if x >=0:
        #Zelen severo'nun belirledigi katsayilar
        b0 = 0.2316419
        b1 = 0.319381530
        b2 = -0.356563782
        b3 = 1.781477937
        b4 = -1.821255978
        b5 = 1.330274429
        # Formulun kendisi
        t = 1. / (1 + b0 * x)
        expr = b1*t + b2*t**2 + b3* t**3+ b4*t**4+b5*t**5
    
        return 1 - gaussian_pdf(x, mu, sigma) * expr # GaussCDF = 1- GaussPDF*Formul
    else:
        return 1 - gaussian_cdf(-x, mu, sigma)

# Gorsellestirme
import matplotlib.pyplot as plt

x = np.arange(-10,10,0.01)
# 0 mean 1 standart sapma
y = [gaussian_pdf(i, 0., 1.) for i in x]
yc = [gaussian_cdf(i, 0., 1.) for i in x]

plt.plot(x,y,'r',x,yc,'g')
plt.legend(["Normal distribution","Normal destiny"])
plt.show()
