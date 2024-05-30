"""
## Define simple association with structural model
$U_{0} \sim \mathcal{U}(0, 1)$

$U_{1} \sim \mathcal{N}(0, 1)$

$A := 1_{U_{0} > 0.61}$

$B := 1_{(A + 0.5*U_{1})>0.2}$
"""

print("ASSOCIATION")

import numpy as np
from scipy import stats
class BookSCM:
    def __init__(self, random_seed=None):
        self.random_seed = random_seed
        self.u_0 = stats.uniform()
        self.u_1 = stats.norm()
    def sample(self, sample_size=100):
        if self.random_seed:
            np.random.seed(self.random_seed)
            u_0 = self.u_0.rvs(sample_size) # rvs generate random variables based on sample size and distribution
            u_1 = self.u_1.rvs(sample_size)
            a = u_0 > 0.61
            b = (a + 0.5*u_1)>0.2
            return a, b
        
scm = BookSCM(random_seed=42)

buy_book_a, buy_book_b = scm.sample(100)

## Let's compute P(A|B)

proba_book_a_given_book_b = buy_book_a[buy_book_b].sum() /  buy_book_a[buy_book_b].shape[0] # coincidencias entre total
print(round(proba_book_a_given_book_b, 3))

print("INTERVENTION")
# new example of scm

class BookSCMv2:
    def __init__(self, random_seed=None):
        self.random_seed = random_seed
        self.u_0 = stats.uniform()
        self.u_1 = stats.norm()
    def sample(self, sample_size=100):
        if self.random_seed:
            np.random.seed(self.random_seed)
            u_0 = self.u_0.rvs(sample_size) # rvs generate random variables based on sample size and distribution
            u_1 = self.u_1.rvs(sample_size)
            a = u_0
            b = 5*a + u_1
            return a, b
        
scm = BookSCMv2(random_seed=45)

buy_book_a, buy_book_b = scm.sample(100)

r, p = stats.pearsonr(buy_book_a, buy_book_b)
b_mean = np.mean(buy_book_b)
b_var = np.var(buy_book_b)
print(f"Correlation: {r}, p-value: {p}") # Since it is a linear relationship, pearson corr is high
print(f"Mean of B before intervention: {b_mean}, Variance: {b_var}")
# Now let's intervene on A -> fixing its value by 1.5


class BookSCMv3:
    def __init__(self, random_seed=None):
        self.random_seed = random_seed
        self.u_0 = stats.uniform()
        self.u_1 = stats.norm()
    def sample(self, sample_size=100):
        if self.random_seed:
            np.random.seed(self.random_seed)
            u_0 = self.u_0.rvs(sample_size) # rvs generate random variables based on sample size and distribution
            u_1 = self.u_1.rvs(sample_size)
            a = np.array([1.5]*sample_size) # fix value on 1.5
            b = 5*a + u_1
            return a, b
        
scm = BookSCMv3(random_seed=45)

buy_book_a, buy_book_b = scm.sample(100)
r, p = stats.pearsonr(buy_book_a, buy_book_b)
print(f"Correlation: {r}, p-value: {p}") # Since it is a linear relationship, pearson corr is high
b_mean = np.mean(buy_book_b)
b_var = np.var(buy_book_b)
print(f"Correlation: {r}, p-value: {p}") # Since it is a linear relationship, pearson corr is high
print(f"Mean of B after intervention: {b_mean}, Variance: {b_var}")

# value of B is much higher now (since setting A to 1.5 returns higher values than setting them around a mean of 0 and a variance o 1 in normal dist.)

# IMPORTANT
# Had we intervened on B, it would have changed its value and the correlation coefficient, maybe to a non-significant one. That clearly tell us that A is independent from B but not vice versa (which ofc we have set initially with our functions)

print("CAUSATION WITHOUT (LINEAR) CORRELATION")
# obvio ejemplo tonto pero weno
x = np.random.uniform(-2, 2, 5000)
y = x**2 + 0.2*np.random.randn(len(x))

import matplotlib.pyplot as plt

plt.scatter(x, y)
plt.show()

print("COUNTERFACTUALS")
"""$P(Y_{X=0} = 1|X = 1, Y_{X=1} = 1)$

# probabilidad del estado Y = 1 si X hubiera sido 0 dado que lo que ha ocurrido ha sido Y = 1 y X = 1."""


## Principles:
# 1) Abduction: using evidence to calculate exogenous variables
# 2) Modification: replacing actual treatment with counterfactual values
# 3) Prediction: using the model to compute the counterfactual result

# modelo predefinido
class CounteractualSCM:
    def abduct(self, t, y): # nos da el valor de u (exógena) dado los valores reales del treatment y el resultado
        return (t + y - 1) / (2*t - 1)
    def modify(self, t): # modifica el modelo cambiando el valor de t teniendo en cuenta la variable exógena anterior
        return lambda u: t*u + (t - 1)*(u-1)
    def predict(self, u, t):  # toma el modelo modificado y predice el nuevo valor
        return self.modify(t)(u)
    
coffee = CounteractualSCM()
t = 1 # café
y = 1 # sentirse mal

u = coffee.abduct(t, y)
print(u)

coffee.predict(u=u, t=0) # devuelve y=0, el modelo contrafactual nos dice que sin el treatment no hubiera habido ese resultado


######################################################################33
# LINEAR REGRESSION

import statsmodels.api as sm
plt.style.use("fivethirtyeight")

np.random.seed(45)

n_samp = 5000

alpha = 1.12
beta = 0.93
error_param = 0.5

def draw_random_linear_reg(n_samp: int, alpha: float, beta: float, error_param: float=1):
    epsilon = np.random.rand(n_samp)
    X = np.random.rand(n_samp)
    y = alpha + beta*X + error_param*epsilon

    X = sm.add_constant(X) # la constante convierte la matriz en (n, 2) y obvio la constante no se puede multiplicar por beta!!!!
    model = sm.OLS(y, X)
    fitted_model = model.fit()
    print(fitted_model.summary())

draw_random_linear_reg(n_samp, alpha, beta, error_param)
