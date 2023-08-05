import numpy as np
import pandas as pd
import sympy as sy
import pandas as pd
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# BLS algorithm 
#------------------------------------------------------------------------------
def BLS(x, d, f, g, alpha_max = 1.0, alpha_min = 1e-6, 
        rho = 0.5, c1 = 0.1, c2 = 0.5, 
        strong_wolfe = False, out = True):
    """
    Parameters
    ----------
    x : initial point
    d : initial direction
    f : function
    g : gradient function
    alpha_max : initial value of alpha
    alpha_min : final minimum value of alpha
    rho, c1, c2 parameters
    strong_wolfe : indicator for Wolfe conditions
        - True : ask for Strong Wolfe conditions
        - False : (default) just Wolfe conditions
    out : print out logs. By default it is set to true
    
    Returns
    -------
    alph : the optimal alpha
    W_out : the satisfied Wolfe conditions
    
    """
    def WC1(al):
        return f(x+alph*d) <= f(x) + c1*g(x).T @ d*alph
    def WC2(al):
        return g(x+alph*d).T @ d >= c2*g(x).T @ d
    def SWC2(al):
        return np.abs(g(x+alph*d).T@d) <= c2*np.abs(g(x).T@d)
    # =========================================================================== #
    al, rh = sy.symbols('α ρ');
    if out == True:
        print("# ==================================================================== #")
        print("Initial point:", x.T)
        print("Initial direction:", d.T)
        print("Backtracking Linear Search Hyperparameters:")
        print("  ", al, " max:", alpha_max)
        print("  ", al, " min:", alpha_min)
        print("  ", rh, ":", rho)
        print("   c1:", c1)
        print("   c2:", c2)
        print("Asked for Strong Wolfe conditions: ", strong_wolfe)
        print("# ==================================================================== #")
    # =========================================================================== #
    # Acceptability conditions:
    def W(alph):
        if strong_wolfe:
            return WC1(alph) and SWC2(alph)
        else:
            return WC1(alph) and WC2(alph)
        
    # Initialization algorithm:
    alph = alpha_max
    
    # Loop: while the output condition is false ~.
    it_max = 100
    if out: print("Starting search...")
    it = 0
    while not W(alph) and alph > alpha_min:
        if out == True: print(al,"(",it, ")" " = ", alph, sep="")
        alph = rho*alph
        it += 1
        if it > it_max:
            break
    if out == True: 
        print(al,"(",it, ")" " = ", alph, sep="")
        print("# ==================================================================== #")
        if alph <= alpha_min:
            print("Stopped iterating by ",al, " min. NOT FOUND.")
        print("Output:", al,"=",alph)
    
    W_out = 0
    if WC1(alph):
        W_out = 1
    if WC1(alph) and WC2(alph):
        W_out = 2
    if WC1(alph) and SWC2(alph):
        W_out = 3
    if out == True:   
        # print result WC
        if W_out == 0:
            print("Does not satisfy any Wolfe Condition.")
        elif W_out == 1:
            print("Satisfies Wolfe Condition 1: Sufficient decrease.")
        elif W_out == 2:
            print("""Satisfies Wolfe Condition 1 and Wolfe Condition 2:\nSufficient decrease and Curvature condition.
            """)
        elif W_out == 3:
            print("""Satisfies Wolfe Condition 1 and Strong Wolfe Condition 2:\nSufficient decrease and (Strong) Curvature condition.
            """)
    return alph, W_out

# FIRST DERIVATIVE METHODS
#------------------------------------------------------------------------------
# Gradient method for any function f
#------------------------------------------------------------------------------
def GM(x, f, g, BLS_params, eps = 1e-6, kmax = 1500, precision = 6):
    """
    Parameters
    ----------
    x : initial point
    f : function
    g : gradient function
    BLS_params : dictionary with BLS parameters
    eps : epsilon for stopping condition on gradient norm
    kmax : maximum number of iterations
    precision : decimal precision on gradient norm
    
    Returns
    -------
    Xk : x at each iteration
    data : additional information on each iteration (alpha, gradient norm)
    
    """
    gradient_norm = round(np.linalg.norm(g(x)), precision)
    info = [[np.NaN, gradient_norm]]
    Xk = []
    dimension = len(x)
    for i in range(0, dimension):
        Xk.append([x[i].squeeze()])
    
    k = 0
    print("[GM] Initial:", x.T)
    # ================================================================================================ #  
    while np.linalg.norm(g(x)) > eps and k < kmax:
        d = -g(x)
        alpha, _ = BLS(x, d, f, g, **BLS_params)   # Backtracking Line Search
        x = x + alpha*d
        k += 1
        gradient_norm = np.round(np.linalg.norm(g(x)), precision)
        info.append([alpha, gradient_norm])
        for i in range(0, dimension):
            Xk[i].append(x[i].squeeze())
       # ============================================================================================== #  
    # OUTPUT:
    print("[GM] Final:",x.T)
    print("[GM] Iterations:", k)
    data = pd.DataFrame(info, columns=["alpha", "||g(x)||"], dtype=np.float)
    return Xk, data

