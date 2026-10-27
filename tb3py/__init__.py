from juliacall import Main as jl

# 1. Bring the Julia scientific library into scope
jl.seval("using ThreeBodyTB; using Plots")

#def makecrys(A, coords, types): 
#    """
#    Compute the modified Bessel function of the first kind 
#    by calling the underlying Julia implementation.
#    """
#    # juliacall automatically converts Python arguments to Julia and vice versa
#    result = jl.makecrys(A, coords, types)
#    return result

#def compute_bessel(v: float, x: float) -> float:
#    """
#    Compute the modified Bessel function of the first kind 
#    by calling the underlying Julia implementation.
#    """
#    # juliacall automatically converts Python arguments to Julia and vice versa
#    result = jl.besseli(v, x)
#    return result
