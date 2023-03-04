"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))
    

## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y



def subquadratic_multiply(x, y):
    ### TODO
    return _subquadratic_multiply(x,y).decimal_val
    ###
def _subquadratic_multiply(x,y):
  xvec = x.binary_vec
  yvec = y.binary_vec
  
  padding = pad(xvec, yvec)
  xvec = padding[0]
  yvec = padding[1]

  if x.decimal_val <= 1 and y.decimal_val <= 1:
    return BinaryNumber(x.decimal_val*y.decimal_val)
  
  else: 
    x_left = split_number(xvec)[0]
    x_right = split_number(xvec)[1]
    y_left = split_number(yvec)[0]
    y_right = split_number(yvec)[1]

    xl_yl = _subquadratic_multiply(x_left, y_left)

    xr_yr = _subquadratic_multiply(x_right, y_right)

    xlxr = BinaryNumber(x_right.decimal_val + x_left.decimal_val)

    ylyr = BinaryNumber(y_left.decimal_val + y_right.decimal_val)
    finalval = _subquadratic_multiply(xlxr,ylyr)
    finalval = BinaryNumber(finalval.decimal_val - xl_yl.decimal_val - xr_yr.decimal_val)
    newfinal = bit_shift(finalval,len(xvec)//2)
    newleft = bit_shift(xl_yl,len(xvec))
    return BinaryNumber(newleft.decimal_val + newfinal.decimal_val + xr_yr.decimal_val)
## Feel free to add your own tests here.
def test_multiply():
    assert subquadratic_multiply(BinaryNumber(4), BinaryNumber(4)) == 4*4
    assert subquadratic_multiply(BinaryNumber(100), BinaryNumber(7)) == 100*7
    assert subquadratic_multiply(BinaryNumber(1000), BinaryNumber(70)) == 1000*70
def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    return (time.time() - start)*1000

    
    

test_multiply()
print(time_multiply(100,7,subquadratic_multiply))
print(time_multiply(1000,70,subquadratic_multiply))
print(time_multiply(10070,7075,subquadratic_multiply))
print(time_multiply(1007000000,700292387375,subquadratic_multiply))