#------------------------------------------------------------------------------
# Conjugate Gradient method
#------------------------------------------------------------------------------
def CGM(x, f, g, BLS_params, iCG, iRC, eps = 1e-6, kmax = 1500, precision = 6, nu = None):
    """
    Parameters
    ----------
    x : initial point
    f : function
    g : gradient function
    BLS_params : dictionary with BLS parameters
    eps : epsilon for stopping condition on gradient norm
    kmax : maximum number of iterations
    precision : decimal precision on gradient norm
    iCG : type of CGM. iCG 1 is FR, 2 is PR
    iRC : type of restart condition
    nu : needed for a restart condition
    
    Returns
    -------
    Xk : x at each iteration
    data : additional information on each iteration (alpha, gradient norm)
    
    """
    gradient_norm = round(np.linalg.norm(g(x)), precision)
    info = [[np.NaN, gradient_norm]]
    Xk = []
    dimension = len(x)
    for i in range(0, dimension):
        Xk.append([x[i].squeeze()])
    d = -g(x)
    k = 0
    print("[CGM] Initial:", x.T)
    if BLS_params['strong_wolfe'] != True:
        print("WARNING: ⚠️ in order to guarantee a descent direction, the step length α must satisfy SWC.")
    if BLS_params['c2'] >= 0.5:
        print("WARNING: ⚠️ in order to guarantee a descent direction, c2 must be smaller than 0.5.")
    # ======================================================================================================= #  
    while np.linalg.norm(g(x)) > eps and k < kmax:
        alpha, _ = BLS(x, d, f, g, **BLS_params)
        x, x_prev = x + alpha*d, x
        # ======================================================================================================= #  
        # CGM variants
        if iCG == 1:
            beta = (g(x).T @ g(x)) / (g(x_prev).T @ g(x_prev))
        elif iCG == 2:
            beta = max(0, g(x).T @ (g(x) - g(x_prev)) / (g(x_prev).T @ g(x_prev)))
        else:
            raise TypeError("iCG should be 1 (Fletcher-Reeves) or 2 (Polak-Ribière)")
        # ======================================================================================================= # 
        # Restart conditions
        if iRC > 0 and nu is None:
            raise TypeError(f"nu is a necessary parameter with iRC equal to {iRC}")
        if (iRC == 1 and k % nu == 0 or
                iRC == 2 and g(x).T @ g(x_prev) / np.linalg.norm(g(x))**2 > nu or
                k == 0):
            d = -g(x)
        else:
            d = -g(x) + beta*d
        # ======================================================================================================= # 
        k += 1
        gradient_norm = round(np.linalg.norm(g(x)), precision)
        info.append([alpha, gradient_norm])
        for i in range(0, dimension):
            Xk[i].append(x[i].squeeze())
    # ======================================================================================================= #
    # OUTPUT:
    print("[CGM] Final:",x.T)
    print("[CGM] Iterations:", k)
    data = pd.DataFrame(info, columns=["alpha", "||g(x)||"], dtype=np.float)
    return Xk, data


#------------------------------------------------------------------------------
# BFGS method
#------------------------------------------------------------------------------
def BFGS(x, f, g, BLS_params, eps = 1e-6, kmax = 1500, precision = 6):
    gradient_norm = round(np.linalg.norm(g(x)), precision)
    info = [[np.NaN, gradient_norm]]
    Xk = []
    dimension = len(x)
    for i in range(0, dimension):
        Xk.append([x[i].squeeze()])
    
    H = I = np.identity(len(g(x)))
    k = 0
    print("[BFGS] Initial:", x.T)
    while np.linalg.norm(g(x)) > eps and k < kmax:
        d = -H @ g(x)
        alpha, _ = BLS(x, d, f, g, **BLS_params)
        x, x_prev = x + alpha*d, x
        s = x - x_prev
        y = g(x) - g(x_prev)
        rho = 1 / ((y).T @ s)
        H = (I - rho * s @ y.T) @ H @ (I - rho * y @ (s.T)) + rho * s @ s.T
        k += 1
        gradient_norm = round(np.linalg.norm(g(x)), precision)
        info.append([alpha, gradient_norm])
        for i in range(0, dimension):
            Xk[i].append(x[i].squeeze())
        
    # ======================================================================================================= #
    # OUTPUT:
    print("[BFGS] Final:",x.T)
    print("[BFGS] Iterations:", k)
    data = pd.DataFrame(info, columns=["alpha", "||g(x)||"], dtype=np.float)
    return Xk, data

#------------------------------------------------------------------------------
# Plotter for 3D functions (only valid for two dimensions)
#------------------------------------------------------------------------------
def contour_map(f, x_axis, y_axis):
    """
    Parameters
    ----------
    f : function
    x_axis : minimization path of x
    y_axis : minimization path of y
   
    """
    xlist = np.linspace(np.min(x_axis) - 1, np.max(x_axis) + 1, 100)
    ylist = np.linspace(np.min(y_axis) - 1, np.max(y_axis) + 1, 100)

    X, Y = np.meshgrid(xlist, ylist)
    Z = f(np.array([X,Y]))
    plt.figure()
    cp = plt.contourf(X, Y, Z, cmap = 'YlGnBu', levels = 50)
    plt.colorbar(cp)
    plt.title('Descent directions')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(x_axis, y_axis, c = 'red')
    plt.axis('scaled')
    plt.show()
